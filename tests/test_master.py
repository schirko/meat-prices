"""Checks on the committed data (D29). Run with:  pytest

These read only files committed to git, so they need no API keys and run the same
on Scott's computer, on GitHub Actions, and on the VPS.
"""
import pandas as pd
import pytest

from src import checks, config

MASTER = config.PROCESSED_DIR / "master_monthly.csv"
DICTIONARY = config.DOCS_DIR / "DATA_DICTIONARY.md"


@pytest.fixture(scope="module")
def master():
    return checks.load_master(MASTER)


# One test per check, so a failure names exactly what's wrong
@pytest.mark.parametrize("check", checks.ALL_CHECKS, ids=lambda f: f.__name__)
def test_master_check(master, check):
    problems = check(master)
    assert not problems, "\n".join(problems)


def test_every_column_documented(master):
    problems = checks.check_dictionary(master, DICTIONARY.read_text(encoding="utf-8"))
    assert not problems, "\n".join(problems)


def test_only_october_2025_filled(master):
    """The only month filled so far is the government-shutdown month (D18)."""
    filled = master.index[master["filled_columns"] != ""].strftime("%Y-%m").tolist()
    assert filled == ["2025-10"]


def test_master_matches_ers_file(master):
    """The master table's ERS columns are exactly the processed ERS file (no drift between files)."""
    ers = pd.read_csv(config.PROCESSED_DIR / "ers_price_spreads_monthly.csv", parse_dates=["date"])
    for (meat, measure), g in ers.groupby(["meat", "measure"]):
        col = f"ers_{meat.lower()}_{measure}"
        joined = g.set_index("date")["value"]
        diff = (master.loc[joined.index, col] - joined).abs().max()
        assert diff < 1e-3, f"{col} differs from the ERS file by {diff}"


def test_events_file():
    """events.csv follows the D28 format: required fields, valid dates and categories, sources."""
    ev = pd.read_csv(config.PROCESSED_DIR / "events.csv", dtype=str, keep_default_na=False)
    required = ["event_id", "start_date", "end_date", "date_precision", "event", "category", "meats",
                "expected_effect", "popular_explanation", "source_name", "source_url", "notes"]
    assert list(ev.columns) == required
    assert ev["event_id"].is_unique
    start = pd.to_datetime(ev["start_date"], errors="coerce")
    assert start.notna().all(), "every event needs a start date"
    end = pd.to_datetime(ev["end_date"].replace("", None), errors="coerce")
    assert ((end.isna()) | (end >= start)).all(), "end date before start date"
    assert set(ev["date_precision"]) <= {"day", "month"}
    assert set(ev["category"]) <= {"weather", "packing_capacity", "trade", "disease",
                                   "feed_costs", "data", "popular_claim"}
    assert set(ev["popular_explanation"]) <= {"yes", "no"}
    for meats in ev["meats"]:
        assert set(meats.split(";")) <= {"beef", "pork", "chicken"}, meats
    assert (ev["source_name"] != "").all(), "every event needs a source"
