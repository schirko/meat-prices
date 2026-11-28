# Milestones

This is the working plan for the project. Each milestone is broken into items.
Before each item starts, we write down:

1. **What we just accomplished** in the previous item
2. **What we plan to do next and why**
3. **Roadblocks** for the next item
4. **How long it will take and what's involved**

Status key: ✅ done · 🔄 in progress · ⬜ not started · ⏸ deferred

---

## Milestone 0: Project setup ✅

**Goal:** a clean, documented starting point before any data work.

| Item | Status | Notes |
|---|---|---|
| 0.1 Decide project scope and main questions | ✅ | See README "Questions this project answers" |
| 0.2 Mock up the app's main page | ✅ | Sidebar filters, price tiles, event chart, "who gets the dollar", verdict. Design mockup kept outside the repo |
| 0.3 Create folder structure, README, docs, `.gitignore`, `requirements.txt` | ✅ | |

---

## Milestone 1: Get the data ✅

**Goal:** download every data set into `data/raw/`, with a notebook that shows
exactly how, so anyone can repeat it.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 1.1 BLS retail meat prices | ✅ | `01_bls_retail_prices.ipynb` | Register for a free BLS API key, find the right series IDs for beef, pork and chicken, pull monthly prices 2015 to now, save raw data |
| 1.2 BLS Consumer Price Index | ✅ | same notebook | Pull CPI (all items) for the same months, used later for inflation adjustment |
| 1.3 USDA ERS meat price spreads | ✅ | `02_ers_price_spreads.ipynb` | Part 1: download the historical file plus the three recent files (CSV), standardize and take an inventory of data items. Part 2: choose items, match names across files, check overlap, combine 2015 to now (D21) |
| 1.4 USDA NASS cattle inventory | ✅ | `03_nass_cattle_inventory.ipynb` | Register for a free NASS API key, pull January 1 cattle inventory by year from 2010 (D24). Part 1: download and inventory; Part 2: chosen series, coverage, first chart |
| 1.5 Beef cow slaughter | ✅ | same notebook | Pull monthly beef cow slaughter from NASS. Ranchers selling off cows during drought shows up here first (see D17) |
| 1.6 Drought data | ✅ | `04_drought.ipynb` | Weekly U.S. Drought Monitor data for the states holding 75% of beef cows, weighted by 2019 beef cows; % in severe drought or worse and DSCI, monthly from 2010 (D26) |
| 1.7 Grocery category CPIs (context) | ✅ | `05_grocery_categories.ipynb` | BLS CPI indexes for food at home and its categories (produce, cereals and bakery, dairy, beverages, other/packaged foods, meats). Same API and key as notebook 01 (see D19) |

---

## Milestone 2: Clean and explore ✅

**Goal:** one tidy monthly data set, and a first look at the patterns.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 2.1 Combine and clean | ✅ | `06_clean_and_combine.ipynb` | Build `master_monthly.csv` (Jan 2010 to latest month): fill single missing months (D18), inflation-adjusted prices in latest-month dollars, herd repeated per month, all sources joined; generate `docs/DATA_DICTIONARY.md` (D27) |
| 2.2 Exploratory charts | ✅ | `07_explore.ipynb` | Seven charts from the master table: nominal vs real prices, all meats rebased, the full drought → slaughter → herd → price chain, a first look at delays, who gets the beef dollar in real cents, seasonality, a single-year prototype; ends with questions for Milestone 4 |

---

## Milestone 3: Event timeline ✅

**Goal:** a cited, dated table of events that can go on charts and into
statistical tests.

| Item | Status | Notebook / file | What's involved |
|---|---|---|---|
| 3.1 Research and record events | ✅ | `data/processed/events.csv` | Date, event, which meats it affected, source link. Candidates to check: COVID plant shutdowns (2020), JBS cyberattack (2021), drought years (D17), the 2022 chicken breast spike (feed costs? demand? bird flu?), 2022 food plant fires (widely given as the reason chicken prices rose; fact-checkers found them no more common than usual; test against the price data), Colorado bird-flu culls (2022, 2024) and cage-free egg law (2025) (these involve egg-laying hens; check whether they show up in meat-chicken prices at all), Mexican cattle import suspensions, screwworm (2026) |
| 3.2 Overlay events on prices | ✅ | `08_events.ipynb` | Annotated charts; first visual check of which events line up with jumps |

---

## Milestone 4: Analysis ✅

