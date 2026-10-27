# Data sources

Where each data set comes from, what it contains, its limits, and how we get it.
This page is filled in as each data set is added in Milestone 1.

---

## The agencies behind the data

All of the data comes from U.S. government agencies. Their names and acronyms come up
throughout the notebooks, so here is who they are:

| Agency | Short for | Part of | What we use it for |
|---|---|---|---|
| **BLS** | Bureau of Labor Statistics | Department of Labor | Retail meat prices and the Consumer Price Index (items 1.1, 1.2, 1.7) |
| **ERS** | Economic Research Service | Department of Agriculture (USDA) | Meat price spreads: who gets each retail dollar (item 1.3) |
| **NASS** | National Agricultural Statistics Service | Department of Agriculture (USDA) | Cattle herd counts and cow slaughter (items 1.4, 1.5) |
| **AMS** | Agricultural Marketing Service | Department of Agriculture (USDA) | Not used directly; ERS gets its wholesale and farm prices from AMS |
| **USDM** | U.S. Drought Monitor | National Drought Mitigation Center (University of Nebraska–Lincoln), with USDA and NOAA | Weekly drought maps and statistics by state (item 1.6) |

**BLS** collects prices across the economy. Its average retail prices come from the same
store-by-store survey used to build the Consumer Price Index, the standard measure of
inflation.

**ERS** is USDA's research agency. Its economists study farming, food prices, trade and
rural economies, and publish free data sets and reports. For the meat price spreads, ERS
combines retail prices from BLS with wholesale and farm prices from AMS, then converts
them all to the same basis: cents per pound of meat as sold in stores. That conversion is
what makes a rancher's price for a live steer comparable with a shopper's price at the
store. ERS has published this series since the 1970s.

**NASS** runs USDA's farm surveys and censuses: how many cattle are on farms and ranches,
how many are slaughtered, crop production and more.

**AMS** reports daily and weekly market prices for livestock and wholesale meat, among
other things. We don't download from AMS ourselves; its prices reach us through ERS.

**The U.S. Drought Monitor** isn't a single agency: it's produced jointly by the National
Drought Mitigation Center at the University of Nebraska–Lincoln, USDA and NOAA (the
National Oceanic and Atmospheric Administration). Each week, experts combine rainfall,
soil moisture, streamflow and local reports into one map that classifies every area from
D0 (abnormally dry) to D4 (exceptional drought). USDA uses it to decide drought disaster
aid for ranchers.

---

## BLS average retail prices (Item 1.1)

- **Publisher:** U.S. Bureau of Labor Statistics
- **What it is:** monthly average U.S. retail price per pound for specific food
  items, collected as part of the Consumer Price Index survey
- **Access:** BLS Public Data API v2, `https://api.bls.gov/publicAPI/v2/timeseries/data/`
  (free key, stored in `.env`). With a key, one request can return up to 50
  series and 20 years.
- **Notebook:** `notebooks/01_bls_retail_prices.ipynb`
- **Raw file:** `data/raw/bls_prices_YYYYMMDD.json` (not committed; re-run the
  notebook to download)
- **Series ID format:** `APU` = average price, not seasonally adjusted; `0000` =
  U.S. city average; the rest is the item code.
- **Series used (decision D15):**

  | Meat | Series ID | Item |
  |---|---|---|
  | Beef | APU0000703112 | Ground beef, 100% beef, per lb |
  | Pork | APU0000FD3101 | All pork chops, per lb |
  | Chicken | APU0000FF1101 | Chicken breast, boneless, per lb |

- **Coverage:** January 2015 to September 2026 (as of the 2026-10-26 download).
  **October 2025 is missing from every BLS series**, most likely because of the
  federal government shutdown. Filled during cleaning with the average of
  September and November 2025 (D18).
- **Limits:** national averages only, no regional detail in the series we use;
  prices are what stores charge, so loyalty discounts and coupons are not fully
  reflected; one cut per meat stands in for that meat as a whole.

## BLS Consumer Price Index (Item 1.2)

- **Publisher:** U.S. Bureau of Labor Statistics
- **What it is:** monthly index of overall consumer prices, used to adjust for
  inflation
- **Series used:** CUUR0000SA0, CPI-U all items, U.S. city average, not
  seasonally adjusted (1982–84 = 100). Downloaded in the same request as the
  meat prices.

