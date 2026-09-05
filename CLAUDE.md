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