**Goal:** answer "did the events matter?" and "are prices justified?" with
evidence.

| Item | Status | Notebook | What's involved |
|---|---|---|---|
| 4.1 Inflation-adjusted prices | ✅ | `13_verdict.ipynb` (test 1) | Folded into the verdict (D38): real change since 2015 and against the 2015–2019 average, per meat |
| 4.2 Who gets the dollar | ✅ | `13_verdict.ipynb` (test 2) | Folded into the verdict (D38): rancher, packer and store parts of each pound, in real dollars, 2015 on |
| 4.3 Did prices shift at each event? | ✅ | `11_event_tests.ipynb` | Forecast from the 3 years before each event, compared with what happened; gaps judged against every ordinary month (D34) |
| 4.4 Supply side: drought → herd → price | ✅ | `12_supply_chain.ipynb` | Yearly fits (HAC errors) for each link: drought → cow sell-off rate, sell-off → herd change, herd → real price (log-log elasticity); a drought what-if; the 2026 exception (D37) |
| 4.5 Verdict | ✅ | `13_verdict.ipynb` | Three tests per meat (inflation, who gets the dollar, supply out-of-sample) and a plain-language verdict (D38) |

---

## Milestone 5: Interactive explorer ✅

**Goal:** the main page from the mockup, running on real data. Built as an interactive
page inside the project site instead of a Streamlit app (D39).

| Item | Status | What's involved |
|---|---|---|
| 5.1 Page skeleton and controls | ✅ | `explore.html`, built by `python -m src.build_site` from `src/explore_template.html`. Meat picker (beef, pork, chicken, all meats), prices at the time vs. after inflation, year selector ("All years" or one year), events on/off. The selection is kept in the page address, so a view can be shared. |
| 5.2 Price tiles and all-years view | ✅ | Tiles (latest price, change since 2015 before and after inflation, highest month) and the full price history with event bands and lines (D11) |
| 5.2b Single-year view | ✅ | Month-by-month chart, change through the year and against the same months of the year before, the highest month, the events that year, and a short note on the year |
| 5.2c "All meats" view | ✅ | All three meats as an index (2015 = 100), with all prices for comparison; works for all years or one year (D13) |
| 5.2d "Meat vs. the rest of the grocery cart" | ✅ | "Compare with" buttons add grocery categories (groceries overall, cereals, dairy, eggs, fresh produce, drinks, restaurant meals) to the All meats chart (D19) |
| 5.3 "Who gets the dollar" and verdict sections | ✅ | Stacked bars of the rancher, packer and store parts of each pound, by year, in real dollars; tapping a year opens it above. A "What it means" box for each meat; the verdict leads the front page. |
| 5.4 Methods and data page | ✅ | "Findings and methods explained" (`docs/FINDINGS.md`), plus the data sources, decisions and column dictionary, all published as site pages |

---|---|---|
| 5.1 App skeleton and sidebar | ⬜ | Page layout, load processed data; sidebar with meat selector (beef, pork, chicken, all meats), year selector ("All years" or one year), nominal vs inflation-adjusted, event markers on/off |
| 5.2 Price tiles and all-years view | ⬜ | `st.metric` tiles for the selected meat, full price history chart with event markers (see D11) |
| 5.2b Single-year view | ⬜ | When one year is picked: month-by-month chart, change from the year before, events that happened that year |
| 5.2c "All meats" view | ⬜ | All three meats on one chart as an index (Jan 2015 = 100), for all years or one year (see D13) |
| 5.2d "Meat vs. the rest of the grocery cart" | ⬜ | Indexed chart (2015 = 100) of the chosen meats against grocery categories (see D19) |
| 5.3 "Who gets the dollar" and verdict sections | ⬜ | Stacked bars, findings, explanations |
| 5.4 Methods and data page | ⬜ | How everything was done, with source links. Includes a plain-language "Who publishes this data" section on BLS, ERS, NASS and AMS, and "Key terms" sections on the three price stages and spreads, and on price indexes and rebasing (all from `docs/DATA_SOURCES.md`) |

---

## Milestone 6: Automate and test 🔄

**Goal:** the data can be refreshed with one command, and automatic checks catch
problems before they reach the app (D29, D31).

