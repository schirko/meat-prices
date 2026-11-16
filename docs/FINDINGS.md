# Findings and methods explained

This page explains the whole project in everyday language. You don't need a background
in statistics to follow it. Every term is explained the first time it comes up, and
there's a glossary near the end. If you want the technical details, they're in
*For the curious*, and each section names the notebook with the code and full results.

All numbers use data through **September 2026**.

---

## The short version

> **Question:** why does meat cost so much now, and are today's prices fair?
>
> **Beef is the only meat that really got more expensive.** Since 2015 ground beef went
> up 63%, while prices in general went up 42%. So even after allowing for inflation,
> beef costs about 15% more than it did. Pork and chicken went up *less* than everything
> else, so in practice they've become cheaper.
>
> **The news events people blame mostly didn't matter.** I checked 16 of them, from
> plant fires to a cyberattack. Only the 2020 COVID plant closures clearly pushed all
> three meats up, and that faded within months.
>
> **The real reason is a shortage of cattle.** Droughts dried up pasture, so ranchers
> sold off cows they couldn't feed. The U.S. herd shrank 13% from its 2019 peak, and
> fewer cows means less beef for years. The size of the herd explains almost all of
> beef's rise since 2019.
>
> **So are today's prices fair? Mostly yes.** The extra money from beef went mainly to
> ranchers, not to meatpackers or stores. The one exception is 2026: beef is now about
> 11% higher than the cattle shortage alone explains, and that extra shows up in what
> stores keep.

---

## Five ideas that make everything else easier

**1. "After inflation" (also called "real" prices).** Almost everything costs more
than it did ten years ago. To see whether beef *really* got more expensive, we compare it
with prices in general. If beef rose 63% and everything else rose 42%, beef got more
expensive *relative to everything else*, by about 15%. That's the "after inflation"
number. The ordinary price on the shelf at the time is the "nominal" price.

**2. "Percent" vs. "percentage points."** If ranchers sell 9% of their cows one year
and 10% the next, that's **1 percentage point** more (10 − 9), even though it's about
11% more cows. The project uses "points" whenever it compares two percentages.

**3. "Where prices were heading."** To tell whether an event changed prices, it isn't
enough to ask "did prices rise afterward?" They might have been rising anyway. So we
look at the trend *before* the event, project it forward, and compare what actually
happened with that projection. The gap is the event's effect.

**4. "Unusual, or just the normal ups and downs?"** Prices wiggle every month. A 3%
jump might be big, or it might happen all the time. So every result is compared with
what happens in ordinary months, when nothing in particular is going on. A change is
called **clear** only if it's bigger than what ordinary months produce 19 times out of 20.

**5. "Goes with" isn't the same as "causes."** Two things can rise together for many
reasons. When this page says "a smaller herd goes with higher prices," it means they
move together consistently. Whether one *causes* the other is a judgment based on how
strong, consistent and sensible the pattern is. Section 3 explains why the cattle
shortage passes that test.

---

## What was found

### 1. Beef is the only meat that really got more expensive

*Notebooks 01, 05 and 07*

**The question:** did all meat get expensive, or just some?

| Since 2015 | Price on the shelf | After inflation |
|---|---|---|
| Ground beef | up 63% | **up 15%** |
| Chicken breast | up 23% | down 13% |
| Pork chops | up 9% | down 23% |
| Prices in general | up 42% | |
| Groceries overall | up 33% | |

**How to read it:** the middle column is what you'd notice at the store. The right
column compares each meat with prices in general. Only beef is "up" after inflation.
Pork and chicken rose by less than everything else, so they now take a smaller share of
a household's money than in 2015.

**How we know:** monthly average prices that the Bureau of Labor Statistics (BLS)
collects from stores across the country, compared with the Consumer Price Index, the
government's standard measure of inflation.

**How sure are we:** very. These are direct measurements, not estimates.

**In one sentence:** "Meat didn't all get expensive; beef did. Pork and chicken are
actually cheaper than in 2015 once you allow for inflation."

### 2. The news events people blame mostly didn't matter

*Notebooks 08 and 11*

**The question:** plant closures, a cyberattack, bird flu, plant fires: did any of these
actually push prices up?

