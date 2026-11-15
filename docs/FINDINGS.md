# Findings and methods explained

This page brings the whole project together in plain language: what was found, how it
was found, what each method means, the problems caught along the way, and how to talk
about it. Each section points to the notebook with the code and the full results.

Numbers are for data through **September 2026**. "Real" means adjusted for inflation,
in September 2026 dollars.

---

## The story in one minute

> Since 2015, ground beef has risen 63% while prices in general rose 42%, so beef is
> 15% more expensive even after inflation. Pork and chicken actually got cheaper in real
> terms. I tested 16 events people blame, from plant fires to cyberattacks. Only the 2020
> COVID plant closures clearly moved all three meats, and that faded within months. None
> of the popular explanations hold up.
>
> What explains beef is the cattle herd. Drought pushed ranchers to sell off cows, the
> herd shrank 13% from its 2019 peak, and a 1% smaller herd goes with about a 1.8% higher
> real beef price. The shrinking herd alone predicts a 25% real price rise from 2019 to
> 2025; the actual rise was 28%. Drought accounts for roughly 40% of the herd loss.
> Ranchers' other choices account for the rest.
>
> It's built from free government data (BLS, USDA, the U.S. Drought Monitor), with one
> command to refresh it, automated data tests, and every decision documented.

---

## What was found

### 1. Beef is the outlier (notebooks 01, 05, 07)

| Since 2015 | Price change | After inflation |
|---|---|---|
| Ground beef | +63% | **+15%** |
| Chicken breast | +23% | −13% |
| Pork chops | +9% | −23% |
| All prices (CPI) | +42% | |
| Groceries (food at home) | +33% | |

**How it was found:** U.S. average retail prices from the Bureau of Labor Statistics, each
rebased so the 2015 average = 100 and divided by the Consumer Price Index to remove
inflation.

**How to explain it:** "Meat didn't all get expensive. Beef did. Pork and chicken rose
less than everything else, so they're actually cheaper than in 2015 once you allow for
inflation. Groceries overall rose less than prices in general."

### 2. Sudden events explain little (notebooks 08 and 11)

- **The 2020 COVID plant closures** are the only event that clearly moved all three meats:
  beef +11%, pork +17%, chicken +13% above where prices were heading. All three faded
  within months.
- **Chicken's 2022 spike** was real (+8% to +13%). It lines up with higher feed costs and
  the bird flu wave, which started together, so the data can't say which caused it.
  Feed costs didn't move pork or beef within six months. Chickens reach market weight
  in about seven weeks, so feed costs reach chicken prices much faster.
- **The popular claims don't hold up.**
  - The Colorado bird-flu culls and the cage-free egg law came in ordinary months.
  - The "food plant fires" claim lines up only with chicken's 2022 spike. Beef and pork,
    which the claim also covers, didn't move.
- **Beef:** apart from COVID, no sudden event clearly moved it. JBS, both Tyson plant
  events and the screwworm case show nothing. The May 2025 Mexican cattle import
  suspension (+6%) is borderline.

**How it was found:** for each event, a forecast of where the price was heading, compared
with what happened, and judged against ordinary months (see *Forecast and placebo test*
below).

**How to explain it:** "Big news events are easy to blame, but when you compare prices
with where they were already heading, almost none of them made a lasting difference. The
pandemic did, briefly. Beef's rise isn't a string of shocks; it's something slower."

### 3. The cattle herd explains beef (notebook 12)

| Link in the chain | What the data shows |
|---|---|
| Drought → sell-off | 10 more points of cattle country in severe drought means about 0.8 points more of the herd sold (roughly 245,000 cows), **in the same year** |
| Sell-off → herd | Selling more than about **9.6%** of the herd in a year shrinks it, by about 1.1% per extra point |
| Herd → price | A 1% smaller herd goes with about a **1.8% higher real beef price** |

- **The herd alone predicts beef's rise.** The herd shrank 11.8% from January 2019 to
  January 2025, which predicts a **+25%** real price rise; the actual rise was **+28%**.
- **Drought is the biggest single push, but not all of it.** With a normal 2020–2023
  drought, the herd would have lost about 40% less, and the 2025 real beef price would
  have been about 11 points lower. The rest came from ranchers' other choices:
  - selling more cows in 2019–2020, with little drought
  - sending heifers (young females) to slaughter in 2024–2025 instead of keeping them to
    grow the herd
- **2026 breaks the pattern.** Drought is nearly as widespread as in 2022, but cow
  slaughter is the lowest in the data: ranchers are keeping their cows. That may be the
  start of rebuilding. In the short run, rebuilding keeps beef *scarce*, because cows
  kept for breeding aren't turned into beef.

**How to explain it:** "Drought dries up pasture, so ranchers sell cows they can't feed.
Fewer cows means fewer calves for years, so less beef, so higher prices. I measured each
step separately. Together they account for almost all of beef's rise since 2019."

### 4. Ranchers are getting a bigger share of each beef dollar (notebooks 02 and 07)

Ranchers' share of each retail beef dollar rose from **43% in 2019 to 54% in 2025**.
That points to scarce cattle rather than wider margins for packers or stores as the main
driver of the latest rise. *(Item 4.2 will look at this more closely.)*

**How it was found:** USDA's meat price spreads, which follow a pound of beef from the
farm, through the packer (wholesale), to the store (retail).

---

## Methods explained

**Nominal vs. real prices.** *Nominal* is the price on the shelf at the time. *Real*
removes general inflation: each month's price is divided by the Consumer Price Index and
restated in today's dollars. A real increase means something got more expensive
*compared with everything else*.

**Rebasing (2015 = 100).** Dividing each series by its 2015 average and multiplying by
100 puts beef, pork, chicken and inflation on one scale. 163 means 63% above 2015.