| Item | Status | What's involved |
|---|---|---|
| 6.1 Pipeline code in `src/` | ✅ | `config`, `bls`, `ers`, `nass`, `drought`, `master` modules, written from the notebooks' final code and verified to reproduce every processed file exactly; notebooks keep their own code as the readable record (D31) |
| 6.2 One-command refresh | ✅ | `python -m src.refresh` (also `--offline`, `--dry-run`): download, build in a temporary folder, check, publish only if checks pass, write `data/processed/REFRESH_REPORT.md` |
| 6.3 Data tests | ✅ | `pytest`: 23 tests: every check in `src/checks.py` on the committed master table, the data dictionary, the events file, and unit tests recreating the Milestone 1 bugs |
| 6.4 Run tests automatically | ✅ | `.github/workflows/tests.yml`: GitHub Actions runs the tests on every push |
| 6.5 Scheduled refresh | ⏸ | Optional. `deploy/monthly_refresh.sh` is written (20th of each month, 06:00) but not installed. Since D36 a refresh also means rebuilding the site and pushing both projects, so automating it needs a machine with the API keys and push access. Until then it's run by hand (see the 2026-11-15 "Project complete" log entry). |

---

## Milestone 7: Publish ✅

| Item | Status | What's involved |
|---|---|---|
| 7.1 Deploy on the VPS | ✅ | Done another way (D36, D39): the whole project site, including the interactive explorer, is static files served by schirko.com at /scott/meat-prices/ from Scott's VPS (Coolify redeploys on push). No Streamlit service needed. |
| 7.2 Portfolio polish | ✅ | README summary with the verdict, findings, charts, limits and tests badge; the project site at schirko.com/scott/meat-prices with the explorer, findings guide, notebooks and docs (D35, D36, D39); every page links back to the portfolio; final read-through done |
| 7.3 Story presentation | ✅ | 14-slide deck with its own charts, downloadable as PDF, PowerPoint, web page and slide images from the project's front page (D43) |

---

## Progress log

Newest first. One entry per finished item.

### 2026-11-26: October 2026 data refresh
- **Done:**
  - Refreshed the data through October 2026. The first run stopped at the checks
    because chicken's April 2026 price spreads went missing; fixed in D44 and re-run
    from the saved downloads. All checks passed; no past values were revised.
  - Re-ran notebooks 07–13 and updated the numbers in the README, the findings guide,
    the site's notes and the presentation (new charts from `src/presentation_charts.py`).
  - Put back the findings guide's link to the presentation, which an older open copy
    in PyCharm had saved over.
- **What October changed:** small moves, same story.

  | | Through September | Through October |
  |---|---|---|
  | Ground beef since 2015 | +63% | +62% |
  | Beef after inflation | +15% | +14% |
  | Pork after inflation | −23% | −24% |
  | Chicken after inflation | −13% | −16% |
  | 2026 beef vs. the shortage's prediction | $6.90 vs. $6.20 (+11%) | $6.90 vs. $6.21 (+11%) |

  The event tests, the drought → herd → price chain and the ranchers' share are unchanged.
- **Next:** re-export the presentation, rebuild the site and retake the portfolio
  screenshot.

### 2026-11-20: Presentation live on the site (D43)
- **Done:**
  - Exported the deck as PDF, PowerPoint and HTML into `presentation/`. The site build
    made the slide-images zip and the cover thumbnail from the PDF.
  - The build now finds the exports under the names the export menu gives them, so
    re-exporting needs no renaming.
  - Live at schirko.com/scott/meat-prices/#presentation: View the presentation, plus
    PDF (4.1 MB), PowerPoint (1.5 MB), Web page (2.9 MB) and Slide images (2.5 MB).
  - Recreated the project's virtual environment after the folder move (a venv stores
    its own folder path, so a moved one stops working); all 23 tests pass.
- **Note:** the first push didn't show up because Coolify didn't redeploy on its own;
  a manual Redeploy published it.
- **Still open:** the portfolio project adds a "Presentation" button to the project's
  card (D41: the card belongs to the portfolio).

### 2026-11-19: Project folder moved
- **Done:** the project now lives in `B:\Development\Python\meat-prices` (was
  `B:\_Dev\Python\meat-prices`), and the portfolio in `B:\Development\Python\Schirko`.
  Updated `SITE_DIR` in `.env` and `.env.example`, the build script's notes, and the
  "Project root" lines saved in notebooks 01–05. No code depends on the folder's
  location: every path is worked out from the project root (`src/config.py`).

