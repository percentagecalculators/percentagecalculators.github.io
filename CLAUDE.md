# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static site hosted on GitHub Pages at `percentagecalculators.github.io` — a collection of free,
client-side percentage calculator tools. This is the **current, active codebase** (Tailwind
redesign). There is an older, unrelated multi-language Bootstrap site archived under
`legacy-bootstrap-site/` (with its own `CLAUDE.md`) — do not confuse the two; it is not part of
the active build.

## Build pipeline (no framework, but not hand-authored HTML either)

- `src/content/<slug>.json` — one file per tool. This is the **single source of truth** for a
  tool's page: `meta_title`/`meta_description`, `h1`/`subtitle`/`hint`, `card.fields_html` (the
  tool card's entire markup), `script` (that tool's self-contained vanilla JS), `content_html`
  (below-the-fold article body, later split at each `<h2>`), and `faq`.
- `src/content/pages.json` — static pages (About, Contact, Privacy, Terms, Disclaimer).
- `python3 src/build_data.py` — aggregates `src/content/*.json` into `src/data/{tools,site,pages}.json`
  (adds nav grouping, related-tool links, etc.). **Run this first** after editing anything in
  `src/content/`.
- `python3 src/generate.py` — reads `src/data/*.json` + `src/template*.html`, renders and minifies
  into `public/*.html`. Use `--no-minify` for readable output while iterating.
- **Always run both, in order, after touching `src/content/` or `src/data/`.** Editing
  `src/content/*.json` alone does nothing to `public/` until both steps run.
- Styling is Tailwind via the Play CDN (`<script src="https://cdn.tailwindcss.com">`) — no compiled
  Tailwind build, no PostCSS. `src/base.css` → `public/base.min.css` carries ONLY what Tailwind
  utilities can't express: `@font-face` rules and the light/dark CSS custom-property color tokens
  (`--color-bg`, `--color-accent`, etc.) that `TAILWIND_CONFIG` in `generate.py` exposes as
  semantic Tailwind color names (`bg`, `surface`, `border`, `text`, `accent`, ...). Everything else
  is Tailwind utility classes written directly in the templates/content.

## Local preview

```
cd public && python3 -m http.server 8080
```
No build step needed for that — it serves whatever is currently in `public/`.

## The `[hidden]` + `flex`/`grid`/`block` gotcha (learned the hard way)

**Never add a `flex`, `grid`, `block`, `inline`, etc. Tailwind display-utility class directly onto
an element that is also toggled via the `hidden` HTML attribute** (e.g. the home page's tab
panels, `<div class="tab-panel ..." hidden>`). Tailwind's `.flex{display:flex}` is an *author*
stylesheet rule; the browser's `[hidden]{display:none}` is a *user-agent* stylesheet rule. Author
rules always beat user-agent rules regardless of specificity, so adding `flex` to a hidden element
silently un-hides it. This broke the home page's tab switching once already (all 3 tabs rendered
at once) — see git history on `percentage-calculator.json`. If a hidden-toggled element needs to
become a flex container when visible, toggle the class itself in JS (e.g. swap `hidden` for
`hidden:hidden flex` isn't valid Tailwind either — just toggle `hidden` via the `hidden` DOM
property, never pair a permanent `flex` class with a permanent `hidden` attribute on the same
element).

## Tool-card design system

Every tool page's centerpiece is its calculator card, rendered from that tool's own
`card.fields_html` in `src/content/<slug>.json`. **Every tool gets its own accent color** (not a
single global color) so each page reads as its own branded module rather than a cloned template,
while every card still shares one consistent, professional component system. When adding a new
tool, follow this pattern exactly — copy an existing similar tool's `fields_html` as a starting
point rather than reinventing it.

### 1. Assign an accent color

Add the new tool's slug to `TOOL_ACCENTS` in `src/generate.py` (used both for its related-card tint
elsewhere on the site and for its own card, per below). Pick a Tailwind stock color not already
used by another tool in the same nav category if possible: `emerald, blue, rose, violet, amber,
orange, cyan, red, indigo, pink, teal` are already taken — pick another (`lime, sky, fuchsia,
yellow, purple, green, ...`).

