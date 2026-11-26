"""Tests of the pipeline's building blocks, using small made-up data (D29).

Each test below recreates a real problem we hit by hand in Milestone 1, so it
can't come back unnoticed.
"""
import numpy as np
import pandas as pd

from src import checks, config, ers, master


def months(n, start="2025-01-01"):
    return pd.date_range(start, periods=n, freq="MS")


# ---- Filling gaps (D18) -----------------------------------------------------

def test_single_gap_filled_with_neighbor_average():
    df = pd.DataFrame({"x": [1.0, np.nan, 3.0]}, index=months(3))
    filled, log = master.fill_short_gaps(df)
    assert filled["x"].iloc[1] == 2.0
    assert log == [(months(3)[1], "x")]


def test_long_gap_left_empty():
    df = pd.DataFrame({"x": [1.0, np.nan, np.nan, np.nan, 5.0]}, index=months(5))
    filled, log = master.fill_short_gaps(df)
    assert filled["x"].isna().sum() == 3 and log == []


def test_gap_at_end_not_filled():
    """No value after the gap: can't interpolate, so it stays empty."""
    df = pd.DataFrame({"x": [1.0, 2.0, np.nan]}, index=months(3))
    filled, log = master.fill_short_gaps(df)
    assert np.isnan(filled["x"].iloc[2]) and log == []


# ---- ERS loading: the thousands-comma bug -----------------------------------

def test_ers_values_with_thousands_comma(tmp_path):
    """ERS writes 1,011.3; it must load as 1011.3, not as missing (first notebook 02 run)."""
    csv = tmp_path / "beef_recent.csv"
    csv.write_text('Year,Period,Period_Number,Data_Item,Value,Units\n'
                   '2025,October,10,Choice beef retail value,"1,011.3",Cents\n'
                   '2025,Annual,17,Choice beef retail value,"1,000.0",Cents\n', encoding="utf-8")
    df = ers.load_file(csv, "beef_recent")
    assert len(df) == 1                       # annual row dropped
    assert df["value"].iloc[0] == 1011.3


def test_ers_keeps_months_that_rolled_off_the_recent_file(tmp_path):
    """ERS's recent file drops its oldest month each time a new one is added. In the
    November 2026 refresh, chicken's April 2026 fell off and the refresh stopped (D44).
    Earlier downloads must fill that month, and the newest download must win on overlap."""
    header = "Year,Month,Month_Number,Data_Item,Value,Units\n"
    item = "Retail prices or values: retail broiler composite"
    old = tmp_path / "ers_20261026"; old.mkdir()
    new = tmp_path / "ers_20261124"; new.mkdir()
    (old / "summary_recent.csv").write_text(header + f"2026,April,4,{item},238.9,Cents\n"
                                            f"2026,May,5,{item},240.0,Cents\n", encoding="utf-8")
    (new / "summary_recent.csv").write_text(header + f"2026,May,5,{item},243.9,Cents\n"
                                            f"2026,October,10,{item},241.8,Cents\n", encoding="utf-8")
    df = ers.load_with_earlier(new, "summary_recent").set_index("date")["value"]
    assert df[pd.Timestamp("2026-04-01")] == 238.9   # kept from the earlier download
    assert df[pd.Timestamp("2026-05-01")] == 243.9   # the newest download wins (revision)
    assert len(df) == 3
    # Rebuilding the older download doesn't pick up the newer one
    assert len(ers.load_with_earlier(old, "summary_recent")) == 2


# ---- The checks catch real problems -----------------------------------------

def good_master():
    """A tiny master table that passes the arithmetic and real-price checks."""
    idx = months(3)
    m = pd.DataFrame(index=idx)
    m["cpi_all_items"] = [300.0, 310.0, 320.0]
    for meat in ["beef", "pork", "chicken"]:
        m[f"{meat}_price"] = [5.0, 5.5, 6.0]
        m[f"{meat}_price_real"] = m[f"{meat}_price"] * 320.0 / m["cpi_all_items"]
        m[f"ers_{meat}_retail"] = 900.0
        m[f"ers_{meat}_wholesale"] = 500.0
        m[f"ers_{meat}_spread_wholesale_to_retail"] = 400.0
    for meat in ["beef", "pork"]:
        m[f"ers_{meat}_farmer_share_pct"] = 40.0
        m[f"ers_{meat}_packer_share_pct"] = 15.0
        m[f"ers_{meat}_store_share_pct"] = 45.0
    m["filled_columns"] = ""
    return m


def test_good_table_passes():
    m = good_master()
    assert checks.check_ers_arithmetic(m) == []
    assert checks.check_real_prices(m) == []


def test_shares_not_adding_to_100_caught():
    m = good_master()
    m["ers_beef_store_share_pct"] = 50.0
    assert checks.check_ers_arithmetic(m)


def test_percent_stored_as_cents_caught():
    """D23: ERS's pork file held a percent (16.2) where cents (79.9) belonged. A spread
    that doesn't match retail - wholesale must be caught."""
    m = good_master()
    m["ers_pork_spread_wholesale_to_retail"] = 16.2
    assert checks.check_ers_arithmetic(m)


def test_unexpected_gap_caught():
    m = pd.DataFrame({"beef_price": [5.0, np.nan, 6.0], "filled_columns": ""}, index=months(3))
    assert checks.check_gaps(m)


def test_known_gap_allowed():
    m = pd.DataFrame({"ers_chicken_retail": [240.0, np.nan, np.nan, np.nan, 245.0], "filled_columns": ""},
                     index=months(5, "2025-12-01"))
    assert checks.check_gaps(m) == []


def test_cents_read_as_dollars_caught():
    m = pd.DataFrame({"beef_price": [679.0], "filled_columns": ""}, index=months(1))
    assert checks.check_ranges(m)


def test_missing_month_caught():
    idx = pd.DatetimeIndex(["2010-01-01", "2010-03-01"])
    m = pd.DataFrame({"filled_columns": ["", ""]}, index=idx)
    assert checks.check_months(m)


def test_undocumented_column_caught():
    m = pd.DataFrame({"beef_price": [5.0]}, index=months(1))
    assert checks.check_dictionary(m, "| `date` | x |\n")