## USDA ERS meat price spreads (Item 1.3)

- **Publisher:** USDA Economic Research Service
- **Page:** https://www.ers.usda.gov/data-products/meat-price-spreads
- **What it is:** monthly farm, wholesale and retail values for Choice beef,
  pork and broilers (chicken), and the spreads between them, all in cents per
  pound of retail equivalent (the value per pound of meat as sold in stores)
- **Key terms: the three price stages.** For each meat, ERS estimates the value
  of one pound of meat (as sold in the store) at three stages of the supply
  chain. "Three values per meat" in the notebooks and decisions means these
  three stages, not three data sources:

  | Stage | Value | Who receives it | Beef | Pork | Chicken |
  |---|---|---|---|---|---|
  | Farm | **Net farm value** | The rancher or hog farmer (animal price minus hides and other byproducts) | ✓ | ✓ | not reported |
  | Wholesale | **Wholesale value** | The meatpacker or chicken processor | ✓ | ✓ | ✓ |
  | Retail | **Retail value** | The grocery store (what shoppers pay) | ✓ | ✓ | ✓ |

  The **spreads** are the gaps between stages: farm-to-wholesale (roughly the
  packer's part) and wholesale-to-retail (roughly the store's part). Each
  stage's **share** is its part divided by the retail value, so for beef and
  pork the farm, packer and store shares add up to 100%. Chicken has no farm
  value because most chickens are raised under contract for processors rather
  than sold at a farm price, so it has only the wholesale and retail stages.
- **Access:** CSV file downloads, no key (decision D21)
- **Notebook:** `notebooks/02_ers_price_spreads.ipynb`
- **Raw files:** `data/raw/ers_YYYYMMDD/` (not committed)
- **Files used:**

  | File | Covers | Last updated (as of 2026-10-26) |
  |---|---|---|
  | Historical monthly price spread data for beef, pork, broilers | 1970 to early 2026 | 2026-02-25 |
  | Choice beef values and spreads and the all-fresh retail value | Last 24 months (Oct 2024–Sep 2026) | 2026-10-14, monthly |
  | Pork values and spreads | Last 24 months | 2026-10-14, monthly |
  | Summary of retail prices and price spreads | Last 24 months; only current source for the broiler spread | 2026-10-14, monthly |

- **Layouts differ slightly:** historical and summary files use `Month` /
  `Month-number` (or `Month_Number`); beef and pork use `Period` /
  `Period_Number`, where 1–12 are months, 13–16 quarters and 17 the annual
  average.
- **Limits:**
  - Chicken has only a wholesale-to-retail spread, no farm value, because most
    chickens are raised under contract rather than sold at a farm price.
  - Spreads are gross margins between stages, not profits: they include the
    packer's and the store's costs (labor, energy, transport), not just profit.
  - Beef values are for Choice-grade beef; retail values are a weighted average
    of all cuts from the animal, not a single cut like ground beef.
  - Values of 1,000 or more are written with a thousands comma (`1,011.3`); the
    loader strips it.
  - The summary file carries only the latest 6 months of broiler spreads, so
    **chicken has no data for January–March 2026** (D22).
  - Chicken's units label changed in January 2025 ("Cents per retail pound" to
    "Cents per pound of retail equivalent"); the values continue smoothly, so
    it's a relabel, not a method change.
  - **Data error in the recent pork file:** "Pork price spread: farm to
    wholesale" contains the percent share instead of cents. We calculate it
    ourselves instead (D23).
- **Processed output:** `data/processed/ers_price_spreads_monthly.csv` (committed),
  long format: `date, meat, measure, value, units`, January 2015 to September
  2026. Measures: `retail`, `wholesale`, `net_farm`, `spread_farm_to_wholesale`,
  `spread_wholesale_to_retail`, `farmer_share_pct`, `packer_share_pct`,
  `store_share_pct`.

## USDA NASS cattle inventory (Item 1.4)

- **Publisher:** USDA National Agricultural Statistics Service
- **What it is:** number of cattle and beef cows in the U.S., reported each
  January 1 (and mid-year), plus monthly cow slaughter (item 1.5)
