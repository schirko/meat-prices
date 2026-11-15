"""Combine everything into master_monthly.csv and write the data dictionary (notebook 06; D18, D27)."""
import re

import pandas as pd

from . import config


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def fill_short_gaps(df, max_gap=config.MAX_FILL_GAP):
    """Fill gaps of up to max_gap months that have values on both sides (D18).

    Straight-line interpolation: for one missing month, the average of its neighbors.
    Returns (filled table, list of (date, column) pairs that were filled).
    """
    out, log = df.copy(), []
    for col in df.columns:
        s = df[col]
        is_na = s.isna()
        run_id = (is_na != is_na.shift()).cumsum()
        for _, run in s[is_na].groupby(run_id[is_na]):
            start, end = run.index.min(), run.index.max()
            inside = s.loc[:start].notna().any() and s.loc[end:].notna().any()
            if len(run) <= max_gap and inside:
                out[col] = out[col].where(~out.index.isin(run.index), s.interpolate(limit_area="inside"))
                log.extend((d, col) for d in run.index)
    return out, log


def build(prices, ers, herd, slaughter, drought, cpi_cats):
    """Return (master table indexed by month, base month for real prices).

    prices: wide BLS table from bls.chosen_prices(); the others are the processed tables.
    """
    bls, fill_log = fill_short_gaps(prices)
    base_month = bls["cpi_all_items"].last_valid_index()
    base_cpi = bls.loc[base_month, "cpi_all_items"]
    for meat in ["beef", "pork", "chicken"]:
        bls[f"{meat}_price_real"] = bls[f"{meat}_price"] * base_cpi / bls["cpi_all_items"]

    ers_wide = ers.assign(column="ers_" + ers["meat"].str.lower() + "_" + ers["measure"]) \
                  .pivot_table(index="date", columns="column", values="value")

    months = pd.date_range(f"{config.HERD_START_YEAR}-01-01", base_month, freq="MS")
    herd_m = pd.DataFrame({"year": months.year}, index=months)
    herd_m = herd_m.merge(herd.drop(columns="reference_date"), on="year", how="left").set_index(months)
    herd_m = herd_m.drop(columns="year").add_prefix("herd_").add_suffix("_jan1")

    slaughter_m = slaughter.set_index("date").add_prefix("slaughter_")
    drought_m = drought.set_index("date").add_prefix("drought_")

    cats = cpi_cats.pivot_table(index="date", columns="category", values="value")
    cats = cats.reindex(pd.date_range(cats.index.min(), cats.index.max(), freq="MS"))
    cats, cat_log = fill_short_gaps(cats)
    cats_idx = cats / cats.loc[str(config.PRICE_START_YEAR)].mean() * 100
    cats_idx.columns = ["cpi_" + slug(c) + "_2015eq100" for c in cats_idx.columns]

    master = pd.DataFrame(index=months)
    for part in [bls, ers_wide, herd_m, slaughter_m, drought_m, cats_idx]:
        master = master.join(part, how="left")

    fills = [(d, c) for d, c in fill_log] + [(d, "cpi_" + slug(c) + "_2015eq100") for d, c in cat_log]
    filled = pd.DataFrame(fills, columns=["date", "column"])
    text = filled.groupby("date")["column"].apply(lambda s: ";".join(sorted(set(s)))) if len(filled) else pd.Series(dtype=str)
    master["filled_columns"] = text.reindex(master.index).fillna("")
    master.index.name = "date"
    return master, base_month


