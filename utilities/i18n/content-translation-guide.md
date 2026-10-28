# Content translation guide (second pass: `content_html` + FAQ)

Applies to the 42 tool articles (`content_html`) and the 11 FAQ sets already written in English.
Tracked in `content-translation-checklist.md`. First-pass files (meta, h1, card strings, static pages) are done.

**This is localisation, not translation.** The goal is a page a native speaker would believe was written
in their language by someone who knows the topic, that ranks for the terms people there actually search.
A sentence-by-sentence rendering of the English is a failed page, even when every word is correct.

## 1. Scope and what must NOT change

| Stays identical to English | Gets rewritten in the target language |
|---|---|
| Tag sequence, attributes, classes, `id`s, `href`s; `<figure>` infographics are **not imported**: omit them from the translation (the validator drops them from the English before comparing and rejects them in a translation) | All visible text |
| LaTeX (`$$...$$`, `\(...\)`); only `\text{...}` labels may be translated | `<caption>`, `<summary>`, `<figcaption>`, table headers |
| Numbers, decimal point, thousands comma, `$` amounts | Words around the numbers, units spelled out in words |
| Order and number of `<h2>`/`<h3>`/`<h4>`, table rows/columns, list items, FAQ items | Headings, FAQ questions and answers |

Reason for keeping numbers as-is: the calculator prints `12.5`, `1,250.00`. A worked example that says
`12,5` next to a tool that outputs `12.5` looks like a bug. Result: every example can be re-checked in the tool.

Validated mechanically by `python3 utilities/i18n/validate.py <lang> <slug>` (tag skeleton, LaTeX, FAQ count).
Passing it is necessary, not sufficient: sections 2-6 are reviewed by a person.

## 2. Terminology: one glossary per language, written first

Before touching any article, write `src/content/i18n/<lang>/glossary.md` (kept in the repo) with, for each
core concept, the term **real users search for**, not the dictionary term:

- percentage, percent, percentage point, percentage change / increase / decrease / difference / error,
  reverse percentage, markup vs margin, APR vs APY, basis point, ppm, GPA/CGPA/SGPA, ratio, fraction, decimal,
  commission, depreciation, tip, proof (alcohol), slope/grade, percentile, baker's percentage.
- Source of truth, in order: (1) the term already used in that language's `h1`, `nav_names` and
  `long_tail_anchor` (first pass), so article and page title agree; (2) Google autocomplete, "People also ask"
  and the top native-language results for that tool's keyword; (3) a national curriculum/bank/regulator page
  for formal terms. Record the source URL beside any term that is not obvious.
- Record the **chosen form once** (e.g. "percent sign spacing", "formal/informal you", "loanword vs native
  word") and reuse it in all 42 articles. Inconsistent terms across pages are the commonest defect.
- Where two terms compete (loanword vs native), prefer the one with more search volume and say so in the glossary.

## 3. Method per page (do not skip steps)

1. **Read the whole English article first**, then decide the page's search intent and the primary keyword
   in the target language (from the glossary / h1). The first paragraph must contain that keyword naturally,
   inside the same `<strong>` tags the English uses for its key phrases.
2. **Rewrite paragraph by paragraph in the target language's own structure.** Change sentence order,
   split or merge sentences, replace English idioms with native ones, whenever grammar or style needs it.
   Keep every fact, step, and example; do not add or drop claims.
3. **Tags stay in the same order.** If grammar moves a phrase, move the text inside the tag, not the tag.
   If a `<strong>`/`<em>` phrase cannot exist in the target grammar, emphasise the closest equivalent phrase.
4. **Adapt illustrative content, never the maths.** People's names, foods, shops and sports may be swapped
   for locally natural ones. Numbers, formulas, results and table values must be unchanged.
5. **Check every number in the translated text still matches** the English and the calculator (the test in section 7).
6. **Read it aloud / native-speaker pass** (section 6) before ticking.

## 4. Language rules (apply to every language)

- **Grammar and usage:** correct case/gender/number agreement, particles, counters, honorific level, and
  plural rules of the language (Arabic dual/plural, Russian 1/2-4/5+ forms, Japanese/Korean/Chinese counters).
  Never leave an unconverted English word order ("calculator of percentage").
- **Register:** one consistent register for the whole site (see the table below), neutral and instructional,
  no marketing tone the English does not have. Headings in the language's normal heading style (sentence case
  where the language has case).
- **Headings are search queries.** `<h2>`/`<h3>` should read like what a native would type or ask, not like a
  calque of the English heading. Keep the same count and the same hierarchy.
- **Facts are country-specific.** Statements about US/UK/India rules (tax, tipping customs, grading systems,
  proof scales, APR/APY disclosure rules) stay attributed to that country ("in the US ..."). Do not turn them
  into claims about the target country and do not invent local rules. If a section only makes sense for one
  country (e.g. SGPA to percentage for India, 4.0 GPA for the US), keep it, and add local context only when
  you can cite it; otherwise leave a `<!-- REVIEW: ... -->`-free page and list it in "Open questions" in the checklist.