### 2026-11-19: The story as a presentation (D43)
- **Done:**
  - A 14-slide business-story deck with its own charts (`src/presentation_charts.py`).
  - A presentation section on the front page with View, PDF, PowerPoint, Web page and
    Slide images buttons; `build_site` copies the exported files from `presentation/`.
  - CornerpostLogic.com byline on the front page.
- **Next:** export the deck and publish it (done 2026-11-20, above).

### 2026-11-16: Plain-language findings guide and notebook reading guides (D42)
- **Done:**
  - `docs/FINDINGS.md` rewritten for a smart reader with little analytical training:
    the short version, five ideas to know first, each finding with "how sure are we",
    how to read each chart, a glossary, then the methods for the curious.
  - A "Reading guide" cell added at the top of notebooks 08, 11, 12 and 13. They're text
    cells only, so the notebooks don't need re-running.

### 2026-11-16: Standing rule: write only inside scott/meat-prices/ (D41)
- **Rule (Scott):** this project owns `scott/meat-prices/` and its card screenshot,
  nothing else; `scott/index.html` and `scott/styles.css` belong to the portfolio
  project. Card changes go to Scott as text.
- **Build script:** no step ever wrote `scott/index.html`, so nothing was removed. The
  build now refuses to run if `SITE_DIR` points anywhere but the `meat-prices` folder
  (or the local `site/` preview).

### 2026-11-15: Shared portfolio bar (D40)
- **Done:** every generated page now uses the portfolio's shared "back to portfolio" bar
  (`/scott/backbar.css`), with links to Overview, Explore, Notebooks and Docs. The
  project's own back links are gone.
- **Tested:** on a local server laid out like schirko.com (front page, explorer, a
  notebook page, a doc page, and the explorer at phone width), with no script errors.

### 2026-11-15: Project complete (Milestone 7)
- **Done:** item 7.2, the final read-through. The README's data sources now include
  NASS slaughter and the U.S. Drought Monitor. Its project layout includes the findings
  guide and the site builder, and `app/` is marked as an unused placeholder (D39). Scott
  approved the portfolio card.
- **Status:** every milestone is complete except the optional scheduled refresh (6.5),
  which is done by hand for now.
- **Keeping it current:**
  1. `python -m src.refresh`
  2. Run and save any notebook whose results should change.
  3. `python -m src.build_site`
  4. Push meat-prices, then Schirko.
- **When new data arrives:** update the hand-written wording that depends on it (the
  front-page verdict, the explorer's "What it means" and year notes, and the findings
  guide). The numbers update themselves.

### 2026-11-15: Interactive explorer (Milestone 5 complete)
- **Done:** `explore.html` on the project site, built with the rest of the site by
  `python -m src.build_site` (D39). It has:
  - a meat picker, prices at the time or after inflation, and all years or one year
  - events shown as bands and lines, each with a card that includes notebook 11's test
    result
  - an All meats view with grocery comparisons
  - "who gets each dollar" stacked bars
  - a "What it means" box for each meat
- **To feed the event cards,** notebook 11 now saves its results to
  `data/processed/event_tests.csv`.
- **Tested:** desktop and phone widths, light and dark; no script errors.
- **Next:** Milestone 7 wrap-up: a final pass over the site and README, and the
  portfolio card.

### 2026-11-15: The verdict (items 4.5, 4.1, 4.2; Milestone 4 complete)
- **Done:** notebook `13_verdict.ipynb`. It runs three tests per meat, then gives a
  plain-language verdict (D38). Items 4.1 (inflation) and 4.2 (who gets the dollar) are
  folded in, since notebook 07 had already done most of that work.
- **Verdict: mostly justified.**
  - Pork and chicken are cheaper than in 2015 after inflation (−23%, −13%).
  - Beef's rise through 2025 is explained by the cattle shortage. Since 2019, ranchers
    got 86% of the real price rise; packers' part fell from $1.11 to $0.30 a pound.
  - The exception is 2026: beef is about 11% above what the herd predicts (fit on
    2015–2025), and the extra went mainly into the store's part of the price.
- **Also:** the README, the site front page and the findings guide now lead with the
  verdict.
- **Next:** Milestone 5, the interactive app.

### 2026-11-15: Findings guide and portfolio links
- **Done:** `docs/FINDINGS.md`, a single plain-language guide to the whole project. It
  covers the one-minute story, each finding and how it was found, every method
  explained, the data problems caught, how it's built, likely employer questions with
  answers, and limits. It's published on the site as "Findings and methods explained"
  and linked from the front page and the README.
