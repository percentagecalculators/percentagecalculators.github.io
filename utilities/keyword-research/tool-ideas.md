# Tool ideas — from "percentage calculator" keyword research (2026-09-04)

Source data: `output/keyword_ideas_20260904_221224.xlsx` — 780 keyword ideas from Google Ads
`GenerateKeywordIdeas`, seeded with `"percentage calculator"`, global (no geo filter).

Ideas below are the 780 keywords clustered into distinct tool concepts, cross-checked against
the 10 calculators already live on this site (`index.html` + the 10 `/<calculator-name>/` pages
listed in the repo's own `CLAUDE.md`).

## Already built on this site — no action needed

| Tool | Folder |
|---|---|
| Percentage Calculator (basic: X% of Y / Y is what % of X) | `index.html` |
| Percentage Increase Calculator | `percentage-increase-calculator/` |
| Percentage Decrease Calculator | `percentage-decrease-calculator/` |
| Percentage Change Calculator | `percentage-change-calculator/` |
| Percentage Difference Calculator | `percentage-difference-calculator/` |
| Percent-Off / Discount Calculator | `percentage-off-calculator/` |
| Reverse Percentage Calculator | `reverse-percentage-calculator/` |
| Fraction to Percentage Converter | `fraction-to-percentage-calculator/` |
| Percentage Growth Calculator | `percentage-growth-calculator/` |
| Percentage Error Calculator | `percentage-error-calculator/` |
| Average Percentage Calculator | `average-percentage-calculator/` |

These absorb most of the top-volume queries (`percentage calculator` 1.83M, `percentage increase
calculator` 301K, `percentage difference calculator` 301K, `percentage change calculator` 165K,
`discount calculator` 110K).

## Net-new tool opportunities (not yet built)

Ranked roughly by combined keyword volume of the cluster.

### Health & fitness — EXCLUDED, different niche (biggest cluster by volume, 1.8M+, but out of scope)
Deliberately not building this cluster: different audience/vertical from percentage math (fitness
calculators, not math tools), different content needs (medical disclaimers, imperial/metric,
gender-specific formulas). Kept here only as a record of what was found and rejected — do not
add these to `CATEGORY_GROUPS` in `src/build_data.py`.
- Body Fat Percentage Calculator (Navy/Army method, height+weight or tape-measure input) —
  dominant sub-niche: `body fat calculator` 201K, `body fat percentage calculator` 90.5K, plus
  ~85 long-tail variants (army/navy/usmc method, men/women, chart lookups)
- BMI Calculator (with body-fat-% cross-reference) — `bmi percentage calculator` 3.6K
- Body Composition Calculator (muscle mass %, body water %) — smaller but same audience
- Weight Loss Percentage Calculator — `weight loss percentage calculator` 18.1K

### Education
- **GPA ↔ Percentage Converter** — `gpa to percentage` 18.1K + 24 variants (4.0 scale, cgpa,
  reverse direction)
- **CGPA ↔ Percentage Converter** (India-specific, distinct from GPA)
- **SGPA ↔ Percentage Converter** (India-specific) — `sgpa to percentage` 60.5K
- **Marks/Exam Percentage Calculator** — `marks percentage calculator` 49.5K + large long-tail
  (board-specific: CBSE, SSLC, SSC, matric, B.Tech, semester, attendance)
- **Percentile ↔ Percentage Converter** — 11 variants incl. GSEB-specific

### Finance
- **APY Calculator** (Annual Percentage Yield) — 49.5K, 21 variants (incl. crypto/Binance intent)
- **APR Calculator** (Annual Percentage Rate) + **APR ↔ APY Converter** — 40.5K
- **Simple Interest Calculator** / **Compound Interest Calculator**
- **Loan Interest Calculator** (some India-specific SBI intent — consider a generic version)
- **Profit Percentage Calculator** — `formula for percentage profit` 33.1K
- **Profit Margin Calculator**
- **Markup Percentage Calculator**
- **Gross Margin Calculator**
- **Salary Increase / Hike Percentage Calculator** — `salary increase percentage calculator` 5.4K
- **Commission Percentage Calculator**
- **Depreciation Percentage Calculator**

### Converters (small volume individually, cheap to build as a batch)
- **Decimal ↔ Percentage Converter**
- **Ratio ↔ Percentage Converter**
- **PPM ↔ Percentage Converter**
- **Basis Points ↔ Percentage Converter**
- **Slope % ↔ Degrees Converter**
- **Alcohol Proof ↔ Percentage (ABV) Converter**

### Niche / long-tail
- **Tip Percentage Calculator**
- **Win/Loss Percentage Calculator** (sports) — `calculate win rate` 14.8K
- **Percentage Point Calculator**
- **Baker's Percentage Calculator** (baking ratios)
- **Food Cost Percentage Calculator**
- **Percent Solution / Concentration Calculator** (chemistry — mass/volume %, molarity, dilution)

## Explicitly excluded (real search volume, not standalone-tool shaped)

- ~40 "formula/how-to" queries (`percentage increase formula`, `percent kaise nikale`) — content/
  blog fodder for existing calculator pages' FAQ or article sections, not separate tools
- "X ka Y percent" Hindi-phrased queries — same tool as the basic calculator, different phrasing
- Power BI / Excel "percent of total" queries — platform-specific how-to, not a web tool
- Off-topic noise from Google's broad keyword matching (`kcal to calories calculator`,
  `arr calculator`, `clock angle calculator`, `omni calculator percentage` — a competitor brand)

## Net count

**~28 net-new distinct tools** beyond the 10 already live, excluding the health & fitness cluster
above (some mergeable — e.g. GPA/CGPA/SGPA could ship as one "Academic Score Converter" with a
mode toggle, same pattern used for online-sound-test's tool taxonomy).
