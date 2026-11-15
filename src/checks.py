"""Data checks on the master table (D29).

Each check returns a list of problems (empty = passed). The same checks run in
two places:
- tests/test_master.py, on the committed data, every time the tests run;
- src/refresh.py, on freshly built data, before it replaces the current files.
"""
import pandas as pd

from . import config

MEATS = ["beef", "pork", "chicken"]

# Sensible ranges: wide enough for real price swings, narrow enough to catch unit errors
# (e.g. cents read as dollars, or a percent column holding cents as in D23).
RANGES = {
    "_price": (0.5, 30.0),            # $ per lb
    "_price_real": (0.5, 30.0),
    "_pct": (-20.0, 100.0),           # shares can dip slightly below 0 in rare months
    "ers_": (0.0, 3000.0),            # cents per lb (non-share ERS columns)
    "herd_": (1_000_000, 200_000_000),
    "slaughter_beef_cows_slaughtered": (50_000, 1_000_000),
    "slaughter_heifers_slaughtered": (50_000, 2_000_000),
    "slaughter_steers_slaughtered": (100_000, 3_000_000),
    "slaughter_beef_cows_slaughtered_12mo": (1_000_000, 8_000_000),
    "drought_cattle_d2_plus_pct": (0.0, 100.0),
    "drought_conus_d2_plus_pct": (0.0, 100.0),
    "drought_cattle_dsci": (0.0, 500.0),
    "drought_conus_dsci": (0.0, 500.0),
    "cpi_all_items": (100.0, 1000.0),
    "_2015eq100": (30.0, 400.0),
}


def _range_for(col):
    """Exact column name first, then by ending, then by prefix. None = no range (a check failure)."""
    if col in RANGES:
        return RANGES[col]
    for ending in ["_price_real", "_price", "_pct", "_2015eq100"]:
        if col.endswith(ending):
            return RANGES[ending]
    for prefix in ["ers_", "herd_"]:
        if col.startswith(prefix):
            return RANGES[prefix]
    return None


def check_months(m):
    """One row per month, in order, starting January 2010, no missing months."""
    problems = []
    if not m.index.is_unique:
        problems.append("duplicate months")
    if m.index.min() != pd.Timestamp(f"{config.HERD_START_YEAR}-01-01"):
        problems.append(f"table starts {m.index.min():%Y-%m}, expected {config.HERD_START_YEAR}-01")
    expected = pd.date_range(m.index.min(), m.index.max(), freq="MS")
    if len(m) != len(expected) or not (m.index == expected).all():
        problems.append("months are missing or out of order")
    return problems


def check_gaps(m):
    """No empty months inside any column's range, except the known gaps."""
    problems = []
    for col in m.columns.drop("filled_columns"):
        s = m[col]
        first, last = s.first_valid_index(), s.last_valid_index()
        if first is None:
            problems.append(f"{col}: no data at all")
            continue
        empty = s.loc[first:last].isna()
        gaps = {d.strftime("%Y-%m") for d in s.loc[first:last][empty].index}
        unexpected = sorted(gaps - set(config.KNOWN_GAPS.get(col, [])))
        if unexpected:
            problems.append(f"{col}: unexpected empty months {unexpected}")
    return problems


def check_start_dates(m):
    """Prices, ERS and grocery columns start in 2015; herd, slaughter and drought in 2010 (D27)."""
    problems = []
    for col in m.columns.drop("filled_columns"):
        first = m[col].first_valid_index()
        if first is None:
            continue
        early = col.startswith(("herd_", "slaughter_", "drought_"))
        expected_year = config.HERD_START_YEAR if early else config.PRICE_START_YEAR
        # 12-month rolling total needs 11 earlier months
        if col == "slaughter_beef_cows_slaughtered_12mo":
            ok = first == pd.Timestamp(f"{expected_year}-12-01")
        else:
            ok = first == pd.Timestamp(f"{expected_year}-01-01")
        if not ok:
            problems.append(f"{col}: starts {first:%Y-%m}, expected {expected_year}")
    return problems