**What we found:**
- **The 2020 COVID plant closures** clearly pushed all three meats up: beef about 11%,
  pork about 17% and chicken about 13% above where they were heading. All three
  came back down within months.
- **Chicken's 2022 spike** was real, at about 8% to 13% above the trend. It came at the
  same time as higher animal-feed costs and a bird flu outbreak. Because both started
  together, we can't tell which mattered more.
- **The popular explanations don't hold up.** The Colorado bird-flu culls and the
  cage-free egg law came during ordinary months. The "food plant fires" claim lines up
  only with chicken's 2022 spike, while beef and pork, which the claim also covers,
  didn't move.
- **For beef, almost nothing sudden mattered.** The 2021 JBS cyberattack, both Tyson
  plant events and the screwworm case show no clear effect. The one possible exception
  is the May 2025 halt on cattle imports from Mexico (about 6%), and it's borderline.

**How we know:** for each event, we projected where prices were heading beforehand and
measured how far they ended up from that path over the next six months (idea 3). Then
we checked whether that gap was bigger than in ordinary months (idea 4).

**How sure are we:**
- **COVID:** very sure. It's the biggest change in the data, and it shows up for all
  three meats and with two different methods.
- **Chicken in 2022 and the May 2025 import halt:** probably real, but less certain.
- **Overlapping events:** some started too close together to separate.

**In one sentence:** "Big news events are easy to blame, but when you compare prices
with where they were already heading, almost none made a lasting difference. Beef's
rise is something slower."

### 3. A shortage of cattle explains beef

*Notebook 12*

**The question:** if sudden events don't explain beef, what does?

**The idea, as a chain of four steps:** drought dries up pasture and hay → ranchers
sell cows they can't afford to feed → the national herd shrinks → there's less beef
for years, so prices rise. Each step can be measured.

| Step | What the data shows, in plain terms |
|---|---|
| Drought → ranchers sell cows | In a year with more drought, more cows are sold. When drought covers an extra tenth of cattle country, ranchers sell about 245,000 more cows that year (just under 1% of the herd). They react within the year, not later. |
| Selling cows → smaller herd | Ranchers can sell about **1 in 10** of their cows each year and still keep the herd steady, because young females replace them. Sell more than that and the herd shrinks. |
| Smaller herd → higher price | When the herd is **1% smaller**, the price of beef (after inflation) is about **1.8% higher**. |

**Why the price rises faster than the herd shrinks (1.8% vs. 1%):** people keep buying
beef even when it gets more expensive. So when there's less of it, the price has to
climb quite a lot before enough buyers cut back to match the smaller supply.

**What it adds up to:**
- **The herd explains almost all of beef's rise.** From 2019 to 2025 the herd shrank
  about 12%. By the 1.8-to-1 rule, that predicts beef about 25% more expensive after
  inflation; the actual figure was 28%.
- **Drought is the biggest single cause, but not the only one.** If the 2020–2023
  drought had been an ordinary one, the herd would have lost about 40% fewer cows, and
  beef would have cost about 11 percentage points less. The rest came from ranchers'
  other decisions:
  - selling more cows in 2019 and 2020, when there was little drought
  - sending many young females (heifers) to slaughter in 2024 and 2025 instead of
    keeping them to grow the herd
- **2026 breaks the pattern.** Drought is nearly as bad as in 2022, yet ranchers are
  selling the fewest cows in the data: they're holding on to them. That may be the start
  of rebuilding the herd. Oddly, rebuilding keeps beef scarce at first, because cows kept
  for breeding aren't turned into beef.

**How sure are we:** fairly sure about the pattern, less sure about the exact sizes.
- **Why the pattern is believable:**
  - It holds in two separate cattle cycles (2011–2014 and 2019–2026).
  - It survives several cross-checks.
  - It matches basic supply and demand.
  - It predicts the actual rise closely.
- **Why the exact sizes are approximate:**
  - There are only 12–16 years of data per step.
  - Other things, such as demand and imports, also moved and aren't fully separated out.

**In one sentence:** "Drought made ranchers sell cows, fewer cows means less beef for
years, and that shortage explains almost all of beef's rise since 2019."

### 4. Who got the extra money: mostly ranchers

