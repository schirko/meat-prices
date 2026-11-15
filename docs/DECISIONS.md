# Decision log

Every significant choice in this project, and why we made it. New decisions go
at the bottom with the next number. If a decision is later changed, the old
entry stays and a new one explains the change.

Format: **what we decided**, **why**, and **what we considered instead**.

---

## D1. Build this as a portfolio project, not a business (2026-10-26)

- **Decided:** the goal is a Streamlit app that shows potential employers how I
  work with real data. It does not need to bring in traffic or make money.
- **Why:** removing the money question lets the project focus on the quality of
  the analysis. It also keeps it separate from AtHomeGourmet.com, which is being
  saved for a different idea.
- **Considered instead:** making it a feature of AtHomeGourmet.com. Rejected
  because the audiences and goals are different.

## D2. Cover beef, pork and chicken (2026-10-26)

- **Decided:** compare all three meats, not just beef.
- **Why:** beef has had the biggest increases, but comparing it with pork and
  chicken shows whether the cause is something beef-specific (like the cattle
  herd) or something affecting all meat (like inflation or packing costs). It
  also lets us look at whether shoppers switched to cheaper meats.
- **Considered instead:** beef only. Simpler, but loses the comparison.

## D3. Start the history in 2015 (2026-10-26)

- **Decided:** use 2015 to today as the main time range.
- **Why:** it gives five years of "normal" before 2020, so the post-2020 increases
  can be compared against a baseline rather than a single starting point.
- **Considered instead:** starting in 2020. Too short to show what normal looked
  like.

## D4. Use only free, public, official data (2026-10-26)

- **Decided:** BLS, USDA ERS and USDA NASS as the data sources.
- **Why:** they are free, documented, regularly updated and trusted. An employer
  or reader can check every number.
- **Considered instead:** paid grocery scanner data. More detailed, but costs
  money and can't be shared publicly.

## D5. Show prices both "at the time" and adjusted for inflation (2026-10-26)

- **Decided:** every price chart can switch between nominal dollars and
  inflation-adjusted dollars.
- **Why:** part of every price increase is general inflation. Separating that
  out is the only fair way to ask whether meat specifically got more expensive.

## D6. Test events statistically, not just by eye (2026-10-26)

- **Decided:** use changepoint detection and/or interrupted time series to check
  whether prices actually shifted at each event.
- **Why:** it's easy to draw a line on a chart next to a price jump and call it a
  cause. A statistical test is more honest and a stronger portfolio piece.
- **Note:** these tests show timing, not proof of cause. The app will say so.

## D7. Sidebar layout for the app (2026-10-26)

- **Decided:** the app uses a sidebar for filters (meats, date range, nominal vs
  inflation-adjusted, event markers on or off) and a single scrolling main page.
- **Why:** this project has several filters that apply to every chart, and a
  sidebar keeps them in one place without crowding the charts. It is also
  Streamlit's standard pattern. (Normally I avoid sidebars, but here it fits.)
- **Considered instead:** filters above each chart. Repetitive with this many
  shared filters.

## D8. Notebook format (2026-10-26)

- **Decided:** every notebook uses the same structure: what we're looking for,
  code, result, how to read it, what it means, what's next and why.
- **Why:** makes the notebooks readable by non-technical reviewers and keeps the
  reasoning visible, not just the code.

## D9. Raw data is not committed to git (2026-10-26)

- **Decided:** `data/raw/` is in `.gitignore`. The notebooks contain the code to
  re-download everything. Processed data the app needs will be committed.
- **Why:** keeps the repository small and makes it clear the data comes from the
  official sources, not a copy that could drift.

## D10. API keys live in a `.env` file (2026-10-26)

- **Decided:** keys are read from `.env` (not committed). `.env.example` shows
  which keys are needed.
- **Why:** keeps keys out of the public repository.

## D11. One meat at a time, with an all-years view and a single-year view (2026-10-26)

- **Decided:** the user picks one meat (beef, pork or chicken) and first sees
  the overall view: the whole price history across all years. They can then
  isolate any single year to see it month by month.