def describe(master, base_month, cpi_categories):
    """Description, units and source for every column. Raises if any column is undocumented."""
    meat_price = {"beef": "ground beef, 100% beef (BLS APU0000703112)",
                  "pork": "all pork chops (BLS APU0000FD3101)",
                  "chicken": "boneless chicken breast (BLS APU0000FF1101)"}
    ers_measure = {
        "retail": ("Retail value: what shoppers pay", "cents per lb, retail equivalent"),
        "wholesale": ("Wholesale value: what the packer/processor gets", "cents per lb, retail equivalent"),
        "net_farm": ("Net farm value: what the rancher/farmer gets, minus byproducts", "cents per lb, retail equivalent"),
        "spread_farm_to_wholesale": ("Farm-to-wholesale spread (roughly the packer's part)", "cents per lb, retail equivalent"),
        "spread_wholesale_to_retail": ("Wholesale-to-retail spread (roughly the store's part)", "cents per lb, retail equivalent"),
        "farmer_share_pct": ("Farm share of the retail value", "percent"),
        "packer_share_pct": ("Packer share of the retail value", "percent"),
        "store_share_pct": ("Store share of the retail value", "percent"),
    }
    d = {"cpi_all_items": ("CPI, all items, U.S. city average, not seasonally adjusted (CUUR0000SA0)",
                           "index, 1982-84 = 100", "BLS"),
         "filled_columns": ("Columns whose value this month was filled (D18); empty if none",
                            "text, semicolon-separated", "calculated")}
    for meat, label in meat_price.items():
        d[f"{meat}_price"] = (f"Average U.S. retail price, {label}", "$ per lb, at the time", "BLS")
        d[f"{meat}_price_real"] = (f"Same price in {base_month:%B %Y} dollars (adjusted with CPI, all items)",
                                   f"$ per lb, {base_month:%b %Y} dollars", "calculated")
    for col in master.columns:
        if col.startswith("ers_"):
            _, meat, measure = col.split("_", 2)
            text, units = ers_measure[measure]
            d[col] = (f"{meat.capitalize()}: {text}", units, "USDA ERS (spreads and shares calculated, D22)")
    herd_text = {"all_cattle": "All cattle and calves", "beef_cows": "Beef cows",
                 "beef_replacement_heifers": "Beef replacement heifers, 500 lb and over"}
    for key, text in herd_text.items():
        d[f"herd_{key}_jan1"] = (f"{text} on January 1 of this month's year (repeated each month, D27)",
                                 "head", "USDA NASS")
    d.update({
        "slaughter_beef_cows_slaughtered": ("Beef cows slaughtered this month, federally inspected", "head", "USDA NASS"),
        "slaughter_heifers_slaughtered": ("Heifers slaughtered this month, federally inspected", "head", "USDA NASS"),
        "slaughter_steers_slaughtered": ("Steers slaughtered this month, federally inspected", "head", "USDA NASS"),
        "slaughter_heifer_share_pct": ("Heifers as % of heifer + steer slaughter", "percent", "calculated"),
        "slaughter_beef_cows_slaughtered_12mo": ("Beef cows slaughtered in the 12 months ending this month", "head", "calculated"),
        "drought_cattle_d2_plus_pct": ("Cattle country (beef-cow-weighted states, D26): % of area in severe drought or worse", "percent of area", "U.S. Drought Monitor"),
        "drought_cattle_dsci": ("Cattle country: Drought Severity and Coverage Index", "index, 0-500", "U.S. Drought Monitor"),
        "drought_conus_d2_plus_pct": ("Lower 48 states: % of area in severe drought or worse", "percent of area", "U.S. Drought Monitor"),
        "drought_conus_dsci": ("Lower 48 states: Drought Severity and Coverage Index", "index, 0-500", "U.S. Drought Monitor"),
    })
    for cat in cpi_categories:
        d["cpi_" + slug(cat) + "_2015eq100"] = (f"CPI, {cat}, rebased so the 2015 average = 100",
                                                "index, 2015 average = 100", "BLS (rebased)")
    missing = [c for c in master.columns if c not in d]
    if missing:
        raise KeyError(f"No description for: {missing}")
    return d


def write_dictionary(master, base_month, cpi_categories, path, generated_by):
    """Write docs/DATA_DICTIONARY.md from the table itself, so it can't drift out of date."""
    desc = describe(master, base_month, cpi_categories)
    lines = ["# Data dictionary: `data/processed/master_monthly.csv`", "",
             f"Generated by {generated_by}; do not edit by hand.", "",
             f"One row per month, {master.index.min():%B %Y} to {master.index.max():%B %Y} "
             f"({len(master)} rows, {master.shape[1] + 1} columns including `date`).", "",
             "| Column | Description | Units | Source | First month | Last month |",
             "|---|---|---|---|---|---|",
             "| `date` | First day of the month | date | | | |"]
    for col in master.columns:
        text, units, source = desc[col]
        s = master[col] if col != "filled_columns" else pd.Series(dtype=float)
        first, last = s.first_valid_index(), s.last_valid_index()
        f = first.strftime("%Y-%m") if first is not None else ""
        l = last.strftime("%Y-%m") if last is not None else ""
        lines.append(f"| `{col}` | {text} | {units} | {source} | {f} | {l} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