- **Also:** every page on the site now links back to the portfolio at schirko.com/scott.
- **Next:** item 4.5, the verdict. The guide gets updated with each new finding.

### 2026-11-15: The supply chain measured (item 4.4)
- **Done:** notebook `12_supply_chain.ipynb`. It measures each link of the chain with one
  row per year and corrected p-values (D37), then runs a drought what-if.
- **Found:**
  - Drought raises the cow sell-off in the same year: 10 more points of drought means
    about 0.8 points more of the herd sold, roughly 245,000 cows.
  - Selling more than about 9.6% of the herd in a year shrinks it, by about 1.1% per
    extra point.
  - A 1% smaller herd goes with about a 1.8% higher real beef price. That holds with a
    time trend and in year-to-year changes.
  - The herd alone predicts a +25% real price rise from 2019 to 2025; the actual rise was
    +28%.
  - Drought explains roughly 40% of the herd loss and about 11 points of the price rise.
  - 2026 breaks the pattern: drought is back, but ranchers are keeping their cows.
- **Next:** item 4.5, the verdict, with 4.1 and 4.2 folded in.

### 2026-11-15: Site moved to schirko.com (D36)
- **Done:**
  - GitHub Pages unpublished.
  - `python -m src.build_site` now builds into `SITE_DIR`, the Schirko portfolio
    folder, so the site is served at schirko.com/scott/meat-prices/.
  - The project docs are published as pages too.
  - The repo stays public; the site and the portfolio card link to it.
  - The portfolio card in the Schirko project now points to the new address.
- **Next:** item 4.4. After each new notebook,
  rebuild the site and push the Schirko project.

### 2026-11-14: Project site on GitHub Pages (D35)
- **Done:** `python -m src.build_site` builds a front page (summary, key numbers, the
  two charts, findings, method, limits, links) and one HTML page per notebook in
  `docs/`. GitHub Pages serves it at https://schirko.github.io/meat-prices/. The
  portfolio card links there and to the repo.
- **Next:** item 4.4. After each new notebook, rebuild the site and push.

### 2026-11-14: Event tests (item 4.3)
- **Done:** notebook `11_event_tests.ipynb`. For each event and meat, an AR(1)-with-trend
  model fit to the 3 years before forecasts the next 6 months; the gap between actual
  and forecast is judged against the gaps at every ordinary month (D34). A simpler
  forecast is run as a second opinion (they agree on 15 of 19 tests).
- **Found:** the COVID closures clearly shifted all three meats (+11% to +17%). Chicken's
  2022 spike was real but can't be split between feed costs and bird flu. No popular
  claim holds up. Apart from COVID, only the May 2025 Mexican import suspension looks
  like a step up for beef, and that one is borderline. So most of beef's rise isn't
  explained by sudden events.
- **Problem found and fixed:** the model's own 95% range flagged about 30% of
  ordinary months as shifts, so it wasn't used for the verdicts.
- **Next:** item 4.4, drought → sell-off → herd → price.

### 2026-11-14: Events on the price charts (Milestone 3 complete)
- **Done:** notebook `08_events.ipynb` (item 3.2): an event timeline, each meat's price
  with its events, a three-month "how much did the price move" screen ranked against
  every other three-month move (D33), and the beef events on the drought → sell-off →
  price chain.
- **Found:** the 2020 COVID closures caused one of the biggest price moves on record for
  all three meats, then faded. Chicken's 2022 spike lines up with feed costs and bird
  flu together. The three popular claims came in ordinary months (or, for the fires
  claim, only chicken moved). Beef's rise is a slow build following the herd, not a
  series of event shocks.
- **Next:** Milestone 4, testing these patterns properly.

### 2026-11-14: README summary and event list approved
- **Done:** README now opens with the tests badge, a one-page summary, key findings
  and two charts made by `python -m src.readme_charts` (item 7.2, done early).
  GitHub Actions tests pass (green badge). Scott reviewed and approved all 16
  events in `events.csv` as they are (item 3.1 complete).
- **Next:** item 3.2, notebook `08_events.ipynb`, marking the events on the price charts.

### 2026-11-14: Hosting decision
- **Done:** decided the portfolio will link to the public GitHub repo for now (D32);
  VPS hosting (item 7.1) deferred. The README becomes the project's front door.