**Price spreads.** USDA tracks the value of a pound of meat at three stages. The gaps
between them show how each retail dollar is split between the farm, the packer and the
store.

**Weighting drought by where the cows are.** Drought in a state with few cattle matters
less than drought in Texas or Nebraska. Each state's drought is weighted by its share of
the nation's beef cows (2019), giving one "cattle country" drought figure (D26).

**Forecast-based event test (notebook 11).**
1. Take the 3 years of prices before an event.
2. Fit a small time-series model (**AR(1) with a trend**: a straight-line trend, plus the
   tendency of a high month to be followed by another high month).
3. Forecast the next 6 months as if nothing had happened.
4. Measure the gap between actual and forecast prices.

The forecast stands in for "the world without the event".

**Placebo test, and why the model's own error range wasn't used.** Run the same test on
*every* month, events or not. An honest test should flag about 5% of ordinary months as
"shifts". The model's own 95% range flagged about **30%**, because it assumes the model is
exactly right. So each event's gap was instead compared with the gaps at ordinary months.
This is one of the main lessons of the project: always check how often a method raises
false alarms.

**P-value.** If there were really no effect, how often would we see a result this big by
chance? Below 0.05 (1 in 20) is the usual line for "unlikely to be chance". It is not the
probability that the finding is true.

**Straight-line fit (OLS) and R².** OLS finds the line that best fits the dots. The
**slope** is the size of the effect. **R²** is the share of the ups and downs the line
accounts for: 0 means none, 1 means all.

**Elasticity (log-log fit).** Fitting the log of price on the log of the herd makes the
slope a percent-for-percent effect. An elasticity of −1.8 means a 1% smaller herd goes
with a 1.8% higher price. It's bigger than 1 because people don't cut back much on beef
when it gets dearer, so the price has to rise further before buyers give up enough of it.

**Why yearly data for the chain, not monthly.** The herd is counted once a year, and
monthly drought and slaughter change slowly, so each month mostly repeats the one before.
Treating 12 such months as 12 separate facts would make results look far more certain
than they are. One row per year is more honest.

**Newey–West (HAC) correction.** Even yearly values are related to the year before. This
correction widens the uncertainty to account for that, so p-values aren't too optimistic.

**Robustness checks.** Two series that both trend over time can look related by
coincidence. The herd → price result was re-checked with a time trend included and using
year-to-year changes; it held up both ways.

**What-if (counterfactual).** Replace the 2020–2023 drought with a normal level, push
that change through the fitted links, and see how the herd and the price would have
differed. It assumes everything else stayed the same.

**Cross-correlation.** How closely two series line up when one is shifted in time. It
showed drought and cow slaughter line up best with no delay: ranchers respond within the
year.

---

## Problems caught along the way

Each is now covered by an automated test, so it can't come back unnoticed:

- **Thousands commas in USDA files.** Values like "1,234" were read as text and 10 values
  went missing. The loader now strips the commas.
- **A mislabeled USDA column.** A recent pork "farm to wholesale" column held percentages,
  not cents, so the project calculates that spread itself (D23).
- **A missing month.** The October 2025 government shutdown stopped BLS price
  collection. The gap is filled from the months on either side and flagged (D18).
- **Stray rows.** A drought week dated December 29, 2009, fell outside the data range,
  and USDA's "Other States" row would have double-counted cattle. Both are dropped.
- **A package that wouldn't install.** The planned change-point library (`ruptures`) has
  no Windows build for Python 3.14, so the event tests use statsmodels instead (D16,
  D34).

---

## How it's built

- **One-command refresh:** `python -m src.refresh` downloads everything, rebuilds the
  monthly table, runs the data checks, and only replaces the published data if every
  check passes. It writes a report of what changed.
- **23 automated tests**, run on every push by GitHub Actions. They check ranges, gaps,
  that the farm, packer and store shares add up to 100%, that every column is documented,
  and each problem above.
- **Every decision recorded** in DECISIONS.md: what was decided, why, and what else was
  considered.
- **This site** is rebuilt from the data and notebooks with `python -m src.build_site`.

---

## Questions an employer might ask

**"Does this prove the herd *caused* higher prices?"**
Not on its own. It shows a strong, consistent relationship that holds under robustness
checks, matches basic supply and demand, appears in two separate cattle cycles, and
predicts the actual rise closely. Other things (demand, imports, margins) also moved and
aren't fully separated out. I'd call it strong evidence, not proof.

**"Why not use machine learning?"**
The question is *why* prices rose, not predicting next month's price. With 12–16 years of
data, simple models whose every number can be explained and checked are more honest
than a complex model that would fit the noise.

**"What was the hardest part?"**
Two things. Messy source data: several USDA problems only showed up through careful
checks. And not fooling myself: the model's own error range would have called a third of
all ordinary months "events" until the placebo test exposed it.

**"What would you do with more time?"**
- Use decades of BLS and NASS history to firm up the herd → price link.
- Add beef import volumes.
- Finish the "who gets the dollar" analysis (item 4.2).
- Build the interactive app.

**"How do you keep it current?"**
One command refreshes the data, re-runs every check and only publishes if they pass.
Then the site rebuilds from the same data.

---

## Limits

- National averages; local prices differ.
- 12–16 years per measurement, so sizes are approximate.
- Overlapping events (for example feed costs and bird flu in 2022) can't be separated.
- The what-if assumes the links stay fixed.
- October 2025 is estimated because of the shutdown.

## Still to come

- **Item 4.5, the verdict:** are today's beef prices justified by the supply situation?
  It will bring in meat vs. inflation (4.1) and who gets each beef dollar (4.2).
- **The interactive app** (Milestone 5).
