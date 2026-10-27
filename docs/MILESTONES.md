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

## Milestone 1: Get the data 🔄

**Goal:** download every data set into `data/raw/`, with a notebook that shows
exactly how, so anyone can repeat it.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 1.1 BLS retail meat prices | ✅ | `01_bls_retail_prices.ipynb` | Register for a free BLS API key, find the right series IDs for beef, pork and chicken, pull monthly prices 2015 to now, save raw data |
| 1.2 BLS Consumer Price Index | ✅ | same notebook | Pull CPI (all items) for the same months, used later for inflation adjustment |
| 1.3 USDA ERS meat price spreads | ✅ | `02_ers_price_spreads.ipynb` | Part 1: download the historical file plus the three recent files (CSV), standardize and take an inventory of data items. Part 2: choose items, match names across files, check overlap, combine 2015 to now (D21) |
| 1.4 USDA NASS cattle inventory | 🔄 | `03_nass_cattle_inventory.ipynb` | Register for a free NASS API key, pull January 1 cattle inventory by year from 2010 (D24). Part 1: download and inventory; Part 2: chosen series, coverage, first chart |
| 1.5 Beef cow slaughter | 🔄 | same notebook | Pull monthly beef cow slaughter from NASS. Ranchers selling off cows during drought shows up here first (see D17) |
| 1.6 Drought data | ⬜ | `04_drought.ipynb` | Weekly U.S. Drought Monitor data for the main cattle states, and the share of cattle in drought areas (see D17) |
| 1.7 Grocery category CPIs (context) | ⬜ | `05_grocery_categories.ipynb` | BLS CPI indexes for food at home and its categories (produce, cereals and bakery, dairy, beverages, other/packaged foods, meats). Same API and key as notebook 01 (see D19) |

---

## Milestone 2: Clean and explore ⬜

**Goal:** one tidy monthly data set, and a first look at the patterns.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 2.1 Combine and clean | ⬜ | `06_clean_and_combine.ipynb` | Match dates across sources, fill single missing months with the neighbor average (D18), standardize units (cents vs dollars, per pound) |
| 2.2 Exploratory charts | ⬜ | `07_explore.ipynb` | First charts of each meat, early observations |

---

## Milestone 3: Event timeline ⬜

**Goal:** a cited, dated table of events that can go on charts and into
statistical tests.

| Item | Status | Notebook / file | What's involved |
|---|---|---|---|
| 3.1 Research and record events | ⬜ | `data/processed/events.csv` | Date, event, which meats it affected, source link. Candidates to check: COVID plant shutdowns (2020), JBS cyberattack (2021), drought years (D17), the 2022 chicken breast spike (feed costs? demand? bird flu?), 2022 food plant fires (widely given as the reason chicken prices rose; fact-checkers found them no more common than usual; test against the price data), Colorado bird-flu culls (2022, 2024) and cage-free egg law (2025) (these involve egg-laying hens; check whether they show up in meat-chicken prices at all), Mexican cattle import suspensions, screwworm (2026) |
| 3.2 Overlay events on prices | ⬜ | `08_events.ipynb` | Annotated charts; first visual check of which events line up with jumps |

---

## Milestone 4: Analysis ⬜

**Goal:** answer "did the events matter?" and "are prices justified?" with
evidence.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 4.1 Inflation-adjusted prices | ⬜ | `09_inflation_adjusted.ipynb` | Convert prices to today's dollars using CPI; compare meat to overall inflation |
| 4.2 Who gets the dollar | ⬜ | `10_price_spreads.ipynb` | Farm, packer and retail shares over time |
| 4.3 Did prices shift at each event? | ⬜ | `11_event_tests.ipynb` | Changepoint detection and/or interrupted time series |
| 4.4 Supply side: drought → herd → price | ⬜ | `12_supply.ipynb` | Trace the chain in D17: did drought come first, then cow sell-offs, then a smaller herd, then higher beef prices? Measure the time lag between each step |
| 4.5 Verdict | ⬜ | `13_verdict.ipynb` | Pull findings together into plain-language conclusions |

---

## Milestone 5: Streamlit app ⬜

**Goal:** the main page from the mockup, running on real data.

| Item | Status | What's involved |
|---|---|---|
| 5.1 App skeleton and sidebar | ⬜ | Page layout, load processed data; sidebar with meat selector (beef, pork, chicken, all meats), year selector ("All years" or one year), nominal vs inflation-adjusted, event markers on/off |
| 5.2 Price tiles and all-years view | ⬜ | `st.metric` tiles for the selected meat, full price history chart with event markers (see D11) |
| 5.2b Single-year view | ⬜ | When one year is picked: month-by-month chart, change from the year before, events that happened that year |
| 5.2c "All meats" view | ⬜ | All three meats on one chart as an index (Jan 2015 = 100), for all years or one year (see D13) |
| 5.2d "Meat vs. the rest of the grocery cart" | ⬜ | Indexed chart (2015 = 100) of the chosen meats against grocery categories (see D19) |
| 5.3 "Who gets the dollar" and verdict sections | ⬜ | Stacked bars, findings, explanations |
| 5.4 Methods and data page | ⬜ | How everything was done, with source links. Includes a plain-language "Who publishes this data" section on BLS, ERS, NASS and AMS, and a "Key terms" section on the three price stages and spreads (both from `docs/DATA_SOURCES.md`) |