```python
TOOL_ACCENTS = {
    "percentage-calculator": "emerald",
    "percentage-increase-calculator": "blue",
    ...
    "my-new-calculator": "sky",   # <-- add here
}
```

Everywhere below, `{c}` means that tool's chosen color slug, and every color utility needs BOTH a
light-mode and `dark:` variant (raw Tailwind palette colors are not theme-aware custom properties
like `accent`/`border`/etc. — they need explicit `dark:` pairs).

### 2. Tool-card head — icon badge

```html
<div class="tool-card-head flex items-center gap-3 border-b border-border bg-surface-alt px-5 py-4 sm:px-6">
  <span aria-hidden="true" class="icon-badge flex h-10 w-10 flex-none items-center justify-center rounded-xl bg-{c}-100 text-{c}-600 dark:bg-{c}-500/15 dark:text-{c}-400">
    <svg class="icon h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="..."/></svg>
  </span>
  <div class="min-w-0">
    <h1 class="text-base font-bold leading-snug text-text sm:text-lg">{{H1}}</h1>
    <p class="mt-0.5 truncate text-xs text-text-muted sm:text-sm">{{HINT}}</p>
  </div>
</div>
```

The icon SVG itself carries no color/size classes beyond `icon h-5 w-5` — the colored badge
wrapper does all the work. This also means each tool's badge/icon combo should be visually
distinct; don't reuse another tool's icon path.

### 3. Field labels ("eyebrow" style)

```html
<label for="..." class="text-xs font-semibold uppercase tracking-wide text-text-muted">Field Name</label>
```

### 4. Inputs (and the input-row + unit-suffix variant)

```html
<input type="number" id="..." step="any" placeholder="..." oninput="calculate()"
  class="w-full rounded-xl border border-border bg-surface-alt px-4 py-3 font-mono text-base text-text shadow-sm transition duration-150 placeholder:text-text-muted hover:border-border-strong focus:border-{c}-500 focus:outline-none focus:ring-4 focus:ring-{c}-500/15 dark:focus:border-{c}-400 dark:focus:ring-{c}-400/15">
```

For a field with a `%`-suffix sitting next to it (`input-row flex items-center gap-2.5` wrapper),
the input gets `w-full flex-1` prepended to the same class list above, and the suffix is a colored
chip, not a bare muted character:

```html
<div class="input-row flex items-center gap-2.5">
  <input class="w-full flex-1 rounded-xl border ... (same as above)">
  <span class="unit flex-none rounded-lg bg-{c}-50 px-3 py-1.5 text-sm font-bold text-{c}-700 dark:bg-{c}-500/15 dark:text-{c}-300">%</span>
</div>
```

A multi-value `<textarea>` (e.g. average-percentage-calculator) uses the same visual language, just
with `min-h-[110px] resize-y` instead of the single-line padding assumptions:

```html
<textarea id="..." placeholder="..." oninput="calculate()"
  class="w-full min-h-[110px] resize-y rounded-xl border border-border bg-surface-alt px-4 py-3 font-mono text-base text-text shadow-sm transition duration-150 placeholder:text-text-muted hover:border-border-strong focus:border-{c}-500 focus:outline-none focus:ring-4 focus:ring-{c}-500/15 dark:focus:border-{c}-400 dark:focus:ring-{c}-400/15"></textarea>
```

Never leave an input/textarea with no classes at all (this happened once — a completely unstyled
`<textarea>` relying on raw browser defaults). Every field must get the full treatment above.

A side-by-side split field (e.g. numerator/denominator) uses a `/` divider between the two
`calc-field` columns:

```html
<div class="calc-divider hidden self-center pt-6 text-2xl font-semibold text-text-muted/60 md:block">/</div>
```

### 5. Results panel

Wrap the whole results block in a colored, tinted panel (not just a plain top border):

```html
<div class="calc-results mt-auto space-y-2.5 rounded-xl border border-{c}-100 bg-{c}-50/60 p-4 dark:border-{c}-500/20 dark:bg-{c}-500/[0.06]">
  ...secondary rows...
  ...primary row...
</div>
```

