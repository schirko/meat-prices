# Meat Price Explorer

**Why does meat cost so much now?** This project looks at U.S. retail prices for
beef, pork and chicken from 2015 to today. It shows where prices were before 2020,
how they climbed after, which real-world events lined up with each jump, and
whether today's prices are still justified by what is happening in the supply
chain.

The finished product is a Streamlit app built for a general audience, backed by a
series of Jupyter notebooks that show every step of the analysis.

> **Status:** Milestone 1 (getting the data) in progress: BLS retail prices and
> CPI done. First finding: since 2015, ground beef is up about 63%, well ahead of
> overall inflation (about 42%), while pork and chicken breast rose less than
> inflation. See
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

Details on each source, including how it was downloaded, are in
[docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).

## Project layout

```
meat-prices/
├── app/                 Streamlit app (Milestone 5)
├── data/
│   ├── raw/             Data exactly as downloaded (not committed to git)
│   └── processed/       Cleaned data the app reads
├── docs/
│   ├── MILESTONES.md    The plan, progress and what each item involves
│   ├── DECISIONS.md     Every significant decision and why we made it
│   └── DATA_SOURCES.md  Where each data set comes from and how to get it
├── notebooks/           Numbered Jupyter notebooks, one per analysis step
├── src/                 Reusable Python code shared by notebooks and app
├── .env.example         Template for API keys (copy to .env)
└── requirements.txt     Python packages
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

## Author

Scott Schirkofsky. Built as a data science portfolio project.
