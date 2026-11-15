"""USDA ERS meat price spreads (notebook 02; decisions D21-D23)."""
import pandas as pd
import requests

from . import config


def download(raw_dir):
    """Download the four ERS CSV files into raw_dir (e.g. data/raw/ers_YYYYMMDD/)."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    for name, url in config.ERS_FILES.items():
        resp = requests.get(url, headers=config.HTTP_HEADERS, timeout=60)
        resp.raise_for_status()
        (raw_dir / f"{name}.csv").write_bytes(resp.content)
    return raw_dir


def load_file(path, source_name):
    """Load one ERS CSV into monthly rows: date, data_item, value, units, source_file."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [col.strip() for col in df.columns]
    month_col = next(col for col in ["Month-number", "Month_Number", "Period_Number"] if col in df.columns)
    df["month_num"] = pd.to_numeric(df[month_col], errors="coerce")
    df = df[df["month_num"].between(1, 12)].copy()   # drop quarters (13-16) and annual (17)
    df["date"] = pd.to_datetime(dict(year=df["Year"].astype(int), month=df["month_num"].astype(int), day=1))
    # Values of 1,000 or more have a thousands comma ("1,011.3")
    df["value"] = pd.to_numeric(df["Value"].astype(str).str.replace(",", "", regex=False), errors="coerce")
    out = df.rename(columns={"Data_Item": "data_item", "Units": "units"})
    out["data_item"] = out["data_item"].str.strip()
    out["source_file"] = source_name
    return out[["date", "data_item", "value", "units", "source_file"]]


def build(raw_dir):
    """Combine the ERS files into the long spreads table (ers_price_spreads_monthly.csv)."""
    frames = {name: load_file(raw_dir / f"{name}.csv", name) for name in config.ERS_FILES}

    def pick(source, item):
        df = frames[source]
        s = df[(df["data_item"] == item) & (df["date"] >= f"{config.PRICE_START_YEAR}-01-01")]
        return s.set_index("date")["value"].dropna().sort_index()

    # Keep three values per meat; recent file wins where files overlap (D22)
    pieces = []
    for meat, measure, hist_name, recent_file, recent_name in config.ERS_ITEM_MAP:
        h = pick("historical", hist_name).to_frame("value")
        if recent_file is not None:
            r = pick(recent_file, recent_name).to_frame("value")
            h = pd.concat([h[~h.index.isin(r.index)], r])
        pieces.append(h.assign(meat=meat, measure=measure))
    # Chicken's recent wholesale value = retail - published spread (D22)
    derived = (pick("summary_recent", config.ERS_CHICKEN_RECENT_RETAIL)
               - pick("summary_recent", config.ERS_CHICKEN_RECENT_SPREAD)).dropna()
    pieces.append(derived.to_frame("value").assign(meat="Chicken", measure="wholesale"))
    values = pd.concat(pieces).rename_axis("date").reset_index()

    # Calculate spreads and shares ourselves (D22, D23)
    wide = values.pivot_table(index="date", columns=["meat", "measure"], values="value")
    calc = {}
    for meat in ["Beef", "Pork", "Chicken"]:
        retail, wholesale = wide[(meat, "retail")], wide[(meat, "wholesale")]
        calc[(meat, "retail")] = retail
        calc[(meat, "wholesale")] = wholesale
        calc[(meat, "spread_wholesale_to_retail")] = retail - wholesale
        calc[(meat, "store_share_pct")] = (retail - wholesale) / retail * 100
        if (meat, "net_farm") in wide.columns:
            net_farm = wide[(meat, "net_farm")]
            calc[(meat, "net_farm")] = net_farm
            calc[(meat, "spread_farm_to_wholesale")] = wholesale - net_farm
            calc[(meat, "farmer_share_pct")] = net_farm / retail * 100
            calc[(meat, "packer_share_pct")] = (wholesale - net_farm) / retail * 100
    spreads = pd.DataFrame(calc)
    spreads.columns = pd.MultiIndex.from_tuples(spreads.columns, names=["meat", "measure"])

    out = (spreads.melt(ignore_index=False).dropna(subset=["value"]).reset_index()
           .sort_values(["meat", "measure", "date"]))
    out["units"] = out["measure"].map(lambda m: "percent of retail value" if m.endswith("_pct")
                                      else "cents per pound of retail equivalent")
    return out.reset_index(drop=True)