*Notebooks 02, 07 and 13*

**The question:** when you pay more for beef, who gets it: the rancher who raised the
animal, the meatpacker who processed it, or the store that sold it?

**How to read it:** the U.S. Department of Agriculture (USDA) tracks the value of a
pound of beef at each step: what the rancher is paid, what the packer sells it for, and
what the store charges. The gaps between those steps show each one's part of the price.
All amounts are after inflation, in today's dollars.

| Who | Change in their part of a pound of beef, 2019 to 2026 | Share of the increase |
|---|---|---|
| Rancher | up $2.08 | 86% |
| Store | up $1.13 | 47% |
| Meatpacker | **down** $0.81 | −33% |

The shares add up to 100%: the packers' loss offsets part of what ranchers and stores
gained.

**What it means:**
- **Through 2025, almost all of the increase went to ranchers.** That's what a cattle
  shortage looks like: scarce cattle sell for more.
- **Meatpackers were squeezed, not enriched.** They pay record prices for cattle but
  can't pass all of it on, so their part fell from $1.11 to $0.30 a pound.
- **Stores' part jumped in 2026,** by $0.50 a pound in one year.
- **Pork and chicken:** each step is within a few cents of 2019.

**One caution:** a store's part isn't all profit. It also pays for wages, rent,
electricity and spoiled stock. A bigger part could mean higher costs, higher profit or
both; this data can't tell which.

**In one sentence:** "If packers or stores were driving high beef prices, their part
would have grown. Through 2025 it didn't; the money went to ranchers. 2026 is the
exception: the store's part jumped."

### 5. The verdict: mostly justified

*Notebook 13*

**The question:** taking it all together, are today's prices justified? We used three
plain tests:
1. Did the meat rise faster than prices in general?
2. Did anyone in the middle take a bigger cut?
3. Does the cattle shortage explain the price?

| Meat | 1. vs. prices in general | 2. Who got the increase | 3. Explained by the shortage? |
|---|---|---|---|
| Ground beef | 15% more expensive | mostly ranchers; packers down; stores up in 2026 | yes through 2025; 2026 runs about 11% above |
| Pork chops | 23% cheaper | little change | not needed (it got cheaper) |
| Chicken breast | 13% cheaper | little change | not needed (it got cheaper) |

**The 2026 check, in plain terms:**
1. We used the herd-to-price rule from 2015–2025 to predict what beef "should" cost in
   2026, given how few cattle there are.
2. The prediction is about **$6.20 a pound**, and anything from $5.59 to $6.87 would be
   normal.
3. The actual 2026 average so far is **$6.90**, just above that range and about 11%
   above the prediction.
4. That extra lines up with the jump in the store's part of the price.

**What it means:**
- **Pork and chicken: justified.** Both are cheaper than in 2015 after inflation.
- **Beef: mostly justified, with a 2026 caveat.** The rise through 2025 is a real
  shortage, and the money went to ranchers. In 2026 beef got somewhat ahead of what the
  shortage explains. That isn't proof of overcharging, because store costs also rose,
  but it's the one part of today's beef price the shortage doesn't cover.

**In one sentence:** "Mostly yes. Pork and chicken got cheaper, and beef's rise is a real
cattle shortage, with one thing to watch: in 2026 beef got ahead of the shortage, and the
extra shows up in store margins."

---

## How to read the charts

**Lines starting at 100 (front page, explorer "All meats").** Each line is set to 100
at its 2015 average. A line at 163 means 63% higher than in 2015. Comparing a meat with
the dashed "All prices" line shows whether it rose faster or slower than inflation.

**Shaded bands and vertical lines (events).** A shaded band is an event that lasted a
while, such as a drought. A thin vertical line is a one-day event, such as a plant
closing. Dashed or faded marks are popular claims being checked, not established causes.
The number on each matches the event list.

**The four stacked panels (drought → cows sold → herd → price).** Read straight down a
column, year by year: drought on top, then cows sold, then the herd, then the beef
price. The same pattern rolls down the panels with a delay.

**Dots with a straight line through them (notebook 12).** Each dot is one year. The line
is the overall pattern. Dots close to the line follow it; dots far away are years
when something else was going on.

