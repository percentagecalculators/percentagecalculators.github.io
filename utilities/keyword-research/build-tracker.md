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

## Batch 2 — Finance: rates
- [ ] apy-calculator
- [ ] apr-calculator
- [ ] apr-apy-converter
- [ ] simple-interest-calculator
- [ ] compound-interest-calculator

## Batch 3 — Finance: business
- [ ] loan-interest-calculator
- [ ] profit-percentage-calculator
- [ ] profit-margin-calculator
- [ ] markup-calculator
- [ ] gross-margin-calculator

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
- Accent colors used so far: sky, purple, fuchsia, lime, yellow (batch 1). Remaining unused
  Tailwind stock colors for future batches: green (then colors start repeating across
  different nav categories, which is fine per CLAUDE.md — only same-category collisions
  are avoided).