**Secondary rows** (supporting detail, e.g. "Absolute Difference", "You Save") — small, muted,
uppercase label + a plainly-styled `<output>`:

```html
<div class="calc-result-row flex items-baseline justify-between gap-4">
  <span class="label text-xs font-semibold uppercase tracking-wide text-text-muted">Label:</span>
  <output class="value font-mono text-sm text-text-secondary" for="input_id_1 input_id_2" id="secondary_id">–</output>
</div>
```

**The primary row is the hero** — the one number the user came for. Bigger, bolder, colored, and (if
there is at least one secondary row above it in the same panel) visually separated by a divider:

```html
<!-- when there IS at least one secondary row above it in this panel -->
<div class="calc-result-row primary mt-1 flex items-center justify-between gap-4 border-t border-{c}-200/70 pt-3 dark:border-{c}-500/20">
  <span class="label text-sm font-semibold text-text-secondary">Label:</span>
  <output class="value text-3xl font-extrabold tracking-tight text-{c}-600 dark:text-{c}-400" for="..." id="result">–</output>
</div>

<!-- when the primary row is the ONLY row in the panel (no divider — nothing to separate from) -->
<div class="calc-result-row primary flex items-center justify-between gap-4">
  <span class="label text-sm font-semibold text-text-secondary">Label:</span>
  <output class="value text-3xl font-extrabold tracking-tight text-{c}-600 dark:text-{c}-400" for="..." id="result">–</output>
</div>
```

