"""Drought in cattle country (notebook 04; decision D26)."""
import json
from datetime import date

import pandas as pd
import requests

from . import config
from . import nass


def download(raw_dir):
    """Download state beef cows (NASS) and weekly drought stats (USDM) into raw_dir."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    states_raw = nass.get("api_GET", {
        "short_desc": "CATTLE, COWS, BEEF - INVENTORY", "agg_level_desc": "STATE",
        "source_desc": "SURVEY", "reference_period_desc": "FIRST OF JAN",
        "year": str(config.DROUGHT_WEIGHT_YEAR),
    })
    (raw_dir / "nass_beef_cows_by_state.json").write_text(json.dumps(states_raw))

    weights = state_weights(states_raw)
    start, end = f"1/1/{config.HERD_START_YEAR}", f"{date.today():%m/%d/%Y}"

    def usdm(area, aoi):
        resp = requests.get(f"{config.USDM_BASE}/{area}/GetDroughtSeverityStatisticsByAreaPercent",
                            params={"aoi": aoi, "startdate": start, "enddate": end, "statisticsType": 1},
                            headers={"Accept": "application/json"}, timeout=120)
        if resp.status_code != 200:
            raise RuntimeError(f"Drought Monitor failed for {aoi} ({resp.status_code}): {resp.text[:300]}")
        return resp.json()

    stats = {st["state_alpha"]: usdm("StateStatistics", str(st["state_fips_code"]).zfill(2))
             for _, st in weights.iterrows()}
    stats["CONUS"] = usdm("USStatistics", "conus")
    (raw_dir / "usdm_state_stats.json").write_text(json.dumps(stats))
    return raw_dir


def state_weights(states_raw):
    """States holding >= 75% of U.S. beef cows in the weight year, weighted by their cows (D26)."""
    states = pd.DataFrame(states_raw["data"])
    states = states[states["domain_desc"] == "TOTAL"].copy()
    states["beef_cows"] = pd.to_numeric(states["Value"].str.replace(",", "", regex=False), errors="coerce")
    us_total = states["beef_cows"].sum()   # includes any grouped "other states"
    states = states[~states["state_name"].str.upper().str.startswith("OTHER")
                    & ~states["state_fips_code"].astype(str).isin(["98", "99"])]
    states = (states[["state_name", "state_alpha", "state_fips_code", "beef_cows"]]
              .dropna().sort_values("beef_cows", ascending=False).reset_index(drop=True))
    states["share_of_us_pct"] = states["beef_cows"] / us_total * 100
    states["cumulative_pct"] = states["share_of_us_pct"].cumsum()
    n_keep = int((states["cumulative_pct"] < config.DROUGHT_COVERAGE_TARGET).sum()) + 1
    kept = states.head(n_keep).copy()
    kept["weight"] = kept["beef_cows"] / kept["beef_cows"].sum()
    kept["weight_year"] = config.DROUGHT_WEIGHT_YEAR
    return kept


def _weekly(rows, area):
    df = pd.DataFrame(rows)
    df.columns = [col.lower() for col in df.columns]
    date_col = "validstart" if "validstart" in df.columns else "mapdate"
    raw_dates = df[date_col].astype(str)
    if raw_dates.str.fullmatch(r"\d{8}").all():
        df["week"] = pd.to_datetime(raw_dates, format="%Y%m%d")
    else:
        df["week"] = pd.to_datetime(raw_dates.str[:10])
    for col in ["d0", "d1", "d2", "d3", "d4"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["area"] = area
    return df[["area", "week", "d0", "d1", "d2", "d3", "d4"]]


def build(raw_dir):
    """Return (monthly drought measures, state weights)."""
    weights = state_weights(json.loads((raw_dir / "nass_beef_cows_by_state.json").read_text()))
    stats = json.loads((raw_dir / "usdm_state_stats.json").read_text())
    weekly = pd.concat([_weekly(rows, area) for area, rows in stats.items()], ignore_index=True)

    cats = ["d0", "d1", "d2", "d3", "d4"]
    ordered = ((weekly["d0"] >= weekly["d1"] - 0.01) & (weekly["d1"] >= weekly["d2"] - 0.01)
               & (weekly["d2"] >= weekly["d3"] - 0.01) & (weekly["d3"] >= weekly["d4"] - 0.01))
    if not ordered.all() or not weekly[cats].stack().between(0, 100).all():
        raise ValueError("Drought data is not in cumulative format or has values outside 0-100")

    weekly["d2_plus_pct"] = weekly["d2"]
    weekly["dsci"] = weekly[cats].sum(axis=1)
    weekly["month"] = weekly["week"].dt.to_period("M").dt.to_timestamp()
    weekly = weekly[weekly["month"] >= f"{config.HERD_START_YEAR}-01-01"]
    monthly = weekly.groupby(["area", "month"])[["d2_plus_pct", "dsci"]].mean().reset_index()

    w = weights.set_index("state_alpha")["weight"]
    st = monthly[monthly["area"].isin(w.index)].copy()
    st["w"] = st["area"].map(w)
    out = pd.DataFrame({
        "cattle_d2_plus_pct": (st["d2_plus_pct"] * st["w"]).groupby(st["month"]).sum()
                              / st["w"].groupby(st["month"]).sum(),
        "cattle_dsci": (st["dsci"] * st["w"]).groupby(st["month"]).sum() / st["w"].groupby(st["month"]).sum(),
    })
    conus = monthly[monthly["area"] == "CONUS"].set_index("month")
    out["conus_d2_plus_pct"] = conus["d2_plus_pct"]
    out["conus_dsci"] = conus["dsci"]
    return out.rename_axis("date").round(3).reset_index(), weights
