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

## Batch 4 — Finance: pay + misc — DONE 2026-09-05 (Finance & Business category complete: 14 tools)
- [x] salary-increase-calculator (rose accent)
- [x] commission-calculator (sky accent, reused from Education — different category, fine)
- [x] depreciation-calculator (straight-line method, lime accent, reused from Education)

## Batch 5 — Converters — DONE 2026-09-05 (Converters category complete: 7 tools)
- [x] decimal-to-percentage-calculator (teal accent)
- [x] ratio-to-percentage-calculator (A as % of A+B total, ":" divider, amber accent)
- [x] ppm-to-percentage-calculator (÷10,000, emerald accent)
- [x] basis-points-calculator (÷100, indigo accent)
- [x] slope-percentage-calculator (rise/run -> slope% + angle in degrees, orange accent)
- [x] alcohol-proof-calculator (US proof ÷2 = ABV%, red accent)

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
- 2026-09-05: Batch 4 (Finance pay + misc) shipped and verified in-browser — salary increase
  ($60k + 5% -> $63,000), commission ($5000 x 10% -> $500), and depreciation ($10k asset,
  $1k salvage, 5yr -> $1800/yr, 18%) all checked by hand. Finance & Business category is
  now fully built out at 14 tools (percentage-growth-calculator + 13 new).
- Accent colors: Finance category uses teal, green, cyan, indigo, amber, emerald, red,
  orange, blue, violet, pink, rose (12 distinct, no repeats) plus sky and lime reused from
  Education (different category, fine per CLAUDE.md).
- 2026-09-05: Batch 5 (Converters) shipped and verified in-browser — slope (rise 5, run 100
  -> 5%, 2.86°) and ratio (3:4 -> total 7, 42.86%) checked by hand. Converters category is
  now fully built out at 7 tools (fraction-to-percentage-calculator + 6 new).
