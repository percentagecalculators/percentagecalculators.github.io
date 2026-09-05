# Phase 2 build tracker

Tracks the ~28 net-new tools from `tool-ideas.md` (health/fitness excluded — see that file).
Each batch: author `src/content/<slug>.json` (content_html left **empty** for now — to be
written in a later pass), add a `TOOL_ACCENTS` entry in `generate.py`, move the tool from
`CATEGORY_GROUPS[...]["tools"]` to `["slugs"]` + `TOOL_SLUGS`/`NAV_NAMES` in `build_data.py`,
rebuild, verify in browser, commit.

Status legend: `[ ]` pending · `[~]` in progress · `[x]` done

## Batch 1 — Education core (GPA/CGPA/SGPA + marks) — DONE 2026-09-05
- [x] gpa-to-percentage-calculator (4.0 scale, sky accent)
- [x] cgpa-to-percentage-calculator (10-point × 9.5, purple accent)
- [x] sgpa-to-percentage-calculator (10-point × 9.5, fuchsia accent)
- [x] marks-percentage-calculator (obtained/total split field, lime accent)
- [x] percentile-to-percentage-calculator (approx. 0.7×percentile+30, yellow accent — labeled as an estimate since percentile/percentage aren't formally convertible)

## Batch 2 — Finance: rates — DONE 2026-09-05
- [x] apy-calculator (green accent)
- [x] apr-calculator (cyan accent)
- [x] apr-apy-converter (indigo accent)
- [x] simple-interest-calculator (amber accent)
- [x] compound-interest-calculator (emerald accent)

## Batch 3 — Finance: business — DONE 2026-09-05
- [x] loan-interest-calculator (EMI amortization formula, red accent)
- [x] profit-percentage-calculator (profit % of cost price, orange accent)
- [x] profit-margin-calculator (profit % of selling price, blue accent)
- [x] markup-calculator (reverse: cost + markup% -> selling price, violet accent)
- [x] gross-margin-calculator (revenue/COGS framing, pink accent)

## Batch 4 — Finance: pay + misc
- [ ] salary-increase-calculator
- [ ] commission-calculator
- [ ] depreciation-calculator

## Batch 5 — Converters
- [ ] decimal-to-percentage-calculator
- [ ] ratio-to-percentage-calculator
- [ ] ppm-to-percentage-calculator
- [ ] basis-points-calculator
- [ ] slope-percentage-calculator
- [ ] alcohol-proof-calculator

## Batch 6 — Everyday & niche
- [ ] percentage-point-calculator (core group)
- [ ] tip-calculator
- [ ] win-loss-percentage-calculator
- [ ] bakers-percentage-calculator
- [ ] food-cost-percentage-calculator
- [ ] percent-solution-calculator

## Notes / decisions log
- 2026-09-05: health-fitness category removed from nav entirely (see git commit 3aded0b).
- content_html intentionally empty across this whole phase — article body content is a
  separate later pass, not blocking on tool/calculator functionality. `faq` left as `[]`
  for the same reason (no FAQ section renders until it's populated later).
- 2026-09-05: Batch 1 (Education) shipped and verified in-browser (dark + calculation
  correctness spot-checked on gpa-to-percentage-calculator and marks-percentage-calculator).
- 2026-09-05: Batch 2 (Finance rates) shipped and verified in-browser — compound interest
  ($1000, 5%, 3yr, monthly → $1161.47) and APY (5% nominal, monthly → 5.116%) both checked
  against the textbook formula by hand.
- Note: profit-percentage-calculator (% of cost price), profit-margin-calculator (% of
  selling price), markup-calculator (reverse direction: cost+markup%->price), and
  gross-margin-calculator (revenue/COGS framing) are deliberately 4 distinct but related
  tools — their formulas overlap by design (same as GPA/CGPA/SGPA), matching the 4 separate
  search-intent clusters in tool-ideas.md.
- 2026-09-05: Batch 3 (Finance business) shipped and verified in-browser — loan EMI ($20k,
  7.5%, 5yr -> ~$400.76/mo), profit margin ($40/$55 -> 27.27%), and markup ($40 + 30% ->
  $52) all checked by hand.
- Accent colors used so far (batches 1-3): sky, purple, fuchsia, lime, yellow, green, cyan,
  indigo, amber, emerald, red, orange, blue, violet, pink. No color repeats within Finance
  category yet (teal, green, cyan, indigo, amber, emerald, red, orange, blue, violet, pink
  = 11 of ~14 finance tools so far). Remaining unused chromatic colors for batch 4 (3 more
  finance tools): yellow(used in Education — fine, different category), lime(used in
  Education), fuchsia(used in Education), rose, sky(used in Education), purple(used in
  Education). Plan: batch 4 uses rose + two colors reused from Education (fine, cross-category
  reuse is allowed per CLAUDE.md).
