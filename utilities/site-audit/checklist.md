# Site audit checklist (templates + all built pages)

Scope: `src/template*.html`, `src/generate.py`, `src/base.css`, and every built page in `public/`
(19 languages). Out of scope for this round: title-case/heading wording and unique-content checks.

Method: audit one item, fix it, rebuild, re-audit, mark it done, only then start the next.
Status: `[ ]` todo, `[~]` in progress, `[x]` done (fixed + re-verified).

## Round 1

- [x] **1. SEO / technical HTML audit**: broken links; `.html` vs extensionless link consistency;
      menu + footer identical across pages; viewport; missing title/description; reversed
      attribute order (`content` before `name`, `href` before `rel`); canonicals; sitemaps;
      invalid HTML characters. No twitter/og tags needed.
- [x] **2. Unclosed / truncated tags** in every page: html, head, body, script, style, and all others.
- [x] **3. HTML consistency**: font family/size/colour, paragraph classes, H1-H3 order and classes per
      template, page-width layout (container classes) across all templates/pages.
- [x] **4. CSS coverage, no browser defaults**: every element used in every template/page is styled
      in the site's CSS (not relying on UA defaults); checked for all templates, not a sample.
- [x] **5. Navigation**: mobile friendly, dropdowns work, mobile menu items == desktop items,
      no sticky nav on desktop or mobile.
- [x] **6. Responsive sizing**: mobile, tablet, small-to-large desktop, menus included.
- [x] **7. Semantic HTML5** for tool pages: calculator form + H1 + intro paragraph.
- [x] **8. Code bloat**: duplicated markup/inline code that can move to CSS/JS files, without
      changing function or look and feel.

Then: commit (do not push).

## Round 2: navigation & user experience

- [x] A. Alignment of nav elements across devices
- [~] B. Readability (text size/contrast)
- [x] C. Functionality: dropdowns work, everything clickable
- [x] D. Accuracy: every nav/footer/card link goes to the right page
- [x] E. Content organised by topic/category in the menu; nothing duplicated across categories
- [x] F. No links to missing, irrelevant or misleading pages
- [~] G. Cross-browser sanity (features used vs. browser support)

## Added during the round

- [x] Breadcrumbs: visible labels + BreadcrumbList JSON-LD names/URLs were already translated; the `<nav aria-label>`
      was hard-coded English ("Breadcrumb") on every language -> new `breadcrumb` UI string in all 18 `ui.json`.
      Open decision: tool pages (798 of 912) have no breadcrumb row and no BreadcrumbList at all; only the 114 static pages do.
- [x] sitemap.xml: was 2.2 MB on one line (18,240 `xhtml:link` alternates). Now 85 KB, one `<url><loc>` per line,
      written with explicit UTF-8. hreflang stays in each page's `<head>` (see `hreflang_audit.py`).

## Log

- Item 1 (done): `audit_item1.py` over 914 pages: 0 broken internal links/anchors/assets, 0 `.html` or absolute
  internal links, header/footer/drawer identical within every language, viewport/charset/canonical/
  description/robots correct, no reversed `meta`/`link` attribute order, no invalid characters,
  sitemap == 912 indexable pages (404 + verification file excluded), fonts: only DM Sans + JetBrains Mono
  via Tailwind `font-sans`/`font-mono` (no inline `font-family`). Fixed: 27 translated `meta_title`s
  > 70 chars (es/fr/it/pt/ru/th) and 3 fr descriptions > 200 chars. Left as soft notes: 181 translated
  titles are 61-70 chars wide and 269 descriptions are 156-200 (Google may truncate; not errors);
  CJK/Arabic/Indic/Thai pages use system fallback fonts (DM Sans has no such glyphs); sitemap has no `<lastmod>`.
- Item 2 (done): `audit_item2.py` (balanced-tag parse of all 914 pages) + `audit_item2_js.js` (every distinct inline
  script/JSON-LD must parse: 7,071 blocks, 1,207 distinct). 0 problems in 913 content pages: one html/head/body,
  doctype first, ends with `</html>`, no stray/unclosed/truncated tags, no unbalanced comments. Only
  `google7cc5de103ad575d0.html` fails the structural check, and it must stay a one-line verification file.