**Stacked bars ("Who gets each dollar").** The full height of a bar is the price of a
pound of beef that year. The colored layers show each step's part: rancher at the
bottom, packer in the middle, store on top.

**A dot with whiskers (notebook 13).** The hollow dot is the predicted 2026 price. The
whiskers show the range that would be normal. The red dot is what actually happened.
Red inside the whiskers means "as expected"; above them means "higher than the shortage
explains".

---

## Glossary

**Beef cow herd.** The female cattle kept to have calves, counted every January 1 by
USDA. It's the "factory" for future beef, so it changes beef supply for years.

**Clear shift / possible shift.** This project's labels for a change bigger than
ordinary months produce 19 times out of 20 (clear) or 9 times out of 10 (possible).

**Consumer Price Index (CPI).** The government's measure of how much prices in general
have risen. It's used here to adjust for inflation.

**Drought ("severe drought or worse").** From the U.S. Drought Monitor's weekly maps.
This project uses the share of cattle country in the worst three of its five levels,
giving more weight to states with more beef cows.

**Elasticity.** How many percent one thing changes when another changes by 1%. Here: a
1% smaller herd goes with a 1.8% higher price.

**Heifer.** A young female that hasn't had a calf. Keeping heifers grows the herd;
sending them to slaughter doesn't.

**Meatpacker (packer).** The company that buys cattle, processes them and sells beef
wholesale to stores.

**Nominal price.** The price on the shelf at the time, not adjusted for inflation.

**P-value.** A number from 0 to 1 that answers: if nothing real were going on, how often
would a result this big happen by chance? Small (below 0.05, or 1 in 20) means
"unlikely to be chance". It is *not* the chance that the finding is true.

**Percentage point.** The difference between two percentages (from 9% to 10% is 1
point).

**Placebo test.** Running the same check on ordinary months where nothing happened, to
see how often it raises a false alarm.

**Prediction range (95%).** The range a value should fall in 19 times out of 20 if the
usual pattern holds.

**Price spread.** The gap between the price at one step of the supply chain and the
next, for example between what a store pays and what it charges.

**R² ("R-squared").** How well a pattern fits, from 0 (not at all) to 1 (perfectly).
0.8 means the pattern accounts for about 80% of the ups and downs.

**Real price.** The price after removing general inflation, in today's dollars.

**Rebased (2015 = 100).** Setting each series to 100 at its 2015 average so different
things can be compared on one scale.

---

## For the curious: the methods in more detail

**Rebasing and real prices.** Each price is divided by its 2015 average and multiplied
by 100. Real prices divide each month's price by that month's CPI and multiply by the
latest month's CPI, so everything is in September 2026 dollars (D27).

**Weighting drought.** Each state's drought share is weighted by its share of U.S. beef
cows in 2019, giving one "cattle country" figure (D26).

**Event tests (notebook 11, D34).**
- **The forecast:** fit a small time-series model, an **AR(1) with a trend**, to the
  36 months before each event, then forecast the next 6 months. The model is a
  straight-line trend plus the tendency of a high month to be followed by another high
  month.
- **The gap:** the average difference between the actual and forecast prices.
- **Judging the gap:** it's compared with the same gap computed at every ordinary month
  since 2018, and the p-value is the share of ordinary months with a gap at least as
  big. The model's own 95% range would have flagged about 30% of ordinary months as
  shifts, so it wasn't used.
- **Second opinion:** a simpler forecast (the last month plus the average monthly
  change) gives the same verdict in 15 of 19 tests. The other 4 are borderline cases.

**The supply chain (notebook 12, D37).**
- **The fits:** each step is a straight-line (ordinary least squares, OLS) fit on one
  row per year. The herd → price step is fitted on logs, so its slope is an elasticity.
- **Why yearly:** monthly values move so slowly that neighboring months aren't
  independent.
- **Correcting the uncertainty:** the p-values use the Newey–West (HAC) correction,
  because each year is also related to the year before.
- **Robustness checks:** the herd → price result holds with a time trend added (−1.67)
  and in year-to-year changes (−1.59).
- **Timing:** a cross-correlation (how well drought and slaughter line up when one is
  shifted in time) finds the strongest link with no delay.
