"""Project settings shared by the refresh pipeline, the tests and (later) the app.

Every choice here is documented in docs/DECISIONS.md; the decision number is
given next to each setting.
"""
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

load_dotenv(PROJECT_ROOT / ".env")


def api_key(name):
    """Read an API key from .env (D10). Returns '' if missing; callers decide whether that's fatal."""
    return os.getenv(name, "").strip()


def today_stamp():
    return f"{date.today():%Y%m%d}"


# ---- Time ranges -----------------------------------------------------------
PRICE_START_YEAR = 2015   # D3: prices, ERS spreads and grocery CPIs
HERD_START_YEAR = 2010    # D24: herd, slaughter and drought

# ---- BLS (items 1.1, 1.2, 1.7) --------------------------------------------
BLS_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Notebook 01 candidates, kept so the raw download matches the notebook (D15)
BLS_PRICE_CANDIDATES = [
    "APU0000703112", "APU0000FD3101", "APU0000704211", "APU0000704212",
    "APU0000706111", "APU0000FF1101", "CUUR0000SA0",
]
# D15: the chosen series and their column names in the master table
BLS_CHOSEN = {
    "APU0000703112": "beef_price",
    "APU0000FD3101": "pork_price",
    "APU0000FF1101": "chicken_price",
    "CUUR0000SA0": "cpi_all_items",
}
# Item 1.7 (D19): grocery categories, (group, category)
CPI_CATEGORIES = {
    "CUUR0000SA0":     ("Overall",          "All items"),
    "CUUR0000SAF11":   ("Overall",          "Food at home"),
    "CUUR0000SEFV":    ("Overall",          "Food away from home"),
    "CUUR0000SAF111":  ("Grocery category", "Cereals and bakery"),
    "CUUR0000SAF112":  ("Grocery category", "Meats, poultry, fish and eggs"),
    "CUUR0000SEFJ":    ("Grocery category", "Dairy"),
    "CUUR0000SAF113":  ("Grocery category", "Fruits and vegetables"),
    "CUUR0000SAF1131": ("Grocery category", "Fresh fruits and vegetables"),
    "CUUR0000SEFM":    ("Grocery category", "Processed fruits and vegetables"),
    "CUUR0000SAF114":  ("Grocery category", "Nonalcoholic beverages"),
    "CUUR0000SAF115":  ("Grocery category", "Other food at home (packaged)"),
    "CUUR0000SEFC":    ("Protein detail",   "Beef and veal"),
    "CUUR0000SEFD":    ("Protein detail",   "Pork"),
    "CUUR0000SEFF":    ("Protein detail",   "Poultry"),
    "CUUR0000SEFH":    ("Protein detail",   "Eggs"),
}

# ---- USDA ERS (item 1.3, D21-D23) -----------------------------------------
ERS_FILES = {
    "historical": "https://www.ers.usda.gov/media/5028/historical-monthly-price-spread-data-for-beef-pork-broilers.csv",
    "beef_recent": "https://www.ers.usda.gov/media/5020/choice-beef-values-and-spreads-and-the-all-fresh-retail-value.csv",
    "pork_recent": "https://www.ers.usda.gov/media/5026/pork-values-and-spreads.csv",
    "summary_recent": "https://www.ers.usda.gov/media/5025/summary-of-retail-prices-and-price-spreads.csv",
}
# (meat, measure, historical name, recent file, recent name)
ERS_ITEM_MAP = [
    ("Beef",    "retail",    "Choice beef retail value",     "beef_recent",    "Choice beef retail value"),
    ("Beef",    "wholesale", "Choice beef wholesale value",  "beef_recent",    "Choice beef wholesale value"),
    ("Beef",    "net_farm",  "Choice beef net farm value",   "beef_recent",    "Choice beef net farm value"),
    ("Pork",    "retail",    "Pork retail value",            "pork_recent",    "Pork retail value"),
    ("Pork",    "wholesale", "Pork wholesale value",         "pork_recent",    "Pork wholesale value"),
    ("Pork",    "net_farm",  "Pork net farm value",          "pork_recent",    "Pork net farm value"),
    ("Chicken", "retail",    "Retail broiler composite",     "summary_recent", "Retail prices or values: retail broiler composite"),
    ("Chicken", "wholesale", "Wholesale broiler composite",  None,             None),
]
ERS_CHICKEN_RECENT_RETAIL = "Retail prices or values: retail broiler composite"
ERS_CHICKEN_RECENT_SPREAD = "Price spread: wholesale-retail broiler spread"

# ---- USDA NASS (items 1.4, 1.5, D24, D25) ---------------------------------
NASS_BASE = "https://quickstats.nass.usda.gov/api"
NASS_ROW_LIMIT = 50_000
NASS_QUERIES = {
    "inventory": {
        "commodity_desc": "CATTLE", "statisticcat_desc": "INVENTORY",
        "agg_level_desc": "NATIONAL", "source_desc": "SURVEY",
        "year__GE": str(HERD_START_YEAR),
    },
    "slaughter": {
        "commodity_desc": "CATTLE", "statisticcat_desc": "SLAUGHTERED",
        "agg_level_desc": "NATIONAL", "source_desc": "SURVEY", "freq_desc": "MONTHLY",
        "year__GE": str(HERD_START_YEAR),
    },
}
HERD_SERIES = {
    "CATTLE, INCL CALVES - INVENTORY": "all_cattle",
    "CATTLE, COWS, BEEF - INVENTORY": "beef_cows",
    "CATTLE, HEIFERS, GE 500 LBS, BEEF REPLACEMENT - INVENTORY": "beef_replacement_heifers",
}
SLAUGHTER_SERIES = {
    "CATTLE, COWS, (EXCL MILK), SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN HEAD": "beef_cows_slaughtered",
    "CATTLE, HEIFERS, SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN HEAD": "heifers_slaughtered",
    "CATTLE, STEERS, SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN HEAD": "steers_slaughtered",
}

# ---- U.S. Drought Monitor (item 1.6, D26) ---------------------------------
USDM_BASE = "https://usdmdataservices.unl.edu/api"
DROUGHT_WEIGHT_YEAR = 2019
DROUGHT_COVERAGE_TARGET = 75   # percent of U.S. beef cows

# ---- Master table (D18, D27) ----------------------------------------------
MAX_FILL_GAP = 2   # months; longer gaps stay empty

# Gaps we know about and accept. Any other gap inside a column's range fails
# the checks. If ERS later fills a known gap, nothing fails.
KNOWN_GAPS = {
    "ers_chicken_retail": ["2026-01", "2026-02", "2026-03"],
    "ers_chicken_wholesale": ["2026-01", "2026-02", "2026-03"],
    "ers_chicken_spread_wholesale_to_retail": ["2026-01", "2026-02", "2026-03"],
    "ers_chicken_store_share_pct": ["2026-01", "2026-02", "2026-03"],
}

HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (meat-prices portfolio project; data download)"}