- **Units and names:** `%` stays `%` (spelling out "percent" as a word follows the glossary). Spacing before `%`
  follows the language: non-breaking space (`&nbsp;`) in de, fr, ru; attached in the rest, including es (decided so the text matches the calculator output; confirm the rest with the reviewer).
- **Currency:** amounts and the `$` symbol stay as written (no conversion). If a reviewer decides the symbol
  should be local, change symbol only, never the number, and apply it to all 42 pages.
- **Tone of examples:** keep examples neutral; no brands, no real people, no medical/legal/financial advice
  beyond what the English says.
- **Brand/links:** the one external link (`joteocalculator.com`, 6 pages) keeps its URL; translate the anchor text.
  `#fragment` links keep their target `id`.

## 5. FAQ rules

- Same number and order of items as English. Mapping is 1:1 so the FAQPage schema stays equivalent.
- **Questions** are phrased the way a native speaker would ask them (check "People also ask"); do not
  mirror English syntax. Keep the question mark convention of the language (`؟`, `？`, `?`).
- **Answers** are self-contained, 1-3 sentences, begin with the answer, contain the same numbers and formula
  as English. Plain text only (they are escaped into JSON-LD), no HTML.
- The same terminology as the article and glossary.

## 6. Quality gates before ticking a box

1. `validate.py <lang> <slug>` passes.
2. Glossary check: search the file for the English term list, none remains in prose (except brand/formula names).
3. No English sentence fragments left (`grep -P '[A-Za-z]{4,}'` on text nodes for non-Latin languages; read for Latin ones).
4. Numbers in prose/tables identical to English (script in section 7).
5. A second person reads it: native speaker or equivalent proficiency. For the first 3 tools of every language
   this review is mandatory and its comments are applied to the glossary before the remaining 39 tools.
6. Page opened in a browser: layout, RTL for Arabic, no overflow in tables, headings and TOC readable.

## 7. Tooling and sequence

- Build: `python3 src/generate.py` then `python3 utilities/silo_linking/generate_silo_rotation.py`.
- Functional test unchanged: `NODE_PATH=.test-cache/node_modules node utilities/i18n/test_tools.js <lang>`.
- Writing: `python3 utilities/i18n/add_content.py <lang> <slug> --html article.html [--faq faq.json]` merges the
  article/FAQ into the tool file and validates it; on any error the file is restored.
- Number check is built into `validate.py` (digit sequences in article and FAQ must equal English's).
- Order within a language: glossary -> the 3 pilot tools (home, one finance, one education) -> review ->
  remaining tools in checklist order -> FAQs -> full validate + build + browser spot-check.
- Order across languages: do not start language N+1 until N is committed and reviewed.

## 8. Language profiles (decisions to confirm with the reviewer)

| Code | Language | Direction / script notes | Address & register |
|---|---|---|---|
| ar | Arabic | RTL; Modern Standard Arabic; keep Western digits and `%` to match the calculator; formulas stay LTR | Impersonal/imperative, formal |
| bn | Bengali | Bengali script; Western digits kept | Polite `আপনি` |
| de | German | Latin | Formal `Sie`; `&nbsp;%` |
| es | Spanish | Latin; Latin American-neutral Spanish (costo, tasa, tarea); `%` attached | `tú`, impersonal where possible |
| fr | French | Latin; `&nbsp;` before `%` and before `: ; ? !` | `vous` |
| hi | Hindi | Devanagari; Western digits kept | `आप` |
| id | Indonesian | Latin | Standard, `Anda` |
| it | Italian | Latin | `Lei`/impersonal, neutral |
| ja | Japanese | No spaces between words; full-width punctuation | `です・ます` |
| ko | Korean | Hangul; spacing rules | `합니다` style (formal polite) |
| ms | Malay | Latin; Malaysian standard | Standard, `anda` |
| nl | Dutch | Latin | `u` or neutral; choose once |
| pt | Portuguese | Latin; pick Brazilian (largest audience) and state it in the glossary | `você`/impersonal |
| ru | Russian | Cyrillic; plural forms; `&nbsp;%` | `вы` |
| th | Thai | No spaces between words | Polite particles used sparingly, neutral |
| vi | Vietnamese | Latin with diacritics | `bạn` |
| zh-cn | Chinese (Simplified) | Mainland terminology, full-width punctuation | Neutral |
| zh-tw | Chinese (Traditional) | Taiwan terminology (not an OpenCC conversion of zh-cn), full-width punctuation | Neutral |

## 9. Open decisions before starting (listed once, answered in the checklist)

1. **Heading `id`s.** Done: translated pages reuse the English heading ids by position (`english_heading_ids()` in
   `generate.py`), so anchors and TOC links match across languages. The heading count must equal English (validator checks the tag skeleton).
2. **Percent-sign spacing and digit style** per language (table above).
3. **Currency symbol policy** (default: unchanged).
