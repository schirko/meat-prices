# Data sources

Where each data set comes from, what it contains, its limits, and how we get it.
This page is filled in as each data set is added in Milestone 1.

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
- **Series used:** _pending decision D15_
- **Limits:** national averages only; prices are what stores charge, so sales
  and coupons are not fully reflected. _More to add after reviewing the data._

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
  pork and broilers (chicken), and the spreads between them
- **Access:** spreadsheet download
- **Limits:** _to be filled in_

## USDA NASS cattle inventory (Item 1.4)

- **Publisher:** USDA National Agricultural Statistics Service
- **What it is:** number of cattle and beef cows in the U.S., reported each
  January 1 (and mid-year)
- **Access:** NASS Quick Stats API (free key)