def check_ranges(m):
    """Every value falls in a sensible range for its units."""
    problems = []
    for col in m.columns.drop("filled_columns"):
        rng = _range_for(col)
        if rng is None:
            problems.append(f"{col}: no range defined")
            continue
        s = m[col].dropna()
        bad = s[(s < rng[0]) | (s > rng[1])]
        if len(bad):
            problems.append(f"{col}: {len(bad)} value(s) outside {rng}, e.g. {bad.index[0]:%Y-%m} = {bad.iloc[0]:.2f}")
    return problems


def check_ers_arithmetic(m, tol=0.05):
    """Spreads and shares agree with the values they come from (D22)."""
    problems = []
    for meat in MEATS:
        p = f"ers_{meat}_"
        spread = m[p + "retail"] - m[p + "wholesale"] - m[p + "spread_wholesale_to_retail"]
        if spread.abs().max() > tol:
            problems.append(f"{meat}: retail - wholesale != wholesale-to-retail spread")
        if p + "farmer_share_pct" in m:
            total = m[p + "farmer_share_pct"] + m[p + "packer_share_pct"] + m[p + "store_share_pct"]
            off = (total - 100).abs().dropna()
            if len(off) and off.max() > tol:
                problems.append(f"{meat}: farm + packer + store shares don't add to 100 (off by {off.max():.3f})")
    return problems


def check_real_prices(m, tol=1e-6):
    """Real prices equal nominal prices in the base (latest) month, and are price x CPI ratio elsewhere."""
    problems = []
    base = m["cpi_all_items"].last_valid_index()
    for meat in MEATS:
        nominal, real = m[f"{meat}_price"], m[f"{meat}_price_real"]
        if abs(nominal[base] - real[base]) > 1e-3:
            problems.append(f"{meat}: real price differs from nominal in the base month {base:%Y-%m}")
        expected = nominal * m.loc[base, "cpi_all_items"] / m["cpi_all_items"]
        if ((expected - real).abs() > 1e-3).any():
            problems.append(f"{meat}: real price doesn't match price x (base CPI / CPI)")
    return problems


def check_filled(m, max_months=6):
    """Filled values are flagged, name real columns, and stay rare (D18)."""
    problems = []
    flagged = m.loc[m["filled_columns"].fillna("") != "", "filled_columns"]
    for date, text in flagged.items():
        for col in text.split(";"):
            if col not in m.columns:
                problems.append(f"{date:%Y-%m}: filled_columns names unknown column '{col}'")
    if len(flagged) > max_months:
        problems.append(f"{len(flagged)} months have filled values (more than {max_months}); check the source data")
    return problems


def check_dictionary(m, dictionary_text):
    """Every column is documented in the data dictionary, and nothing extra is."""
    documented = set()
    for line in dictionary_text.splitlines():
        if line.startswith("| `"):
            documented.add(line.split("`")[1])
    cols = set(m.columns) | {"date"}
    problems = [f"not in data dictionary: {c}" for c in sorted(cols - documented)]
    problems += [f"in data dictionary but not in table: {c}" for c in sorted(documented - cols)]
    return problems


ALL_CHECKS = [check_months, check_gaps, check_start_dates, check_ranges,
              check_ers_arithmetic, check_real_prices, check_filled]


def run_all(master, dictionary_text=None):
    """Run every check; return {check name: [problems]} for the checks that failed."""
    results = {fn.__name__: fn(master) for fn in ALL_CHECKS}
    if dictionary_text is not None:
        results["check_dictionary"] = check_dictionary(master, dictionary_text)
    return {name: probs for name, probs in results.items() if probs}


def load_master(path):
    m = pd.read_csv(path, parse_dates=["date"]).set_index("date")
    m["filled_columns"] = m["filled_columns"].fillna("")
    return m