- **Why:** focusing on one meat keeps each chart readable. The all-years view
  answers "how did we get here?" and the single-year view answers "what
  happened in that year?", for example when an event hit and how fast prices
  reacted.
- **Data impact:** the BLS data is monthly, so a single year has 12 points. That
  is enough for a month-by-month chart, and confirms monthly (not annual) data
  is the right choice in Milestone 1.
- **Changes:** replaces the mockup's "show all three meats on one chart"
  checkboxes with a meat selector. Comparing meats side by side moves to its own
  section (see open question below).
- **Resolved:** an "All meats" option is added to the selector. See D13.

## D12. Public repo, deployed on Streamlit Community Cloud (2026-10-26)

- **Decided:** the GitHub repository is public, and the app will be deployed on
  Streamlit Community Cloud once there is a working version.
- **Why:** employers can read the code, notebooks and docs, and use the live
  app, from one link. Streamlit Community Cloud is free and deploys directly
  from the GitHub repo.
- **Consequences:**
  - Nothing secret is ever committed. API keys stay in `.env` (see D10).
  - The deployed app reads the processed data files in `data/processed/` and
    does not call the BLS or USDA APIs. The live app therefore needs no API
    keys, loads faster, and keeps working if an API is down. Data is refreshed
    by re-running the notebooks and committing the new processed files.

## D13. "All meats" option compares percentage change, not dollars (2026-10-26)

- **Decided:** the meat selector gets a fourth option, "All meats". It shows the
  three meats on one chart as percentage change from a starting point (an index
  where January 2015 = 100), not as dollars per pound. The year selector works
  the same way in this view. Picking one meat still shows dollars per pound.
- **Why:** the question "did beef rise faster than pork and chicken?" needs all
  three on one chart. But beef costs several times more per pound than chicken,
  so in dollars the chicken line sits flat near the bottom and its changes are
  hard to see. Indexing puts all three on the same scale, so the steepest line
  is the one that rose fastest.
- **Considered instead:** dollars on one chart (misleading, as above); keeping
  the comparison only in the verdict section (hides the most interesting
  comparison until the end).

## D14. Matplotlib in notebooks, Plotly in the app (2026-10-26)

- **Decided:** notebook charts use matplotlib; the Streamlit app uses Plotly.
- **Why:** GitHub displays notebooks with their saved output, but it can't show
  Plotly's interactive charts, so they appear blank to anyone browsing the repo.
  Matplotlib charts are saved as images and show up everywhere. The app is
  where interactivity (hover, zoom) is useful, and Plotly works well in
  Streamlit.

## D15. One BLS series per meat (2026-10-26)

- **Decided:**
  - **Beef:** APU0000703112, ground beef, 100% beef
  - **Pork:** APU0000FD3101, all pork chops
  - **Chicken:** APU0000FF1101, chicken breast, boneless
  - **CPI:** CUUR0000SA0, all items, not seasonally adjusted
- **Why:** each chosen series is complete from January 2015 to September 2026
  except October 2025 (missing from every series; see D18). Ground beef and
  chicken breast are the cuts most households buy and the prices most often
  quoted in the news. All pork chops is the broadest pork measure, and the three
  pork cuts moved together, so the choice mattered little. The CPI series is not
  seasonally adjusted to match the meat prices.
- **Ruled out:** bone-in pork chops (stopped after May 2026); whole chicken
  (also missing May 2020, and fewer people buy it); boneless pork chops (no
  advantage over all pork chops).
- **Evidence:** coverage table, missing-months table and candidate charts in
  `notebooks/01_bls_retail_prices.ipynb`.

## D16. Drop `ruptures` for now (2026-10-26)

- **Decided:** removed the `ruptures` changepoint library from
  `requirements.txt`.