- **Next:** item 3.1 event review, then 3.2.

### 2026-11-13: Milestone 6 items 6.1–6.4 complete
- **Done:** built the refresh pipeline in `src/` and the tests in `tests/`, with the
  decisions recorded in D31 (Scott asked me to make the calls). An offline refresh from
  the 2026-10-26 raw files reproduced every processed file and the master table exactly.
  All 23 tests pass on the committed data. GitHub Actions workflow added. The VPS refresh
  script is written and will be installed in Milestone 7.
- **Next:** Scott runs `pytest` and `python -m src.refresh --offline --dry-run` on his
  machine to confirm, pushes, and checks the first GitHub Actions run; then back to the
  event list review (item 3.1).

### 2026-11-13: Plan updated: automation, tests and VPS hosting
- **Done:** reviewed what's left to reach a finished project. Added Milestone 6
  (automate and test: shared code in `src/`, one-command refresh, `pytest` data
  tests, GitHub Actions, monthly refresh on the VPS) per D29. Publishing moves
  to Milestone 7 and targets Scott's VPS instead of Streamlit Community Cloud
  (D30), with the app featured on his portfolio site.
- **Next:** Scott reviews the event list (item 3.1); then item 3.2.

### 2026-10-26: Milestone 2 complete; item 3.1 drafted
- **Done:** notebook 07 run in full on Scott's machine, completing Milestone 2.
  Drafted `data/processed/events.csv` with 16 sourced events (drought periods,
  plant fire and closures, COVID shutdowns, the JBS cyberattack, feed costs,
  bird flu, Mexican cattle import suspensions, screwworm, the 2025 shutdown) and
  three popular explanations to test (2022 plant fires, Colorado culls,
  cage-free law). Decision D28 records the format and inclusion rules.
- **Next:** Scott reviews the event list (additions, removals, dates); then
  item 3.2, overlaying the events on the prices.

### 2026-10-26: Item 2.2 written
- **Done:** notebook 07 written and run on the real master table; findings and
  a list of questions for Milestone 4 written in.
- **Findings:** the drought → sell-off → herd → price chain shows up in both
  cycles (2011–2019 and 2020–2026). Drought and cow slaughter rise together in
  the same year (correlation +0.58, yearly); a shrinking herd goes with a
  rising real beef price the same year and the next (−0.59, −0.55). Since 2019
  the rancher's part of retail beef rose about 185 real cents per pound, the
  store's about 64, and the packer's fell about 65. Seasonal swings are small
  (about ±2%). A first monthly test of the drought delay gave no clear signal,
  so yearly values are used instead (explained in the notebook).
- **Next:** Scott runs notebook 07; then Milestone 3, the event timeline.

### 2026-10-26: Item 2.1 complete
- **Done:** notebook 06 run in full on Scott's machine: `master_monthly.csv`
  (201 months × 56 columns) and `docs/DATA_DICTIONARY.md` generated, all
  checks as expected (only October 2025 filled; only chicken's ERS January–March
  2026 still empty).
- **Next:** item 2.2, exploratory charts.

### 2026-10-26: Item 2.1 written
- **Done:** agreed the master table design together (D27). Notebook 06 builds
  `master_monthly.csv` (201 months × 56 columns), fills October 2025 and flags
  it, adds inflation-adjusted prices, checks every column, and generates
  `docs/DATA_DICTIONARY.md`. Tested on the real data from Milestone 1.
- **First finding:** in September 2026 dollars, ground beef is up about 15%
  since 2015, while pork chops are down about 23% and chicken breast about 13%:
  beef is the only meat that got more expensive in real terms.
- **Next:** Scott runs notebook 06; then item 2.2, exploratory charts.

### 2026-10-26: Milestone 1 complete
- **Done:** notebooks 04 and 05 run in full on Scott's machine. The drought
  table now starts in January 2010 (stray December 2009 week removed). Every
  data source is downloaded, checked and saved to `data/processed/`:
  `ers_price_spreads_monthly.csv`, `nass_herd_jan1.csv`,
  `nass_slaughter_monthly.csv`, `drought_cattle_country_monthly.csv`,
  `drought_state_weights.csv`, `cpi_grocery_categories_monthly.csv`. BLS meat
  prices and CPI are still read from notebook 01's raw download; Milestone 2
  brings them into a processed table.
- **Next:** Milestone 2, item 2.1: clean and combine everything into one
  monthly table.