---

## Milestone 6: Publish ⬜

| Item | Status | What's involved |
|---|---|---|
| 6.1 Deploy | ⬜ | Streamlit Community Cloud (free), from the public GitHub repo; app reads committed processed data, no API keys needed (see D12) |
| 6.2 Portfolio polish | ⬜ | README screenshots, link from GitHub profile and résumé |

---

## Progress log

Newest first. One entry per finished item.

### 2026-10-26: Item 1.3 started
- **Done:** notebook 02 Part 1 written: downloads four ERS CSV files,
  standardizes their three slightly different layouts, and lists every data item
  with units and date range (D21).
- **Next:** Scott runs Part 1; we review the inventory together and choose
  which items to keep, then write Part 2.
- **Bug found and fixed (from Scott's question about the inventory):** beef
  retail value appeared to be missing 10 of 24 recent months. The months
  weren't missing: ERS writes values of 1,000 or more with a thousands comma
  (`1,011.3`), which the loader turned into missing values. The loader now
  strips the comma first.

### 2026-10-26: Item 1.3, Part 2 written
- **Done:** notebook 02 Part 2 maps three values per meat across files,
  confirms the historical and recent files agree (within 0.05 cents), combines
  them, calculates spreads and shares (D22), checks them against ERS's published
  figures, and saves `data/processed/ers_price_spreads_monthly.csv`.
- **Found:** a mislabeled column in ERS's recent pork file (percent stored as
  cents), handled by using our calculation (D23). Chicken's 2025 units label
  change is only a relabel. Chicken has no data for January–March 2026.
- **First finding:** beef's farmer share fell from about 52% (2015) to 43%
  (2019), then rose to about 54% (2025), while the packer share shrank to under
  5%. Consistent with scarce cattle (D17).
- **Next:** Scott runs notebook 02; then item 1.4/1.5, NASS cattle inventory
  and cow slaughter.

### 2026-10-26: Docs, key terms; items 1.4 and 1.5 started
- **Done:** added "Key terms: the three price stages" to DATA_SOURCES.md and the
  README ("three values per meat" = farm, wholesale and retail for each meat,
  not three data sources). NASS API key registered and stored in `.env`.
  Notebook 03 Part 1 written: checks row counts, downloads cattle inventory and
  monthly cattle slaughter from 2010 (D24), and lists every series.
- **Next:** Scott runs notebook 02 Part 2 and notebook 03 Part 1; we choose the
  herd and cow slaughter series together.

### 2026-10-26: Item 1.3 complete
- **Done:** notebook 02 run in full on Scott's machine. All results match the
  test run: files agree in the overlap, 10 of 11 checks within 0.1, the pork
  column error confirmed (D23), coverage complete for beef and pork (141
  months), chicken missing Jan–Mar 2026 as expected.
  `data/processed/ers_price_spreads_monthly.csv` saved (2,808 rows).
- **Next:** notebook 03 Part 1 (NASS).

### 2026-10-26: Items 1.4 and 1.5, Part 2 written
- **Done:** chose six NASS series together (D25). Notebook 03 Part 2 builds the
  January 1 herd table and the monthly slaughter table (with heifer share and
  12-month totals), checks coverage (complete), charts herd, slaughter and the
  ground beef price together, and saves `nass_herd_jan1.csv` and
  `nass_slaughter_monthly.csv`.
- **First finding:** the beef cow herd fell from 31.6 million (2019) to 27.6
  million (2026), down 13%. Beef cow slaughter peaked in 2022 at 13.2% of the
  herd, larger than the 2011 drought sell-off (12.3%). Heifer share of slaughter
  was near 40% in 2022–2024, the highest in the data, and replacement heifers
  remain near their low, so no rebuild yet. Caveat: the decline began around
  2018 as the normal cycle turned; the drought accelerated it.
- **Next:** Scott runs notebook 03 in full; then item 1.6, drought data.

### 2026-10-26: Items 1.1 and 1.2 complete
- **Done:** notebook 01 downloads BLS prices and CPI (Jan 2015 to Sep 2026),
  checks coverage, lists missing months and compares each candidate with
  inflation. Chose one series per meat (D15). Found October 2025 missing from
  every series, to be filled with a neighbor average (D18).
- **First finding:** since the 2015 average, ground beef is up about 63%,
  overall prices (CPI) about 42%, chicken breast about 23% and pork chops about
  9%. Beef is the only meat that clearly outran inflation.
- **Next:** item 1.3, USDA ERS meat price spreads.

### 2026-10-26: Items 1.1 and 1.2 started
- **Done:** BLS API key registered and stored in `.env`. Notebook
  `01_bls_retail_prices.ipynb` written: downloads six candidate meat series plus
  CPI, saves the raw response, builds a tidy table, checks coverage and charts
  the candidates. Decisions D14 (matplotlib in notebooks) and D15 (pending).
- **Next:** Scott runs the notebook; together we review the results, fill in
  "What it means", and choose one series per meat (D15).

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
