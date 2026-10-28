#!/usr/bin/env python3
"""Writes src/content/i18n/<lang>/*.json from one compact language data module.

    python3 utilities/i18n/build_lang.py --skeleton de   # writes lang_de.py with EVERY tool/page/UI key
    python3 utilities/i18n/build_lang.py path/to/lang_de.py

The module defines:
  LANG        language code ("fr")
  EG          prefix replacing "e.g. " in card placeholders ("p. ex. ")
  COMMON      {english card string: translation} shared by several tools
  T           {slug: (meta_title, meta_description, h1, subtitle, hint,
                      long_tail_anchor, {english card string: translation})}
  UI          chrome strings (see generate.UI_EN keys) + footer_tagline,
              native_name, nav_groups, company_links
  HOME_NAME   nav name of the home page (other nav names default to the h1)
  NAV_OVERRIDES  optional {slug: shorter nav name}
  PAGES       {page: [translated strings in source order, or None to copy the
              English string verbatim]} -- order: h1, subtitle (if the English
              page has one), then per section: heading, paragraphs, list items
  PAGE_META   {page: (meta_title, meta_description)}

The tool list is read from src/content/ (never from a hand-kept list). Before
anything is written the module is checked for completeness -- every tool, page,
UI key, card string and page string count -- and ALL problems are reported at
once; if there is any, nothing is written. Afterwards the language is validated
and its checklist section ticked.
"""
import importlib.util, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import validate as v  # noqa: E402
import generate  # noqa: E402

CONTENT = os.path.join(ROOT, "src", "content")


def dump(path, doc):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")


def flat_page(page):
    out = [page["h1"]]
    if "subtitle" in page:
        out.append(page["subtitle"])
    for sec in page["sections"]:
        out.append(sec["heading"])
        out += sec.get("paragraphs", [])
        out += sec.get("list", [])
    return out


def build_page(en, strings, meta, problems, name):
    src = flat_page(en)
    if len(strings) != len(src):
        problems.append(f"page {name!r}: {len(strings)} strings, English has {len(src)} (order: h1, subtitle, then per section heading/paragraphs/list)")
        return None
    it = iter(zip(strings, src))
    take = lambda: (lambda s, e: e if s is None else s)(*next(it))
    page = {"meta_title": meta[0], "meta_description": meta[1], "h1": take()}
    if "subtitle" in en:
        page["subtitle"] = take()
    page["sections"] = []
    for sec in en["sections"]:
        out = {"heading": take()}
        if "paragraphs" in sec:
            out["paragraphs"] = [take() for _ in sec["paragraphs"]]
        if "list" in sec:
            out["list"] = [take() for _ in sec["list"]]
        page["sections"].append(out)
    return page


def english_tools():
    """Every tool the site builds (home included), straight from src/content."""
    return sorted(f[:-5] for f in os.listdir(CONTENT) if f.endswith(".json") and f != "pages.json")