- **Why:** it has no ready-made Windows package for Python 3.14, so pip tried to
  compile it from source and failed ("Microsoft Visual C++ 14.0 or greater is
  required"). Because one package failed, pip installed none of the others.
- **Plan for Milestone 4:** event testing (D6) will use interrupted time series
  in `statsmodels`, which installs cleanly. If we still want automatic
  changepoint detection, we'll revisit then: check for a newer `ruptures`
  release, or write a simple changepoint search ourselves.
- **Considered instead:** installing Microsoft C++ Build Tools (several GB, and
  every future user of the repo would need it too); downgrading Python (affects
  the whole environment for one optional package).

## D17. Treat drought as a root cause of the beef price rise (2026-10-26)

- **Decided:** the analysis will trace one cause chain in detail:
  **drought → less grazing and costlier hay → ranchers sell off cows → smaller
  herd → fewer cattle to market → higher beef prices.** We add drought data
  (U.S. Drought Monitor) and beef cow slaughter (NASS) to Milestone 1, and test
  the chain step by step in Milestone 4.
- **Why:** the drought years around 2020–2022 are a likely root cause of the
  beef price rise, rather than a one-time shock like a plant closure. It also
  explains why beef prices stay high: a cow sold off can't be replaced quickly.
  Rebuilding the herd takes years, because a heifer kept back for breeding takes
  roughly two years before her first calf reaches market.
- **What to look for:** each step should show up *after* the one before it,
  with a delay. Drought first, then a spike in cow slaughter, then a falling herd
  count, then rising prices. Measuring those delays is the analysis.
- **Fits the comparison in D2:** pork and chicken don't depend on pasture, and
  they rose far less than beef. That supports drought and the cattle herd as
  beef-specific causes.
- **Caution:** timing lining up isn't proof of cause. The app will present this
  as the evidence for the chain, alongside other factors (packing capacity,
  imports, demand).

## D18. Fill single missing months with the average of their neighbors (2026-10-26)

- **Decided:** when a month is missing from a BLS series, fill it with the
  average of the month before and the month after. Filled values are flagged in
  a column (`is_filled`) so they can be identified, and the app's methods page
  will say which months were filled. Applied in Milestone 2 (cleaning), not in
  the raw data.
- **Why:** notebook 01 found the same month missing from every series,
  including the CPI, most likely because of the late-2025 federal government
  shutdown. A gap would break the line on every chart and leave holes in
  month-over-month calculations. A one-month average is a small, honest fix:
  prices don't usually jump and fall back within a single month.
- **Limit:** only for gaps of one month (or two in a row at most). Longer gaps
  stay missing, because an average across many months would hide real movement.
- **Considered instead:** leaving a visible gap (honest but breaks charts and
  calculations); dropping the month from every series (shifts the timeline).

## D19. Stay focused on meat; add other groceries as context only (2026-10-26)

- **Decided:** the project stays focused on beef, pork and chicken, and the repo
  stays `meat-prices`. Other grocery categories (produce, cereals and bakery,
  dairy, beverages, packaged foods) are added as context only: one data item
  (1.7) and one comparison chart in the app (5.2d).
- **Why:** notebook 01 showed beef rose about 63% since 2015 against about 42%
  for overall prices, while pork and chicken breast rose less than inflation.
  Comparing meat with the rest of the grocery cart tests whether beef is unusual
  or whether all food rose the same way. But a full "rising food prices" project
  would need a cause investigation for every category, each with different
  drivers. The project's strength is depth: the drought → herd → beef price
  chain, and who gets each dollar, which also connects to my agriculture work.
- **Considered instead:** renaming to `rising-food-prices` and broadening the
  objective. Rejected for now; the notebook-per-source structure would support
  it as a later phase. The app's title may be sharpened later (for example,
  "Why did beef get so expensive?") without renaming the repo.

## D20. Always show more than one baseline year for "change since" figures (2026-10-26)

- **Decided:** wherever the app states a percentage change, it shows it from
  both 2015 and 2019 (the last year before COVID), or lets the user pick the
  starting year.
- **Why:** the starting year changes the story. Since 2015, chicken breast rose
  less than inflation (+23% vs +42%); since 2019, it rose slightly more (+39% vs
  +32%), because 2015–2019 was a cheap stretch for chicken and pork. Beef is the
  outlier either way. Showing both keeps anyone from claiming a baseline was
  chosen to make a point.