Use `<output for="space separated input ids">`, never `<span>`, for any computed/calculated value —
`<output>` is the HTML5 element made for exactly this ("the result of a calculation performed by a
script"), and it also carries an implicit `role="status"` (live region) for free.

The footnote formula line stays a subtle, small sibling *after* `.calc-results`, not inside it:

```html
<p class="calc-formula mt-3 text-center font-mono text-xs text-text-muted/80" id="formula_display"></p>
```

### 6. Placeholder / empty state

Before the user has entered valid input, every `<output>` should start (and — if you touch the
tool's `calculate()` JS reset branch — reset to) an en dash `–`, never a bare `?`. This is a static
HTML content choice (the initial `>–</output>` in `fields_html`); it's fine to leave the JS
`calculate()` reset logic alone unless you're already touching that file for another reason.

### 7. Equal card height vs. the related-tools grid

The tool card and the 2×2 related-tools grid sit in one shared CSS grid row
(`template.html`, no `items-start`, so it stretches to the taller column). For that stretch to
visually reach a *shorter* card, give that tool's own markup (not the shared template) `h-full
flex-col` on `.tool-card`, `flex-1 flex-col` on `.tool-card-body`, and `mt-auto` on `.calc-results`
(so any extra height becomes breathing room above the results panel, not blank space at the very
bottom). Copy this from any existing tool's `fields_html` rather than reinventing it. Do **not**
add `flex`/`flex-col` to anything carrying a `hidden` attribute (see the gotcha above) — the home
page's per-tab `<div class="tab-panel ...">` wrappers must NOT get this treatment; only
`.tool-card`/`.tool-card-body` (which never have `hidden`) do.

### 8. Verify before calling it done

After any card-styling change, rebuild (`build_data.py` then `generate.py`) and actually look at the
page — in a browser, both light and dark mode, ideally more than one tool for comparison. A CSS
diff that "should" look right and one that's actually been screenshotted are not the same thing.

## Internal Linking Strategy — Advanced Silo (Grid-Based)

Two-pillar Advanced Silo internal-linking system (Kyle Roof methodology), adapted from
`mic-tests.github.io`'s own silo implementation. Unlike that site, the link carrier here is
**the existing "related tools" card grid** (`aside.related-tools`, rendered by
`render_related_calculators()` in `src/generate.py`, styled with `template.html:62`'s
`{{RELATED_CALCULATORS}}` slot) — not inline sentence links inside article body copy. Each grid
card *is* the silo link. This was a deliberate choice for this site: the grid exists at the same
fixed location on every page regardless of whether that page's `content_html` has been written
yet, so the silo system works for all 41 tools immediately, with no dependency on the (still
largely unwritten) article content for the 30 tools added in the Phase 2 expansion.

**Full plan reference:** `/Users/buzzsubash/.claude/plans/curious-hatching-aurora.md` (this
session's approved plan — includes the full rationale, alternatives considered, and the
mic-tests comparison in more detail than this summary).

### Pillars, hubs, supporters

| Pillar | File | Keyword | Volume |
|---|---|---|---|
| Pillar 1 | `index.html` (percentage-calculator) | "percentage calculator" | 1,830,000/mo |
| Pillar 2 | `percentage-difference-calculator.html` | "percentage difference calculator" | 301,000/mo |

**Pillar 1's hubs** (utility/conversion/education theme):

| Hub | File | Keyword | Volume | Supporters |
|---|---|---|---|---|
| A — Converters | `fraction-to-percentage-calculator.html` | "fraction to percentage" cluster | ~6,600/mo | decimal-to-percentage-calculator, ratio-to-percentage-calculator, ppm-to-percentage-calculator, basis-points-calculator, slope-percentage-calculator, alcohol-proof-calculator |
| B — Education | `sgpa-to-percentage-calculator.html` | "sgpa to percentage" | 60,500/mo | marks-percentage-calculator, gpa-to-percentage-calculator, cgpa-to-percentage-calculator, percentile-to-percentage-calculator |
| C — Everyday | `win-loss-percentage-calculator.html` | "calculate win rate" | 14,800/mo | tip-calculator, bakers-percentage-calculator, food-cost-percentage-calculator, percent-solution-calculator |

**Pillar 2's hubs** (comparison/finance theme):

| Hub | File | Keyword | Volume | Supporters |
|---|---|---|---|---|
| D — Core comparison | `percentage-increase-calculator.html` | "percentage increase calculator" | 301,000/mo | percentage-decrease-calculator, percentage-change-calculator, percentage-off-calculator, reverse-percentage-calculator, percentage-error-calculator, average-percentage-calculator, percentage-point-calculator |
| E — Finance/Interest | `apy-calculator.html` | "apy calculator" | 49,500/mo | apr-calculator, apr-apy-converter, simple-interest-calculator, compound-interest-calculator, loan-interest-calculator, percentage-growth-calculator |
| F — Finance/Profit | `profit-percentage-calculator.html` | "formula for percentage profit" | 33,100/mo | profit-margin-calculator, markup-calculator, gross-margin-calculator, salary-increase-calculator, commission-calculator, depreciation-calculator |

2 pillars + 6 hubs + 33 supporters = 41 (every currently-built tool). No cross-pillar bridging —
the two pillar groups rotate and bridge fully independently.

### Grid link counts (strict — matches the classic methodology exactly)

| Page type | Card count | Rule |
|---|---|---|
| Pillar | exactly 1 | links to whichever of its 3 hubs is first in that month's shuffle. This hoards all authority on the pillar — it never links to more than one hub, and never to a supporter directly. |
| Hub | 3 or 4 | up to its pillar (always) + left neighbor hub (empty if this hub is first in the pillar's shuffled order) + right neighbor hub (empty if last) + down to the first supporter in its own shuffled chain (always). Only the *middle* hub of each pillar's 3-hub group gets all 4; first/last hubs show 3. |
| Supporter | 2 or 3 | up to its hub (always) + prev-or-next in its shuffled chain + next-or-bridge (a forward/backward bridge to the adjacent hub's first/last supporter, when this supporter sits at the start/end of its own chain). Only the true endpoints of the *whole pillar's* chain (first supporter of the first hub, last supporter of the last hub) show 2; everything else shows 3. |

Anchor text = each card's existing visible title (`nav_name`), which is already close to the
target page's primary keyword by construction (e.g. "GPA to Percentage Calculator") — no
"click here" / generic labels.

**Hard rules (enforced by the script, audited by `--dry-run`):**
- A supporter's cards never link directly to a pillar
- A hub never links to a different hub's supporters
- No page ever links to itself, and no page ever shows the same target twice
- No cross-pillar leakage except the pillar page's own single hub-link (which stays within its
  own 3-hub group) — a page under Pillar 1 never links to anything under Pillar 2's silo, or
  vice versa

### Build order (unchanged habit, now with one more step)

`python3 src/build_data.py` → `python3 src/generate.py` →
`python3 utilities/silo_linking/generate_silo_rotation.py` (**last**, always). The rotation
script patches the already-minified `public/*.html` files in place — `generate.py`'s
`minify_html_dir()` runs html-minifier-terser with `--remove-comments`, so injecting the
`<!-- SILO_START:grid -->...<!-- SILO_END:grid -->` markers before that step would strip them.
Re-running `generate.py` without re-running the rotation script afterward reverts every page's
related-tools grid back to the generic same-category picks baked into `render_related_calculators()`.

**Run manually:**
```bash
python3 utilities/silo_linking/generate_silo_rotation.py --dry-run   # preview, no writes
python3 utilities/silo_linking/generate_silo_rotation.py              # apply
```

### Monthly rotation (GitHub Actions)

`.github/workflows/silo-rotation.yml` — `cron: '0 16 1-3 * *'` (midnight SGT, days 1–3 as a
retry safety net) + `workflow_dispatch`. Runs the rotation script against committed
`public/*.html` and commits only if `git diff` shows changes, using the built-in `GITHUB_TOKEN`.
This repo has no other GitHub Actions workflows — GitHub Pages serves the committed `public/`
directly via repo settings, so the workflow's commit to `main` is picked up the same way any
other commit is.

### Known trade-off vs. the strict methodology

Deliberately different from a body-content silo (and from `mic-tests.github.io`'s own
implementation): these links live in a sidebar-style card widget next to the tool card, not
inline inside the main article body. The classic Advanced Silo methodology's rationale for
body-content-only links is that search engines discount nav/sidebar/footer links as
navigational. This was a conscious trade-off made this session in exchange for not needing
`content_html` written for the 30 new tools first — see the plan file referenced above for the
full discussion. Writing real article content for those 30 tools (a separate, still-pending
pass — see `utilities/keyword-research/build-tracker.md`) would make a future move to
body-content links possible, but is not required for the grid-based system to keep working.

## Article content styling (content_html)

Tool pages' `content_html` (and info pages' `sections`) is authored by an external SEO content
pipeline (`utilities/publish_seo_content.py` splices `output/<slug>/content.html` into each
tool's `content_html` field — see that script's own docstring) as **bare semantic HTML**, no
inline Tailwind classes. Both `template.html` and `template-page.html` wrap this content in a
shared `.article` class (`ARTICLE_PROSE_CLASSES` in `generate.py`, reused via the
`{{ARTICLE_PROSE_CLASSES}}` token so both templates stay in sync) combining Tailwind's typography
plugin (`?plugins=typography` on the CDN script tag — headings/p/lists/links/strong/em/code/table
cells/blockquote/hr) with plain CSS rules in `base.css` for everything Typography leaves at
browser defaults: `aside` (styled as a callout box), `details`/`summary` (styled as an expandable
card with a +/− toggle), `dl`/`dt`/`dd` (styled as a glossary), and `b`/`img`. Tables get a
`.table-scroll` wrapper + header/border treatment — the wrapper itself is added by existing
client-side JS (`wrapTables()` in both templates, runs on `DOMContentLoaded`), not at build time;
don't re-add a Python-side wrapper for this, it already exists and would just double up.

**Math formulas:** the pipeline emits LaTeX (`$$...$$` for display math, `\(...\)` for inline —
**never** single-`$`, since the site is full of literal dollar amounts like "$5,000" that would
otherwise be misparsed as math delimiters). Both templates load KaTeX + the auto-render extension
from jsdelivr and call `renderMathInElement()` on every `.article` element on `DOMContentLoaded`
(see `renderMath()` in each template's script block) — this runs client-side against the already
-built static HTML, so no server-side math rendering is needed. Verified: KaTeX's default styling
inherits `color` from its container, so formulas theme correctly in dark mode with no extra CSS.