- **The what-if:** it replaces the 2020–2023 drought with the 2015–2019 average and
  carries that change through the fitted steps.

**The 2026 check (notebook 13, D38).** It's an *out-of-sample* test. The herd → price
fit uses 2015–2025 only, so 2026 is a year it hasn't seen, and the 95% prediction
range comes from that fit. Testing on unseen data is fairer than checking how well a
model fits the data it was built from.

---

## Problems caught along the way

Each is now covered by an automated test, so it can't come back unnoticed:

- **Commas in numbers.** USDA files write thousands as "1,234", which the computer read
  as text, and 10 values went missing. The loader now strips the commas.
- **A mislabeled USDA column.** A pork column labeled in cents actually held percentages,
  so the project calculates that number itself (D23).
- **A missing month.** The October 2025 government shutdown stopped price collection.
  The gap is filled from the months on either side and flagged as estimated (D18).
- **Stray rows.** A drought week dated outside the data range, and a USDA "Other States"
  row that would have double-counted cattle. Both are dropped.
- **A software package that wouldn't install** on Python 3.14, so the event tests use a
  different, standard package instead (D16, D34).

---

## How it's built

- **One command refreshes everything:** `python -m src.refresh`. It downloads the
  data, rebuilds the monthly table and runs the checks. It only replaces the published
  data if every check passes, and it writes a report of what changed.
- **23 automated tests**, run every time code is pushed to GitHub. Among other things,
  they check for gaps, values out of range, and that the rancher, packer and store parts
  add up to 100%.
- **Every decision is written down** in DECISIONS.md: what was decided, why, and what
  else was considered.
- **This site** is rebuilt from the data and notebooks with `python -m src.build_site`,
  including the interactive explorer. The explorer is plain JavaScript with the data
  built into the page, so it needs no server and no chart library.

---

## Questions an employer might ask

**"Does this prove the cattle shortage *caused* higher prices?"**
Not on its own. The pattern is strong and consistent, survives cross-checks, matches
supply and demand, shows up in two separate cattle cycles, and predicts the actual rise
closely. But demand, imports and margins also moved and aren't fully separated out. I'd
call it strong evidence, not proof.

**"Why not use machine learning?"**
The question is *why* prices rose, not predicting next month's price. With 12–16 years
of data, simple models whose every number can be explained and checked are more honest
than a complex model that would fit the noise.

**"What was the hardest part?"**
Two things. First, messy source data: several USDA problems only showed up through
careful checks. Second, not fooling myself: the first event test would have called a
third of all ordinary months "events" until the placebo test exposed it.

**"So are beef prices a rip-off?"**
Mostly no. Through 2025 the cattle shortage explains the rise, and the money went to
ranchers, not packers or stores. In 2026 beef got about 11% ahead of what the shortage
explains, and the store's part grew. That's worth watching, but the data can't separate
store costs from store profit, so I wouldn't call it gouging.

**"Weren't the big meatpackers to blame?"**
Not in this data. Their part of each pound of beef fell from $1.11 to $0.30 (in today's
dollars) between 2019 and 2026.

**"What would you do with more time?"**
- Use decades of BLS and USDA history to firm up the herd-to-price link.
- Add beef import volumes and tariffs.
- Look at store costs (wages, energy) to see how much of 2026's store increase they
  explain.
- Add the 2027 herd count and newer prices to see whether 2026's gap closes.

**"How do you keep it current?"**
One command refreshes the data, re-runs every check and only publishes if they pass.
Then the site rebuilds from the same data.

---

## Limits

- **National averages:** prices in your area may differ.
- **Few years:** 12–16 per measurement, so sizes are approximate.
- **Overlapping events:** some started too close together to separate, for example feed
  costs and bird flu in 2022.
- **The what-if:** it assumes nothing else changed.
- **One estimated month:** October 2025, because of the shutdown.
- **Price spreads include costs:** a store's or packer's part isn't all profit.
- **Two products:** USDA's spreads cover all fresh beef, while the BLS price is ground
  beef.

## Still to come

- **Watching 2026:** whether beef's gap above the shortage's prediction grows or closes,
  and whether ranchers keeping their cows shows up as a bigger herd in January 2027.