- **Access:** NASS Quick Stats API, `https://quickstats.nass.usda.gov/api/`
  (free key, stored in `.env` as `NASS_API_KEY`). Endpoints: `get_counts`
  (row count only) and `api_GET` (the data). Each request is limited to 50,000
  rows.
- **Notebook:** `notebooks/03_nass_cattle_inventory.ipynb`
- **Raw files:** `data/raw/nass_YYYYMMDD/` (not committed)
- **Years:** 2010 to now (D24)
- **Value codes:** numbers are written with thousands commas; `(D)` = withheld
  to avoid disclosing individual operations, `(NA)` = not available, `(Z)` =
  less than half the unit shown. Codes become missing values; the original
  text is kept in `value_raw`.
- **Series used (decision D25):**

  | Table | NASS series (`short_desc`) | Column |
  |---|---|---|
  | Herd, Jan 1 | CATTLE, INCL CALVES - INVENTORY | `all_cattle` |
  | Herd, Jan 1 | CATTLE, COWS, BEEF - INVENTORY | `beef_cows` |
  | Herd, Jan 1 | CATTLE, HEIFERS, GE 500 LBS, BEEF REPLACEMENT - INVENTORY | `beef_replacement_heifers` |
  | Slaughter, monthly | CATTLE, COWS, (EXCL MILK), SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN HEAD | `beef_cows_slaughtered` |
  | Slaughter, monthly | CATTLE, HEIFERS, SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN HEAD | `heifers_slaughtered` |
  | Slaughter, monthly | CATTLE, STEERS, SLAUGHTER, COMMERCIAL, FI - SLAUGHTERED, MEASURED IN HEAD | `steers_slaughtered` |

  Only rows with `domain_desc` = TOTAL are used (national totals).
- **Coverage:** herd every January 1 from 2010 to 2026; slaughter every month
  from January 2010 to September 2026. No suppressed (`(D)`) values.
- **Limits:** the July 1 inventory is incomplete (no report in 2013, 2016,
  2024), so only January is used; FI slaughter excludes the small share of
  cattle slaughtered in plants without federal inspection.
- **Processed outputs (committed):**
  - `data/processed/nass_herd_jan1.csv`: `year, reference_date, all_cattle,
    beef_cows, beef_replacement_heifers` (head)
  - `data/processed/nass_slaughter_monthly.csv`: `date, beef_cows_slaughtered,
    heifers_slaughtered, steers_slaughtered, heifer_share_pct,
    beef_cows_slaughtered_12mo`

## U.S. Drought Monitor (Item 1.6)

- **Publisher:** National Drought Mitigation Center (University of Nebraska–Lincoln),
  with USDA and NOAA
- **What it is:** weekly percent of each state's area in each drought category,
  D0 (abnormally dry) to D4 (exceptional drought)
- **Access:** statistics web service, no key:
  `https://usdmdataservices.unl.edu/api/StateStatistics/GetDroughtSeverityStatisticsByAreaPercent?aoi=<state FIPS>&startdate=M/D/YYYY&enddate=M/D/YYYY&statisticsType=1`
  (`USStatistics` with `aoi=conus` for the lower 48). JSON when requested with
  `Accept: application/json`, otherwise CSV.
- **Format used:** `statisticsType=1`, cumulative ("traditional"): each column
  is that category *or worse*, so D2 = % in severe drought or worse.
- **Notebook:** `notebooks/04_drought.ipynb`
- **Raw files:** `data/raw/drought_YYYYMMDD/` (not committed), including the NASS
  state beef cow counts used for the weights
- **Method (D26):** states holding at least 75% of U.S. beef cows on January 1,
  2019, weighted by those 2019 beef cows; weekly values averaged to months; DSCI
  = D0 + D1 + D2 + D3 + D4 (cumulative).
- **Checks in the notebook:** every week must satisfy D0 ≥ D1 ≥ D2 ≥ D3 ≥ D4,
  and all values must be between 0 and 100.
- **Processed outputs (committed):**
  - `data/processed/drought_cattle_country_monthly.csv`: `date,
    cattle_d2_plus_pct, cattle_dsci, conus_d2_plus_pct, conus_dsci`
  - `data/processed/drought_state_weights.csv`: the states used, their 2019
    beef cows and weights
- **Limits:** drought maps measure dryness, not pasture or hay conditions
  directly; weights reflect where cows were in 2019, not where they moved
  afterwards.
