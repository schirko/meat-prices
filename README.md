# Meat Price Explorer

**Why does meat cost so much now?** This project looks at U.S. retail prices for
beef, pork and chicken from 2015 to today. It shows where prices were before 2020,
how they climbed after, which real-world events lined up with each jump, and
whether today's prices are still justified by what is happening in the supply
chain.

The finished product is a Streamlit app built for a general audience, backed by a
series of Jupyter notebooks that show every step of the analysis.

> **Status:** Milestone 1 (getting the data) complete; Milestone 2 (clean and
> combine) next. Early findings:
> - Since 2015, ground beef is up about 63%, well ahead of overall inflation
>   (about 42%); pork and chicken breast rose less than inflation, and groceries
>   as a whole (+33%) rose less than prices in general.
> - The U.S. beef cow herd fell 13% from its 2019 peak to 2026 after a drought-
>   driven sell-off that peaked in 2022; ranchers' share of the retail beef
>   dollar rose to about 54% in 2025.
> - Beef broke away from every other grocery category from 2024, as the herd
>   reached its low.
>
> See
> [docs/MILESTONES.md](docs/MILESTONES.md) for the full plan and progress.

---

## Questions this project answers

1. **Where were prices in 2015, and where are they now?** Per-pound retail prices
   for each meat, in dollars at the time and adjusted for inflation.
2. **What happened along the way?** A dated timeline of events (plant shutdowns,
   cyberattack, drought, import suspensions, disease) laid over the price history.
3. **Did those events actually move prices?** Statistical tests for whether
   prices shifted at each event, rather than just eyeballing a chart.
4. **Who got the extra money?** How each retail dollar splits between the
   rancher, the meatpacker and the grocery store, and how that split changed.
5. **Are today's prices still justified?** A plain-language verdict based on
   supply (herd size), inflation and margins.

## Data sources (all free, all public)

| Data | Source | Used for |
|---|---|---|
| Average retail prices per pound | U.S. Bureau of Labor Statistics (BLS) | The main price history |
| Consumer Price Index (CPI) | BLS | Adjusting for inflation |
| Meat price spreads (farm, wholesale, retail) | USDA Economic Research Service (ERS) | Who gets each dollar |
| Cattle inventory | USDA National Agricultural Statistics Service (NASS) | Supply side |
| Event timeline | Curated from news and USDA reports, with citations | Annotating charts, testing events |

**Key terms.** The price spreads follow one pound of meat through three stages:
the **farm** (what the rancher or hog farmer is paid), **wholesale** (what the
meatpacker gets) and **retail** (what shoppers pay). The gaps between them are
the spreads, and each stage's share of the retail price shows who gets each
dollar. Chicken has only the wholesale and retail stages.

**Who are these agencies?** BLS (Bureau of Labor Statistics) is part of the
Department of Labor and measures prices and inflation. ERS (Economic Research
Service) and NASS (National Agricultural Statistics Service) are part of the U.S.
Department of Agriculture: ERS is its research agency, and NASS runs its farm
surveys, including cattle counts.

Details on each agency and source, including how each data set was downloaded,
are in [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md). Everything is combined into
one monthly table, `data/processed/master_monthly.csv`, described column by
column in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).

## Project layout

```
meat-prices/
├── .github/workflows/   Runs the tests on every push (GitHub Actions)
├── app/                 Streamlit app (Milestone 5)
├── data/
│   ├── raw/             Data exactly as downloaded (not committed to git)
│   └── processed/       Cleaned data the app reads, plus REFRESH_REPORT.md
├── deploy/              Monthly refresh script for the server
├── docs/
│   ├── MILESTONES.md    The plan, progress and what each item involves
│   ├── DECISIONS.md     Every significant decision and why we made it
│   ├── DATA_SOURCES.md  Where each data set comes from and how to get it
│   └── DATA_DICTIONARY.md  Every column in the master table (generated)
├── notebooks/           Numbered Jupyter notebooks, one per analysis step
├── src/                 The data pipeline: download, build, check, publish
├── tests/               Data and pipeline tests (pytest)
├── .env.example         Template for API keys (copy to .env)
├── requirements.txt     Python packages (full development setup)
└── requirements-test.txt  Just what the pipeline and tests need
```

## How the notebooks are written

Every notebook follows the same pattern so a reader can follow along without
running the code:

- **What we're looking for:** the question this step answers
- **Code**, then **its result**
- **How to read it:** what the chart or table shows
- **What it means:** the plain-language finding
- **What's next and why:** how this step leads to the next one

## Setup

```bash
# 1. Activate the virtual environment (Windows)
.venv\Scripts\activate

# 2. Install packages
pip install -r requirements.txt

# 3. Add API keys
copy .env.example .env
# then edit .env and paste in your keys
```

## Refreshing and testing the data

Everything in `data/processed/` can be rebuilt from the official sources with one
command. New data only replaces the current files if every data check passes, and
each run writes `data/processed/REFRESH_REPORT.md` explaining what changed.

```bash
python -m src.refresh                      # download everything, rebuild, check, publish
python -m src.refresh --offline            # rebuild from the saved raw files (no downloads)
python -m src.refresh --offline --dry-run  # build and check only; change nothing
pytest                                     # run the data and pipeline tests
```

The tests check, among other things, that there is one row per month with no
unexpected gaps, that values are in sensible ranges, that the farm, packer and
store shares add up to 100%, and that every column is documented. They also
recreate the data problems found during development (thousands commas in USDA
files, a mislabeled USDA column, a month missing during the 2025 government
shutdown), so those can't come back unnoticed. GitHub Actions runs the tests on
every push, and the server runs the refresh monthly.

## Author

Scott Schirkofsky. Built as a data science portfolio project.