## D21. ERS spreads: CSV files, historical plus recent, reviewed before combining (2026-10-26)

- **Decided:** download four ERS CSV files: the historical file (1970 to early
  2026) and the three recent 24-month files (beef, pork, and the summary file
  for chicken). Notebook 02 is split in two: Part 1 downloads and takes an
  inventory of every data item; Part 2 combines them after we review the
  inventory together.
- **Why:**
  - The historical file was last updated in February 2026, so on its own it
    stops months short of the BLS data. The recent files bring it up to
    September 2026, and the months where they overlap let us check the files
    agree.
  - CSV rather than Excel: the CSVs are already in a long, tidy layout (one row
    per item per month), so less reshaping and fewer chances for error.
  - Reviewing first: ERS names the same measure slightly differently in
    different files, so matching names is a judgment call worth making
    deliberately, not in code we haven't looked at.
- **Considered instead:** the historical file alone (too old); the Excel
  versions (multi-row headers, more cleanup).

## D22. Keep three values per meat and calculate the spreads ourselves (2026-10-26)

- **"Three values per meat"** means the three price stages for each of beef,
  pork and chicken (farm, wholesale, retail), not three data sources. See "Key
  terms" under ERS in `docs/DATA_SOURCES.md`.
- **Decided:** from the ERS files we keep only the retail value, wholesale value
  and net farm value (beef and pork; chicken has no farm value), and calculate
  everything else with ERS's definitions:
  - farm-to-wholesale spread = wholesale − net farm (roughly the packer)
  - wholesale-to-retail spread = retail − wholesale (roughly the store)
  - farmer's share = net farm ÷ retail
- Where the historical and recent files overlap, the **recent** file is used
  (newer, includes any revisions). For chicken's recent months, wholesale =
  retail − published spread.
- **Chicken's January–March 2026 stays a gap** (no ERS file covers it), per
  D18's two-month limit, and will be noted on the methods page.
- **Why:** three names to match per meat instead of about ten; the same formula
  for every month from 2015 to 2026; and a built-in check, since our results can
  be compared with the spreads and shares ERS publishes.
- **Result:** the historical and recent files agree to within 0.05 cents where
  they overlap, and our calculations match ERS's published figures to within
  0.1, except one mislabeled column (D23).

## D23. Use our calculated pork farm-to-wholesale spread, not the published column (2026-10-26)

- **Decided:** ignore the "Pork price spread: farm to wholesale" column in ERS's
  recent pork file and use our calculated value.
- **Why:** in that file the column holds the *percent* share (for example 16.2
  in October 2024) instead of cents per pound. It's identical to the "farm-
  wholesale spread share of retail value" column in every month. ERS's own
  figures show the correct value: farm-to-retail (385.7) minus wholesale-to-
  retail (305.8) = 79.9 cents, which matches our wholesale − net farm
  calculation. The historical file doesn't have the problem.
- **Evidence:** "Investigating the pork mismatch" in
  `notebooks/02_ers_price_spreads.ipynb`.
- **Possible follow-up:** report the mislabeled column to ERS.

## D24. Cattle herd and slaughter data start in 2010, not 2015 (2026-10-26)

- **Decided:** NASS cattle inventory and cow slaughter are downloaded from 2010,
  five years earlier than the price data (D3).
- **Why:** the cattle cycle is slow. Ranchers sold off cows in the 2011–2013
  drought (mainly Texas and the southern Plains), rebuilt the herd from about
  2014 to 2019, then sold off again. Without the earlier years, the herd chart
  would start in the middle of a rebuild and we couldn't judge whether the
  recent sell-off is unusual. It also gives the lag analysis in item 4.4 room
  to look back several years.
- **Focus on cows:** cow slaughter, not total cattle slaughter, is the sell-off
  signal. Steers and heifers are slaughtered every year as normal business;
  cows are the breeding herd, so each cow slaughtered means fewer calves later.

## D25. Six NASS series: January 1 herd and federally inspected slaughter (2026-10-26)

