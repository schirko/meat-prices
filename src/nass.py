"""USDA NASS cattle herd and slaughter (notebook 03; decisions D24, D25)."""
import json

import pandas as pd
import requests

from . import config


def get(endpoint, params):
    """Call a Quick Stats endpoint. Never prints the URL, which contains the key."""
    key = config.api_key("NASS_API_KEY")
    if not key:
        raise RuntimeError("NASS_API_KEY is missing from .env")
    resp = requests.get(f"{config.NASS_BASE}/{endpoint}/",
                        params={"key": key, "format": "JSON", **params}, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"NASS {endpoint} failed ({resp.status_code}): {resp.text[:300]}")
    return resp.json()


def download(raw_dir):
    """Download inventory and slaughter into raw_dir (e.g. data/raw/nass_YYYYMMDD/)."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    for name, params in config.NASS_QUERIES.items():
        count = int(get("get_counts", params)["count"])
        if count > config.NASS_ROW_LIMIT:
            raise RuntimeError(f"NASS query '{name}' would return {count:,} rows (limit {config.NASS_ROW_LIMIT:,})")
        (raw_dir / f"{name}.json").write_text(json.dumps(get("api_GET", params), indent=1))
    return raw_dir


def _to_frame(rows):
    df = pd.DataFrame(rows)
    df["value"] = pd.to_numeric(df["Value"].astype(str).str.strip().str.replace(",", "", regex=False),
                                errors="coerce")   # (D), (NA), (Z) become NaN
    df["year"] = df["year"].astype(int)
    return df


def build(raw_dir):
    """Return (herd, slaughter): the two processed NASS tables."""
    inv = _to_frame(json.loads((raw_dir / "inventory.json").read_text())["data"])
    sl = _to_frame(json.loads((raw_dir / "slaughter.json").read_text())["data"])

    herd_rows = inv[inv["short_desc"].isin(config.HERD_SERIES)
                    & (inv["reference_period_desc"] == "FIRST OF JAN")
                    & (inv["domain_desc"] == "TOTAL")]
    herd = (herd_rows.assign(series=herd_rows["short_desc"].map(config.HERD_SERIES))
            .pivot_table(index="year", columns="series", values="value", aggfunc="first")
            [list(config.HERD_SERIES.values())])
    herd.columns.name = None
    herd = herd.reset_index()
    herd.insert(1, "reference_date", herd["year"].astype(str) + "-01-01")

    srows = sl[sl["short_desc"].isin(config.SLAUGHTER_SERIES) & (sl["domain_desc"] == "TOTAL")].copy()
    srows["date"] = pd.to_datetime(dict(
        year=srows["year"],
        month=pd.to_datetime(srows["reference_period_desc"], format="%b").dt.month,
        day=1))
    slaughter = (srows.assign(series=srows["short_desc"].map(config.SLAUGHTER_SERIES))
                 .pivot_table(index="date", columns="series", values="value", aggfunc="first")
                 [list(config.SLAUGHTER_SERIES.values())])
    slaughter.columns.name = None
    slaughter["heifer_share_pct"] = (slaughter["heifers_slaughtered"]
                                     / (slaughter["heifers_slaughtered"] + slaughter["steers_slaughtered"]) * 100)
    slaughter["beef_cows_slaughtered_12mo"] = slaughter["beef_cows_slaughtered"].rolling(12).sum()
    return herd, slaughter.rename_axis("date").reset_index()
