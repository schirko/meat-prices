# Presentation plan: "Why does meat cost so much now?"

> **Status (2026-11-20): built and published.** This is the outline the deck was built
> from. The finished deck has 14 slides: cover, hook, overall, beef, pork, chicken,
> events, claims, real cause, how it adds up, who got the money, verdict, what to watch,
> and how it was done. Every slide has speaker notes. Its charts are drawn by
> `src/presentation_charts.py`. View or download it at
> [schirko.com/scott/meat-prices/#presentation](https://schirko.com/scott/meat-prices/#presentation).
> D43 covers how it's published.

A story deck for a business audience, built from the project's findings (data through
September 2026). Each slide has one message (the headline), one visual, and what to say
over it. Length: about 12 slides, 10–12 minutes, plus an appendix for questions.

**Format:** a Claude slide deck, downloadable as PowerPoint (.pptx) or PDF.

**Story arc:** the hook → what happened overall → each meat → the events people blame →
the real cause → who got the money → the verdict → what to watch.

---

## 1. Title
- **Headline:** Why does meat cost so much now?
- **Subtitle:** Beef, pork and chicken prices, 2015–2026: what happened, why, and who got
  the money.
- **Visual:** none, or a faint version of the headline chart.

## 2. The hook
- **Headline:** Ground beef is up 63% since 2015; prices in general are up 42%.
- **Visual:** headline chart (`docs/images/headline.png`). Lines start at 100 in 2015;
  beef pulls away from "All prices."
- **Say:** "Everyone has noticed meat getting expensive. But it's not all meat, and the
  reasons aren't the ones you hear on the news."

## 3. Overall: only beef really got more expensive
- **Headline:** After inflation, beef is up 15%. Pork and chicken are cheaper than in 2015.
- **Visual:** a three-bar chart of the change after inflation: beef +15%, chicken −13%,
  pork −23% (notebook 13, test 1).
- **Say:** "Compared with everything else we buy, pork and chicken got cheaper. Beef is
  the one that needs explaining."

## 4. Beef: a long climb, not a spike
- **Headline:** Beef rose steadily, and steepest from late 2024.
- **Visual:** explorer view of ground beef, all years, with events shown (notebook 08,
  section 3, top panel).
- **Say:** "Apart from the 2020 COVID jump, beef doesn't jump at news events. It climbs."

## 5. Pork: one shock, then cheaper
- **Headline:** Pork's only big move was the 2020 COVID closures, and it faded within
  months.
- **Visual:** pork panel (notebook 08, section 3).
- **Say:** "Pork is 23% cheaper after inflation than in 2015."

## 6. Chicken: the 2022 spike came and went
- **Headline:** Chicken spiked in 2022 with feed costs and bird flu, then eased.
- **Visual:** chicken panel (notebook 08, section 3).
- **Say:** "Chickens reach market weight in about seven weeks, so feed costs show up in
  chicken prices quickly."

## 7. The events people blame
- **Headline:** Of 16 events, only the COVID closures clearly moved all three meats.
- **Visual:** dot chart of each event's effect against the normal range (notebook 11,
  section 4).
- **Say:** "For each event I projected where prices were already heading, then checked
  whether the gap was bigger than normal month-to-month swings."

## 8. Popular claims, checked
- **Headline:** Plant fires, Colorado culls, the cage-free law: none line up with a price
  jump.
- **Visual:** three short rows (claim → what the data shows).
- **Say:** "The plant-fire claim covers all meats, but only chicken moved, and chicken
  had other reasons."

## 9. The real driver: a cattle shortage
- **Headline:** Drought → ranchers sell cows → smaller herd → higher beef prices.
- **Visual:** four-panel chain chart (`docs/images/chain.png`).
- **Say (the three numbers):**
  - More drought means about 245,000 more cows sold that year.
  - Ranchers can sell about 1 in 10 cows a year and keep the herd steady; more than
    that and it shrinks.
  - A 1% smaller herd goes with a 1.8% higher beef price.

## 10. It adds up
- **Headline:** The shrinking herd predicts a 25% rise in beef since 2019; the actual rise
  was 28%.
- **Visual:** the herd-vs-price scatter (notebook 12, section 4).
- **Say:** "Drought caused about 40% of the herd loss. Ranchers' other choices caused the
  rest."

## 11. Who got the money
- **Headline:** Since 2019, ranchers got most of beef's increase; meatpackers got less.
- **Visual:** stacked bars of the rancher, packer and store parts of a pound of beef
  (notebook 13, section 3, or the explorer's "Who gets each dollar").
- **Numbers:** ranchers +$2.08 a pound, stores +$1.13, packers −$0.81.
- **Say:** "If packers were behind high beef prices, their part would grow. It shrank."

## 12. The verdict
- **Headline:** Mostly justified, with one thing to watch.
- **Visual:** the verdict table (pork ✓, chicken ✓, beef ✓ through 2025, 2026 flagged).
- **Say:** "In 2026 beef is about 11% above what the cattle shortage explains, and the
  extra shows up in store margins. That's not proof of overcharging, since store costs
  rose too, but it's worth watching."

## 13. What to watch next
- **Headline:** Ranchers are keeping their cows in 2026.
- **Say:** "If the herd starts growing, beef stays tight at first, then eases. The
  January 2027 herd count will tell us."

## Appendix (for questions)
- **A1. Data and method:** BLS, USDA ERS, USDA NASS, U.S. Drought Monitor; one-command
  refresh; 23 automated tests.
- **A2. How the event test works,** including the placebo lesson: the first method would
  have flagged 30% of ordinary months.
- **A3. Limits:** national averages; 12–16 years per step; overlapping events; spreads
  include costs.
- **A4. Links:** the project site, explorer and findings guide at
  schirko.com/scott/meat-prices.

---

## Notes for building it
- Charts: reuse the project's PNGs (`docs/images/`) and the notebook charts. Slides 3,
  8 and 12 are simple enough to rebuild natively.
- Every number above comes from `docs/FINDINGS.md`; check it against that file after
  each data refresh.
- Plain-language standard (D42): headlines a non-analyst can read on their own.