- **Decided:**
  - **Herd (January 1 inventory):** all cattle including calves; beef cows;
    beef replacement heifers (500 lb and over).
  - **Slaughter (monthly, federally inspected):** beef cows (cows excluding
    milk cows); heifers; steers.
  - **Calculated:** heifer share of slaughter = heifers ÷ (heifers + steers);
    beef cows slaughtered over the latest 12 months; and, per year, beef cows
    slaughtered as a % of the January 1 beef cow herd.
- **Why:**
  - **January 1, not July 1:** NASS skipped its July cattle report in 2013,
    2016 and 2024, so January is the only complete yearly series.
  - **Beef cows, not all cows:** dairy cows are culled for different reasons
    (milk prices, herd turnover) and don't belong to the beef breeding herd.
  - **Replacement heifers:** young females held back to become cows. A rising
    count is the first sign ranchers are rebuilding; a low count means they
    aren't.
  - **Heifer share of slaughter:** a standard industry signal. Heifers can be
    kept for breeding or slaughtered; a high share means the herd is shrinking.
  - **Federally inspected (FI):** the only slaughter version NASS splits into
    cows, heifers and steers, and it covers almost all commercial slaughter.
  - **Rolling 12-month total:** cow slaughter is seasonal (more cows culled in
    the fall), so the 12-month total shows the trend without the seasons.
- **Coverage:** herd complete for 2010–2026; slaughter complete for every month
  from January 2010 to September 2026. No suppressed values.

## D26. Drought in cattle country: beef-cow-weighted, fixed 2019 weights (2026-10-26)

- **Decided:**
  - **Source:** U.S. Drought Monitor statistics service, weekly percent of
    each state's area in each drought category, cumulative format.
  - **States:** the states that together hold at least 75% of U.S. beef cows
    on January 1, 2019 (from NASS).
  - **Weights:** each state's share of those states' beef cows on January 1,
    2019, fixed for every year.
  - **Measures:** % of area in severe drought or worse (D2–D4) as the headline
    for the app; DSCI (Drought Severity and Coverage Index, 0–500) for the
    statistics in Milestone 4. The lower 48 states as a whole are kept for
    comparison.
  - **Period:** January 2010 onward (matches D24); weekly values averaged to
    months.