### 2026-10-26: Item 1.7, first run reviewed
- **Done:** notebook 05 ran on Scott's machine: all 15 series returned, each
  complete except October 2025. Added a "price indexes and rebasing" explanation
  (index levels vs. prices, with a worked example from the real data) to the
  notebook and a Key terms section in DATA_SOURCES.md. Findings written in.
- **Findings:** beef and veal rose about 59% since 2015 (67% since 2019), more
  than any grocery category and more than all items (42%). Groceries overall
  (food at home, +33%) rose *less* than general inflation since 2015. Eating out
  rose 56%. Beef broke away from everything else from 2024, when the herd hit
  its low. Eggs show the baseline effect (D20): −2% since 2015, +37% since 2019.
- **Next:** Scott re-runs notebooks 04 and 05 so their outputs are saved; then
  Milestone 2.

### 2026-10-26: Item 1.7 started
- **Done:** notebook 05 written: downloads 15 BLS CPI series in one request
  (all items, food at home, food away from home, eight grocery categories, and
  beef, pork, poultry and eggs), checks coverage, rescales every series to its
  2015 average = 100, compares changes since 2015 and 2019 (D20), charts meat
  against the rest of the grocery cart and saves
  `cpi_grocery_categories_monthly.csv`. Reordered this log so the newest entry
  is first, as intended.
- **Next:** Scott runs notebook 05; we fill in the findings together. That
  completes Milestone 1.

### 2026-10-26: Item 1.6, first run reviewed
- **Done:** notebook 04 ran on Scott's machine: 17 states hold 76.2% of U.S.
  beef cows (Texas weight 0.19), 878 weeks per area, both data checks 100%.
  Findings written into the notebook. Fix: the first 2010 map starts on
  December 29, 2009, which created a stray 2009 month; now dropped.
- **Findings:** two major droughts in cattle country (2011–2013, peak 63% in
  severe drought or worse in September 2012; 2020–2023, worst in 2022 at about
  35% on average), each followed by a cow sell-off that ended when the drought
  eased. A new drought in 2026 (about 44% in the spring) has not, so far, been
  followed by more cow slaughter: an open question for item 4.4.
- **Next:** Scott re-runs notebook 04 (to save its outputs and the corrected
  table); then item 1.7, grocery category CPIs.

### 2026-10-26: Items 1.4 and 1.5 complete
- **Done:** notebook 03 run in full on Scott's machine: herd complete for
  2010–2026 (51 rows), slaughter complete for January 2010 to September 2026
  (603 rows), results match the test run. Saved `nass_herd_jan1.csv` and
  `nass_slaughter_monthly.csv`.
- **Next:** run notebook 04 (drought).

### 2026-10-26: Item 1.6 started
- **Done:** agreed the drought method together (D26): states holding 75% of
  U.S. beef cows, weighted by their January 1, 2019 beef cows; % of area in
  severe drought or worse (D2–D4) as the headline and DSCI for statistics;
  monthly from 2010. Notebook 04 written: downloads state beef cows (NASS) and
  weekly drought statistics (U.S. Drought Monitor), checks them, builds the
  cattle-country measures, charts drought against cow slaughter, and saves two
  processed files. Added the Drought Monitor to the agencies table.
- **Next:** Scott runs notebook 03 (Part 2) and then notebook 04; we fill in the
  findings together.

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

### 2026-10-26: Item 1.3 complete
- **Done:** notebook 02 run in full on Scott's machine. All results match the
  test run: files agree in the overlap, 10 of 11 checks within 0.1, the pork
  column error confirmed (D23), coverage complete for beef and pork (141
  months), chicken missing Jan–Mar 2026 as expected.
  `data/processed/ers_price_spreads_monthly.csv` saved (2,808 rows).
- **Next:** notebook 03 Part 1 (NASS).

### 2026-10-26: Docs, key terms; items 1.4 and 1.5 started
- **Done:** added "Key terms: the three price stages" to DATA_SOURCES.md and the
  README ("three values per meat" = farm, wholesale and retail for each meat,
  not three data sources). NASS API key registered and stored in `.env`.
  Notebook 03 Part 1 written: checks row counts, downloads cattle inventory and
  monthly cattle slaughter from 2010 (D24), and lists every series.
- **Next:** Scott runs notebook 02 Part 2 and notebook 03 Part 1; we choose the
  herd and cow slaughter series together.

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
