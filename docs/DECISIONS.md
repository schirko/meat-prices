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
- **Open question:** whether to keep an "All meats" comparison option in the
  selector, or only in the verdict section.