- Item 3 (done): `audit_item3.py` (class/heading/width consistency per template, all pages). Heading order
  clean on every page (one h1, no skipped level); h1/h2/h3/p classes identical per template kind;
  all containers `max-w-7xl px-4 sm:px-6` (404 intentionally `max-w-2xl`). Fixed: ad slots used `px-2`
  instead of `px-4` (generate.py). Intentional, left: home tab h2 `mb-3`/`mb-2` (first one has no intro `<p>`).
- Item 4 (done): every tag in every built page was classified as bare/classed, inside/outside `.article`.
  Bare tags are covered by Tailwind preflight (lists, sub/sup, headings reset), the typography plugin
  (p, headings, lists, links, table cells, code, blockquote, figure) or `base.css` (aside, details/summary, dl/dt/dd,
  b/i, h5/h6, img, tables, caption). Fixed in `src/base.css`: physical `left` properties (aside, dd, th,
  caption) -> logical (`border-inline-start`, `padding-inline-start`, `text-align:start`) so RTL (Arabic)
  mirrors; added `color-scheme: light/dark` (native controls/scrollbars were light in dark mode); added one
  `:focus-visible` ring for links/buttons/summary (was each browser's own outline).
  Not styled because no page uses them today: mark, kbd, pre, abbr, del/ins, q, cite, tfoot (the
  typography plugin covers pre/kbd/tfoot).
- Item 5 (done): `audit_item5.py`: desktop menu links == mobile drawer links (42 == 42) on all 913 pages; header bar is not
  sticky/fixed anywhere (no `position:sticky` in the CSS; the drawer panel and dropdown popovers are fixed overlays by design).
  Real browser (Chrome, iframe at 320-1920 px): dropdowns open/close on outside click and stay inside the viewport at 768/1024/1280/1920;
  priority nav collapses to "More" at 768; drawer opens/closes (button, backdrop, Esc) and its sections expand. Fixed:
  hamburger was pushed off-screen on every phone (<436 px: 237 px logo + language switcher + theme + hamburger) -> logo `h-6 sm:h-8`,
  header language switcher `hidden md:block` (the drawer already lists every language); in RTL the drawer opened from the wrong
  side -> `end-0`/`end-3` + one RTL rule in base.css.
- Item 6 (done): 58 URLs x 320/360/768 px plus 42 tools x {en,nl,de,ru,th} at 320 px in Chrome: no horizontal page overflow except
  fixed: AdSense leaderboard 728 px wide in a 720 px slot at 768 px (threshold now 776), fixed 300 px ad in a 288 px slot at 320 px
  (`px-0`), long Dutch footer words (`break-words`). Remaining, not fixed: one wide *inline* KaTeX formula overflows at 320 px
  on 3 pages (win-loss in nl/de/ru); display formulas already scroll.
- Item 7 (done): tool-page semantics confirmed: one `<main>`, `<section id="calculator">`, `<form novalidate>` containing the `<h1>` + intro `<p>`,
  `<label for>`+`<input>`, `<output for>`, sr-only submit, `<aside aria-label>`. Fixed: form now `aria-labelledby` the h1 (`#tool-title`),
  and all 1,406 `<output>`s are `aria-labelledby` their caption. Not changed: related-tool cards are bare `<a>`s inside the `<aside>`
  (no `<ul>`), written by the silo rotation script.
- Item 8 (done): per-page weight on a tool page 97.2 KB -> 67.9 KB (-30%): repeated Tailwind class strings -> component classes
  (`menu-link`, `drawer-lang-link`, `footer-mega-link`, `.article` prose modifiers) in `src/tailwind-input.css`; the ~9 KB inline script
  (nav + tables + KaTeX + copy buttons, duplicated in three templates) -> `src/site.js` -> `public/site.min.js` (terser, `defer`, `?v=hash`).
  Verified: computed styles/section heights of the article identical before/after, 798/798 jsdom tool tests pass with the external script,
  Chrome check of drawer/theme/copy/reset/KaTeX/table wrapping in en/fr/ar. Not done: header 28 KB + drawer 15 KB + footer 10 KB are
  the same 42-link lists repeated 3-4x per page (needs a structural change).
- Round 2 (A-G): A/C/D/F covered by items 1, 5, 6 (alignment, working dropdowns, no broken links, no links to missing pages);
  E menu is organised by 5 topic categories, each tool appears once per list; B readability only partly checked
  (no contrast measurement); G cross-browser only checked in Chrome (+ jsdom), not Safari/Firefox.
