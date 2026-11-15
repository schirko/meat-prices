"""Refresh all data with one command (D29).

Usage (from the project folder, with the virtual environment active):

    python -m src.refresh              download everything, rebuild, check, publish
    python -m src.refresh --offline    rebuild from the latest saved raw files (no downloads)
    python -m src.refresh --dry-run    do everything except replace the current files

How it stays safe:
1. New raw downloads go into dated folders under data/raw/ (never overwriting old ones).
2. Every processed file and the master table are built into a temporary folder first.
3. The data checks (src/checks.py) run on the new master table.
4. Only if every check passes are the new files copied into data/processed/ and the
   data dictionary rewritten. Otherwise the current files are left untouched.
5. A short report is written to data/processed/REFRESH_REPORT.md either way.
"""
import argparse
import json
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import pandas as pd

from . import bls, checks, config, drought, ers, master, nass

PROCESSED_FILES = [
    "ers_price_spreads_monthly.csv",
    "nass_herd_jan1.csv",
    "nass_slaughter_monthly.csv",
    "drought_cattle_country_monthly.csv",
    "drought_state_weights.csv",
    "cpi_grocery_categories_monthly.csv",
    "master_monthly.csv",
]


def latest(pattern):
    """Most recent raw file or folder matching a pattern like 'ers_*' (names end in YYYYMMDD)."""
    found = sorted(p for p in config.RAW_DIR.glob(pattern) if p.name[-8:].isdigit() or p.stem[-8:].isdigit())
    if not found:
        raise FileNotFoundError(f"No raw data matching data/raw/{pattern}; run without --offline first")
    return found[-1]


def download_all(stamp, log):
    log("Downloading BLS prices and CPI categories...")
    bls.download(config.RAW_DIR, stamp)
    log("Downloading USDA ERS price spreads...")
    ers.download(config.RAW_DIR / f"ers_{stamp}")
    log("Downloading USDA NASS herd and slaughter...")
    nass.download(config.RAW_DIR / f"nass_{stamp}")
    log("Downloading state beef cows and Drought Monitor statistics...")
    drought.download(config.RAW_DIR / f"drought_{stamp}")


def build_all(out_dir, log):
    """Build every processed file into out_dir from the latest raw files. Returns (master, base_month, sources)."""
    sources = {
        "bls_prices": latest("bls_prices_*.json"),
        "bls_cpi_categories": latest("bls_cpi_categories_*.json"),
        "ers": latest("ers_*"),
        "nass": latest("nass_*"),
        "drought": latest("drought_*"),
    }
    for name, path in sources.items():
        log(f"Using {path.relative_to(config.PROJECT_ROOT)}")

    prices = bls.chosen_prices(json.loads(sources["bls_prices"].read_text()))
    cpi_cats = bls.cpi_categories(json.loads(sources["bls_cpi_categories"].read_text()))
    spreads = ers.build(sources["ers"])
    herd, slaughter = nass.build(sources["nass"])
    drought_monthly, weights = drought.build(sources["drought"])

    spreads.to_csv(out_dir / "ers_price_spreads_monthly.csv", index=False)
    herd.to_csv(out_dir / "nass_herd_jan1.csv", index=False)
    slaughter.to_csv(out_dir / "nass_slaughter_monthly.csv", index=False)
    drought_monthly.to_csv(out_dir / "drought_cattle_country_monthly.csv", index=False)
    weights.to_csv(out_dir / "drought_state_weights.csv", index=False)
    cpi_cats.to_csv(out_dir / "cpi_grocery_categories_monthly.csv", index=False)

    table, base_month = master.build(prices, spreads, herd, slaughter, drought_monthly, cpi_cats)
    table.reset_index().to_csv(out_dir / "master_monthly.csv", index=False, float_format="%.4f")
    master.write_dictionary(table, base_month, cpi_cats["category"].unique(),
                            out_dir / "DATA_DICTIONARY.md", "`python -m src.refresh`")
    log(f"Built master table: {len(table)} months x {table.shape[1]} columns, "
        f"{table.index.min():%Y-%m} to {table.index.max():%Y-%m}")
    return table, base_month, sources


def compare_with_current(new):
    """Plain-language summary of what changed against the current master table."""
    path = config.PROCESSED_DIR / "master_monthly.csv"
    if not path.exists():
        return ["No current master table to compare with."]
    old = checks.load_master(path)
    lines = [f"Months: {len(old)} before, {len(new)} now "
             f"(latest month {old.index.max():%Y-%m} -> {new.index.max():%Y-%m})."]
    added = [c for c in new.columns if c not in old.columns]
    removed = [c for c in old.columns if c not in new.columns]
    if added:
        lines.append(f"New columns: {', '.join(added)}")
    if removed:
        lines.append(f"Removed columns: {', '.join(removed)}")
    # Revisions: published values that changed by more than 0.5% in months both tables share
    shared = new.index.intersection(old.index)
    revised = []
    for col in new.columns.intersection(old.columns).drop("filled_columns"):
        a, b = old.loc[shared, col], new.loc[shared, col]
        if col.endswith("_price_real") or col.endswith("_2015eq100"):
            continue   # these move whenever the base month moves; not a revision
        rel = ((b - a).abs() / a.abs().clip(lower=1e-9)).dropna()
        if (rel > 0.005).any():
            revised.append(f"{col} ({int((rel > 0.005).sum())} months)")
    lines.append("Revised past values (>0.5%): " + (", ".join(revised) if revised else "none"))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description="Refresh all meat-prices data (D29).")
    parser.add_argument("--offline", action="store_true", help="rebuild from saved raw files, no downloads")
    parser.add_argument("--dry-run", action="store_true", help="build and check, but don't replace current files")
    args = parser.parse_args(argv)

    report = [f"# Refresh report", "", f"Run: {datetime.now():%Y-%m-%d %H:%M}", ""]

    def log(msg):
        print(msg)
        report.append(f"- {msg}")

    stamp = config.today_stamp()
    try:
        if not args.offline:
            download_all(stamp, log)
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            table, base_month, _ = build_all(tmp, log)
            problems = checks.run_all(table, (tmp / "DATA_DICTIONARY.md").read_text(encoding="utf-8"))
            report += ["", "## Checks", ""]
            if problems:
                for name, probs in problems.items():
                    report += [f"- **{name}** FAILED"] + [f"  - {p}" for p in probs]
            else:
                report.append("- All checks passed.")
            report += ["", "## Changes", ""] + [f"- {line}" for line in compare_with_current(table)]

            if problems:
                status, code = "NOT published: checks failed. Current files were left unchanged.", 1
            elif args.dry_run:
                status, code = "NOT published: dry run.", 0
            else:
                for name in PROCESSED_FILES:
                    shutil.copy2(tmp / name, config.PROCESSED_DIR / name)
                shutil.copy2(tmp / "DATA_DICTIONARY.md", config.DOCS_DIR / "DATA_DICTIONARY.md")
                status, code = (f"Published: data/processed/ and docs/DATA_DICTIONARY.md updated "
                                f"(real prices in {base_month:%B %Y} dollars)."), 0
    except Exception as exc:   # report the failure instead of a bare traceback
        status, code = f"FAILED before checks: {type(exc).__name__}: {exc}", 2

    report += ["", "## Result", "", status, ""]
    (config.PROCESSED_DIR / "REFRESH_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(status)
    return code


if __name__ == "__main__":
    sys.exit(main())
