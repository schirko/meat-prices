"""BLS retail meat prices and CPI categories (notebooks 01 and 05)."""
import json
from datetime import date

import pandas as pd
import requests

from . import config


def fetch(series_ids, start_year, end_year, key):
    """One BLS API v2 request for up to 50 series. Raises if BLS reports a failure."""
    payload = {"seriesid": list(series_ids), "startyear": str(start_year),
               "endyear": str(end_year), "registrationkey": key}
    resp = requests.post(config.BLS_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS request failed: {data.get('status')} {data.get('message')}")
    return data


def download(raw_dir, stamp):
    """Download both BLS files into raw_dir with the same names the notebooks use."""
    key = config.api_key("BLS_API_KEY")
    if not key:
        raise RuntimeError("BLS_API_KEY is missing from .env")
    end = date.today().year
    files = {}
    for name, series in [("bls_prices", config.BLS_PRICE_CANDIDATES),
                         ("bls_cpi_categories", list(config.CPI_CATEGORIES))]:
        data = fetch(series, config.PRICE_START_YEAR, end, key)
        path = raw_dir / f"{name}_{stamp}.json"
        path.write_text(json.dumps(data, indent=2))
        files[name] = path
    return files


def parse(raw):
    """Turn a BLS API response into a long table: series_id, date, value (monthly rows only)."""
    rows = []
    for s in raw["Results"]["series"]:
        for o in s["data"]:
            if o["period"].startswith("M") and o["period"] != "M13":
                rows.append({"series_id": s["seriesID"],
                             "date": pd.Timestamp(int(o["year"]), int(o["period"][1:]), 1),
                             "value": pd.to_numeric(o["value"], errors="coerce")})
    return pd.DataFrame(rows).sort_values(["series_id", "date"]).reset_index(drop=True)


def chosen_prices(raw_prices):
    """Wide monthly table of the four chosen series (D15), one row per month, gaps left as NaN."""
    long = parse(raw_prices)
    long = long[long["series_id"].isin(config.BLS_CHOSEN)]
    wide = long.assign(column=long["series_id"].map(config.BLS_CHOSEN)) \
               .pivot_table(index="date", columns="column", values="value")
    wide = wide.reindex(pd.date_range(wide.index.min(), wide.index.max(), freq="MS"))
    return wide[list(config.BLS_CHOSEN.values())]


def cpi_categories(raw_cpi):
    """The processed grocery-category table from notebook 05 (cpi_grocery_categories_monthly.csv)."""
    cpi = parse(raw_cpi)
    cpi["group"] = cpi["series_id"].map(lambda s: config.CPI_CATEGORIES[s][0])
    cpi["category"] = cpi["series_id"].map(lambda s: config.CPI_CATEGORIES[s][1])
    avg_2015 = cpi[cpi["date"].dt.year == 2015].groupby("series_id")["value"].mean()
    cpi["index_2015"] = cpi["value"] / cpi["series_id"].map(avg_2015) * 100
    return cpi[["date", "series_id", "group", "category", "value", "index_2015"]]
