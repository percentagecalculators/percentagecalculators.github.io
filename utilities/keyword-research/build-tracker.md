# Phase 2 build tracker

## Update 2026-09-05: Advanced Silo internal linking shipped
Two-pillar grid-based silo linking system is now live — see CLAUDE.md's "Internal Linking
Strategy — Advanced Silo (Grid-Based)" section for the full pillar/hub/supporter map and rules,
and `utilities/silo_linking/generate_silo_rotation.py` for the implementation. Runs as the last
build step (`build_data.py` → `generate.py` → `generate_silo_rotation.py`), rotates monthly via
`.github/workflows/silo-rotation.yml`. Also fixed a pre-existing bug in `generate.py`'s
`TOOL_ICON_RE` regex that silently fell back to the generic default icon on every related-card
grid, site-wide, since it never actually matched `class="icon h-5 w-5"` (only bare
`class="icon"`) — every tool's related-card now shows its own distinct icon.


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

## Batch 6 — Everyday & niche — DONE 2026-09-05 (all 6 batches complete — 41 tools live total)
- [x] percentage-point-calculator (core group; purple accent; distinguishes pp difference from relative % change)
- [x] tip-calculator (bill/tip%/split people, green accent)
- [x] win-loss-percentage-calculator (wins/losses/ties, yellow accent)
- [x] bakers-percentage-calculator (ingredient % of flour weight, orange accent)
- [x] food-cost-percentage-calculator (ingredient cost / menu price, red accent)
- [x] percent-solution-calculator (mass/volume % w/v, cyan accent)

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
- 2026-09-05: Batch 6 (Everyday & Niche + Core's percentage-point-calculator) shipped and
  verified in-browser — tip ($80 + 18% tip / 4 people -> $23.60/person) and percentage
  point (20% to 25% -> 5pp difference, 25% relative change) checked by hand. This closes
  out the ENTIRE tool-ideas.md backlog: all 6 batches done, site at 41 tools total
  (11 original + 30 new), all 5 nav categories fully built (no more "tools" placeholders
  anywhere in CATEGORY_GROUPS).
- Next phase (not started): write content_html + faq for all 30 new tools — that's a
  separate pass, deliberately deferred per the user's original instruction this round.