def load_module(path):
    spec = importlib.util.spec_from_file_location("langmod", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def skeleton(lang):
    """Writes lang_<code>.py next to the cwd: every tool, page and UI key the
    site needs, filled with the English text, so nothing can be forgotten."""
    lines = [f'LANG = "{lang}"', 'EG = "e.g. "  # translate the "e.g. " prefix', 'HOME_NAME = ""', "NAV_OVERRIDES = {}", "COMMON = {}", "", "T = {}"]
    for slug in english_tools():
        en = json.load(open(os.path.join(CONTENT, slug + ".json"), encoding="utf-8"))
        card = {s: s for s in sorted(v.card_strings(en["card"]["fields_html"])) if not s.startswith("e.g. ")}
        lines.append(f"T[{slug!r}] = (")
        for k in ("meta_title", "meta_description", "h1", "subtitle", "hint", "long_tail_anchor"):
            lines.append(f"    {en[k]!r},")
        lines.append(f"    {card!r})")
    lines += ["", f"UI = {json.dumps({**generate.UI_EN, 'footer_tagline': '', 'native_name': ''}, ensure_ascii=False, indent=4)}", "UI['nav_groups'] = {}", "UI['company_links'] = {}", ""]
    site = json.load(open(os.path.join(ROOT, "src", "data", "site.json"), encoding="utf-8"))
    for g in site["nav_groups"]:
        lines.append(f"UI['nav_groups'][{g['key']!r}] = {{'label': {g['label']!r}, 'short_label': {g['short_label']!r}, 'tagline': {g['tagline']!r}}}")
    for l in site["company_links"]:
        lines.append(f"UI['company_links'][{l['href']!r}] = {l['label']!r}")
    pages = json.load(open(os.path.join(CONTENT, "pages.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(ROOT, "src", "data", "pages.json"), encoding="utf-8"))
    lines += ["", "PAGE_META = {"]
    for pg in meta:
        lines.append(f"    {pg['slug']!r}: ({pg['meta_title']!r}, {pg['meta_description']!r}),")
    lines += ["}", "", "# order per page: h1, subtitle (if any), then per section heading/paragraphs/list items.", "# None = copy the English string verbatim (e.g. social links).", "PAGES = {}"]
    for name, page in pages.items():
        lines.append(f"PAGES[{name!r}] = [")
        lines += [f"    {x!r}," for x in flat_page(page)]
        lines.append("]")
    out = f"lang_{lang}.py"
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("wrote", out)


def main(path):
    m = load_module(path)
    lang = m.LANG
    problems = []
    docs = {}  # path -> document; nothing is written unless problems stays empty
    out_dir = os.path.join(CONTENT, "i18n", lang)

    tools = english_tools()
    for slug in tools:
        if slug not in m.T:
            problems.append(f"missing tool {slug!r} in T")
    for slug in m.T:
        if slug not in tools:
            problems.append(f"unknown tool {slug!r} in T (no src/content/{slug}.json)")
    h1s = {}
    for slug in tools:
        if slug not in m.T:
            continue
        mt, md, h1, sub, hint, anchor, card = m.T[slug]
        en = json.load(open(os.path.join(CONTENT, slug + ".json"), encoding="utf-8"))
        cs = {}
        for s in sorted(v.card_strings(en["card"]["fields_html"])):
            if s in card:
                cs[s] = card[s]
            elif s in m.COMMON:
                cs[s] = m.COMMON[s]
            elif s.startswith("e.g. "):
                cs[s] = m.EG + s[5:]
            else:
                problems.append(f"{slug}: no translation for card string {s!r}")
        for s in card:
            if s not in v.card_strings(en["card"]["fields_html"]):
                problems.append(f"{slug}: card string {s!r} is not in the English card")
        for name, val in (("meta_title", mt), ("meta_description", md), ("h1", h1), ("subtitle", sub), ("hint", hint), ("long_tail_anchor", anchor)):
            if val == en[name]:
                problems.append(f"{slug}.{name} is still the English text")
        h1s[slug] = h1
        docs[os.path.join(out_dir, slug + ".json")] = {
            "slug": slug, "lang": lang, "meta_title": mt, "meta_description": md, "h1": h1,
            "subtitle": sub, "hint": hint, "long_tail_anchor": anchor, "card_strings": cs,
        }

    en_pages = json.load(open(os.path.join(CONTENT, "pages.json"), encoding="utf-8"))
    pages = {}
    for name, en in en_pages.items():
        if name not in m.PAGES or name not in m.PAGE_META:
            problems.append(f"missing page {name!r} in PAGES/PAGE_META")
            continue
        page = build_page(en, m.PAGES[name], m.PAGE_META[name], problems, name)
        if page:
            pages[name] = page
    docs[os.path.join(out_dir, "pages.json")] = pages

    ui = dict(m.UI)
    site = json.load(open(os.path.join(ROOT, "src", "data", "site.json"), encoding="utf-8"))
    for k in list(generate.UI_EN) + ["footer_tagline", "native_name"]:
        if not ui.get(k):
            problems.append(f"UI: missing {k!r}")
    for g in site["nav_groups"]:
        for k in ("label", "short_label", "tagline"):
            if not ui.get("nav_groups", {}).get(g["key"], {}).get(k):
                problems.append(f"UI: nav_groups.{g['key']}.{k} missing")
    for l in site["company_links"]:
        if not ui.get("company_links", {}).get(l["href"]):
            problems.append(f"UI: company_links[{l['href']}] missing")
    if not getattr(m, "HOME_NAME", ""):
        problems.append("HOME_NAME missing")
    nav = dict(h1s)
    nav["percentage-calculator"] = getattr(m, "HOME_NAME", "")
    nav.update(getattr(m, "NAV_OVERRIDES", {}))
    ui["nav_names"] = dict(sorted(nav.items()))
    docs[os.path.join(out_dir, "ui.json")] = ui

    if problems:
        print(f"NOTHING WRITTEN -- {len(problems)} problem(s):")
        for p_ in problems:
            print("  -", p_)
        raise SystemExit(1)

    os.makedirs(out_dir, exist_ok=True)
    for fpath, doc in docs.items():
        dump(fpath, doc)
    errs = 0
    for slug in tools + ["pages", "ui"]:
        e = v.check(lang, slug)
        if e:
            errs += 1
            print("FAIL", lang, slug)
            for line in e:
                print("   -", line)
    if errs:
        raise SystemExit(f"{errs} file(s) failed validation (files were written -- fix the data module and re-run)")
    # tick this language's section of the checklist
    cl = os.path.join(ROOT, "utilities", "i18n", "translation-checklist.md")
    lines = open(cl, encoding="utf-8").read().split("\n")
    sec = None
    for i, l in enumerate(lines):
        if l.startswith("## "):
            sec = l[3:].split(" ")[0]
        elif sec == lang and l.startswith("- [ ] "):
            lines[i] = l.replace("[ ]", "[x]", 1)
    open(cl, "w", encoding="utf-8").write("\n".join(lines))
    print(f"{lang}: {len(tools)} tool files + pages + ui written, all valid; checklist ticked")


if __name__ == "__main__":
    if sys.argv[1] == "--skeleton":
        skeleton(sys.argv[2])
    else:
        main(sys.argv[1])