- **Why:**
  - Drought only matters for beef where the cattle are: drought in Texas
    affects far more cows than drought in Nevada.
  - **Fixed 2019 weights:** 2019 was the herd's peak before the drought. If
    each year used its own herd, a state that lost cows *because of* drought
    would count less afterwards, understating the drought.
  - **D2–D4 headline:** one plain-English number ("40% of cattle country was in
    severe drought"). **DSCI for statistics:** combines coverage and severity
    in one number, and is the Drought Monitor's own standard index.
  - **DSCI calculated ourselves:** with cumulative percentages, DSCI equals
    D0 + D1 + D2 + D3 + D4, the same as weighting each category 1 (D0) to 5
    (D4). This avoids a second download and is easy to check.
  - Essentially the same idea as USDA's "cattle in drought" statistic, but
    built transparently from public data.
- **Considered instead:** all 48 states unweighted (dominated by states with
  few cattle); each year's own weights (understates drought, as above).

## D27. One master monthly table: range, real dollars, herd and gaps (2026-10-26)

- **Decided:**
  - **One table**, `data/processed/master_monthly.csv`, built by notebook 06,
    is what the analysis and the app read. A data dictionary,
    `docs/DATA_DICTIONARY.md`, is generated by the same notebook.
  - **Range:** January 2010 to the latest month. Price, ERS and grocery columns
    are empty before 2015 (D3); herd, slaughter and drought start in 2010 (D24).
  - **Inflation-adjusted prices** (`_real` columns) are in dollars of the
    latest month: price × (latest CPI ÷ CPI that month), using CPI all items.
  - **Herd:** each January 1 count is repeated for every month of that year,
    in columns ending `_jan1`. No values are estimated between counts.
  - **Gaps:** single (or two-month) gaps with data on both sides are filled by
    straight-line interpolation, which for one month is the average of its
    neighbors (D18). A `filled_columns` column lists what was filled in each
    month. Longer gaps stay empty.
- **Why:**
  - One table means every chart and test uses exactly the same numbers.
  - Latest-month dollars are the most intuitive for readers ("in today's
    money"); the app labels them with the month.
  - Repeating the January count is honest about what NASS published;
    estimating in between would invent monthly numbers that don't exist.
  - Generating the data dictionary from the notebook keeps it in sync with the
    table; the notebook stops if any column lacks a description.
- **Result (first build):** 201 months × 56 columns. Only October 2025 was
  filled; the only remaining gap is chicken's ERS data for January–March 2026.

## D28. Event timeline: what goes in, and how it's recorded (2026-10-26)

- **Decided:** events live in `data/processed/events.csv`, one row per event,
  with: start and end date, how exact the date is (`day` or `month`), a short
  description, a category (`weather`, `packing_capacity`, `trade`, `disease`,
  `feed_costs`, `data`, `popular_claim`), the meats it could affect, the effect
  we'd expect if it mattered, whether it's a **popular explanation** being
  tested, and a source link.
- **What goes in:** events with a plausible, specific link to the supply or cost
  of beef, pork or chicken, plus the popular explanations we agreed to test (the
  2022 plant fires, the Colorado bird-flu culls and the cage-free law). Every
  event needs a source; drought periods come from our own drought measure (D26).
- **Why:**
  - **Expected effect written down in advance:** saying what each event *should*
    do to prices before testing it keeps the analysis honest; we can't decide
    after the fact that whatever happened was the expected effect.
  - **Popular explanations flagged separately:** they're included to be tested,
    not presented as causes. The app will say whether the price data supports
    them.
  - **Date precision recorded:** some events have an exact day, others only a
    month; tests in Milestone 4 shouldn't treat a month-level date as exact.
- **Not included:** general inflation (already handled by real prices) and
  events with no clear link to these meats.

## D29. Add a one-command data refresh and automated tests (2026-11-13)

- **Decided:** a new Milestone 6 before publishing:
  - move the download and cleaning code from notebooks 01–06 into `src/`
    (revised in D31: the notebooks keep their own code, and `src/` is verified
    to reproduce their results);
  - `python -m src.refresh` re-downloads every source and rebuilds every
    processed file, the master table and the data dictionary;
  - `pytest` data tests check the master table (one row per month, only known
    gaps, filled months flagged, shares add to 100%, sensible value ranges,
    every column documented);
  - GitHub Actions runs the tests on every push; a monthly job on the VPS runs
    the refresh, and new data is only used if the tests pass.
- **Why:** the project should keep working as new months are published, not
  be a one-time analysis. Automated checks catch problems like the ones found
  by hand in Milestone 1 (thousands commas, a mislabeled ERS column, the
  October 2025 gap) before they reach the app. Both are skills employers look
  for.
- **Notebooks stay:** they remain the readable, step-by-step record of how and
  why each step works.

## D30. Host the app on Scott's VPS, not Streamlit Community Cloud (2026-11-13)

- **Decided:** the app runs on Scott's own VPS and is featured on his
  portfolio site. This replaces the Streamlit Community Cloud plan in D12; the
  rest of D12 still holds (public repo; the app reads committed processed data
  and needs no API keys).
- **Why:** all of Scott's sites and apps are hosted on his VPS, and the
  portfolio site will link to each project. Self-hosting also makes the monthly
  scheduled refresh (D29) simple: it runs on the same server as the app.
- **What changes:** Milestone 7 (publish) now covers running Streamlit as a
  service behind the web server with HTTPS.

## D31. How the refresh and tests work (2026-11-13)

Scott asked me to make these calls while building Milestone 6; each can be revisited.

- **Notebooks keep their own code; `src/` is the production path.** Rewriting the
  notebooks to call `src/` would have changed files Scott has already reviewed and
  committed. Instead, `src/` was written from the notebooks' final code and **checked
  against them**: an offline refresh from the 2026-10-26 raw files reproduced every
  processed file and the master table exactly (largest difference about 6 × 10⁻¹⁴, i.e.
  rounding noise). If the two ever need to change, change `src/` and the notebook
  together. Item 6.1 is complete on this basis.
- **Build first, publish only if the checks pass.** The refresh builds everything in a
  temporary folder, runs the checks, and copies the files into `data/processed/` (and the
  data dictionary into `docs/`) only if every check passes. A failed refresh leaves the
  current data in place, so the app never shows unchecked data.
- **Raw downloads are kept, in dated folders,** as before (D9); `--offline` rebuilds
  from the latest saved raw files with no downloads, useful for testing and for re-running
  after a code change.
- **A refresh report** (`data/processed/REFRESH_REPORT.md`, committed) records which raw
  files were used, the check results, how many months the table gained, and any **revised
  past values** (>0.5%), since agencies sometimes revise earlier months.
- **The same checks run in both places** (`src/checks.py`): in the refresh before
  publishing, and in `pytest` on the committed data. Checks: one row per month from
  January 2010; no gaps except a short list of known ones (chicken's ERS January–March
  2026); columns start when they should (D27); values in sensible ranges (catches cents
  read as dollars, or a percent in a cents column, as in D23); spreads and shares add up;
  real prices match the CPI formula; filled months are flagged and rare; every column is
  in the data dictionary.
- **Known gaps are listed, not ignored.** A new gap fails the checks; if ERS later fills
  a known gap, nothing fails.
- **Pipeline unit tests** recreate the real problems found in Milestone 1 (thousands
  commas, the mislabeled pork column, the October 2025 gap) with tiny made-up tables, so
  each one would be caught if it came back.
- **GitHub Actions** runs the tests on every push using Python 3.12 and a small
  `requirements-test.txt` (pandas, requests, python-dotenv, pytest), so it's fast and
  needs no API keys.
- **Monthly refresh on the VPS** runs on the **20th of each month** at 06:00 (BLS and
  USDA have published the previous month by then), via `deploy/monthly_refresh.sh`. It's
  written now and installed in Milestone 7, when the app goes on the VPS.

## D32. Portfolio links to the GitHub repo for now; app hosting deferred (2026-11-14)

- **Decided:** Scott's portfolio (schirko.com/scott) will link to this project's
  public GitHub repository rather than a hosted app at schirko.com/scott/meat-prices.
  Hosting the app on the VPS (Milestone 7.1, D30) is deferred, not cancelled.
- **Why:** the app isn't built yet, and a running Streamlit app needs server setup
  (a service plus a web-server rule for the sub-path). The repo already shows the work:
  the README, documented decisions, notebooks with saved outputs, tests and the
  GitHub Actions badge of passing tests.
- **What this means:** the repo is now the project's front door, so the README's
  one-page summary and screenshots (item 7.2) matter more, and every notebook should
  be committed with its outputs saved so the charts show on GitHub.

## D33. How events are drawn and screened (2026-11-14)

- **Decided:**
  - An event that lasts more than a month is drawn as a shaded band; anything else is a
    line on its start date. A drought with no end date is still going on, so it runs
    to the latest month of data.
  - Popular claims are drawn dashed or faded, so they're never mistaken for
    established causes.
  - Each meat's chart shows only the events listed for that meat.
  - Notebook 08 screens each event with one number: the change in the
    **inflation-adjusted** price from the month before the event started to three
    months after. Each change is **ranked against every three-month change for that
    meat since 2015**.
- **Why:** a percent change on its own doesn't say whether it's unusual, because
  prices move about 2% in a typical three months. Ranking it against all the others
  puts it in context with no statistical model. Using real prices keeps general
  inflation from making every recent event look big.
- **Limits, handled in Milestone 4:**
  - Overlapping events can't be separated.
  - An event that lands on a rising trend ranks high even if it did nothing.
  - Slow effects such as drought don't fit a three-month window.
  - The 2020–2023 drought's −16% is an example: it measures the COVID spike fading,
    not the drought.
