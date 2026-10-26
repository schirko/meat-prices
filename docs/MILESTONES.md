# Milestones

This is the working plan for the project. Each milestone is broken into items.
Before each item starts, we write down:

1. **What we just accomplished** in the previous item
2. **What we plan to do next and why**
3. **Roadblocks** for the next item
4. **How long it will take and what's involved**

Status key: ✅ done · 🔄 in progress · ⬜ not started

---

## Milestone 0: Project setup ✅

**Goal:** a clean, documented starting point before any data work.

| Item | Status | Notes |
|---|---|---|
| 0.1 Decide project scope and main questions | ✅ | See README "Questions this project answers" |
| 0.2 Mock up the app's main page | ✅ | Sidebar filters, price tiles, event chart, "who gets the dollar", verdict. Design mockup kept outside the repo |
| 0.3 Create folder structure, README, docs, `.gitignore`, `requirements.txt` | ✅ | |

---

## Milestone 1: Get the data ⬜

**Goal:** download every data set into `data/raw/`, with a notebook that shows
exactly how, so anyone can repeat it.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 1.1 BLS retail meat prices | ⬜ | `01_bls_retail_prices.ipynb` | Register for a free BLS API key, find the right series IDs for beef, pork and chicken, pull monthly prices 2015 to now, save raw data |
| 1.2 BLS Consumer Price Index | ⬜ | same notebook | Pull CPI (all items) for the same months, used later for inflation adjustment |
| 1.3 USDA ERS meat price spreads | ⬜ | `02_ers_price_spreads.ipynb` | Download the ERS spreadsheet, find the beef, pork and broiler tables, reshape to one tidy table |
| 1.4 USDA NASS cattle inventory | ⬜ | `03_nass_cattle_inventory.ipynb` | Register for a free NASS API key, pull January 1 cattle inventory by year |

---

## Milestone 2: Clean and explore ⬜

**Goal:** one tidy monthly data set, and a first look at the patterns.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 2.1 Combine and clean | ⬜ | `04_clean_and_combine.ipynb` | Match dates across sources, handle missing months, standardize units (cents vs dollars, per pound) |
| 2.2 Exploratory charts | ⬜ | `05_explore.ipynb` | First charts of each meat, early observations |

---

## Milestone 3: Event timeline ⬜

**Goal:** a cited, dated table of events that can go on charts and into
statistical tests.

| Item | Status | Notebook / file | What's involved |
|---|---|---|---|
| 3.1 Research and record events | ⬜ | `data/processed/events.csv` | Date, event, which meats it affected, source link |
| 3.2 Overlay events on prices | ⬜ | `06_events.ipynb` | Annotated charts; first visual check of which events line up with jumps |

---

## Milestone 4: Analysis ⬜

**Goal:** answer "did the events matter?" and "are prices justified?" with
evidence.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 4.1 Inflation-adjusted prices | ⬜ | `07_inflation_adjusted.ipynb` | Convert prices to today's dollars using CPI; compare meat to overall inflation |
| 4.2 Who gets the dollar | ⬜ | `08_price_spreads.ipynb` | Farm, packer and retail shares over time |
| 4.3 Did prices shift at each event? | ⬜ | `09_event_tests.ipynb` | Changepoint detection and/or interrupted time series |
| 4.4 Supply side | ⬜ | `10_supply.ipynb` | Herd size vs. beef price |
| 4.5 Verdict | ⬜ | `11_verdict.ipynb` | Pull findings together into plain-language conclusions |

---

## Milestone 5: Streamlit app ⬜

**Goal:** the main page from the mockup, running on real data.

| Item | Status | What's involved |
|---|---|---|
| 5.1 App skeleton and sidebar | ⬜ | Page layout, load processed data; sidebar with meat selector (beef, pork, chicken, all meats), year selector ("All years" or one year), nominal vs inflation-adjusted, event markers on/off |
| 5.2 Price tiles and all-years view | ⬜ | `st.metric` tiles for the selected meat, full price history chart with event markers (see D11) |
| 5.2b Single-year view | ⬜ | When one year is picked: month-by-month chart, change from the year before, events that happened that year |
| 5.2c "All meats" view | ⬜ | All three meats on one chart as an index (Jan 2015 = 100), for all years or one year (see D13) |
| 5.3 "Who gets the dollar" and verdict sections | ⬜ | Stacked bars, findings, explanations |
| 5.4 Methods and data page | ⬜ | How everything was done, with source links |

---

## Milestone 6: Publish ⬜

| Item | Status | What's involved |
|---|---|---|
| 6.1 Deploy | ⬜ | Streamlit Community Cloud (free), from the public GitHub repo; app reads committed processed data, no API keys needed (see D12) |
| 6.2 Portfolio polish | ⬜ | README screenshots, link from GitHub profile and résumé |

---

## Progress log

Newest first. One entry per finished item.

### 2026-10-26: Design decisions D12 and D13
- **Done:** recorded the public repo / Streamlit Cloud plan (D12) and the
  "All meats" indexed comparison (D13); added item 5.2c.
- **Next:** item 1.1, once the BLS API key is activated.

### 2026-10-26: Design change, meat selector and year drill-down
- **Done:** recorded decision D11 (pick one meat, see all years, then isolate
  any year) and added the single-year view to Milestone 5.
- **Next:** still item 1.1. Monthly data supports both views.

### 2026-10-26: Item 0.3, project structure and docs
- **Done:** created the folder layout, README, this milestone plan, the decision
  log and data sources page, `.gitignore`, `requirements.txt` and `.env.example`.
- **Next:** item 1.1, BLS retail meat prices.
