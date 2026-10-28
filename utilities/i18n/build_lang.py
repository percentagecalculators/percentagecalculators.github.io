#!/usr/bin/env python3
"""Writes src/content/i18n/<lang>/*.json from one compact language data module.

    python3 utilities/i18n/build_lang.py path/to/lang_fr.py

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

Card strings with no letters are skipped; any other string missing from the
tool's dict, COMMON or the "e.g." rule is reported and the run fails.
Afterwards the language is validated and its checklist section ticked.
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


def build_page(en, strings, meta):
    if len(strings) != len(flat_page(en)):
        raise SystemExit(f"page string count {len(strings)} != English {len(flat_page(en))} for {en['h1']!r}")
    src = flat_page(en)
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


def main(path):
    spec = importlib.util.spec_from_file_location("langmod", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    lang = m.LANG
    out_dir = os.path.join(CONTENT, "i18n", lang)
    os.makedirs(out_dir, exist_ok=True)
    failed = False

    slugs = sorted(f[:-5] for f in os.listdir(CONTENT) if f.endswith(".json") and f != "pages.json")
    for slug in slugs:
        if slug not in m.T:
            print("MISSING TOOL", slug)
            failed = True
    h1s = {}
    for slug, (mt, md, h1, sub, hint, anchor, card) in m.T.items():
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
                print("MISSING CARD STRING", slug, repr(s))
                failed = True
        h1s[slug] = h1
        dump(os.path.join(out_dir, slug + ".json"), {
            "slug": slug, "lang": lang, "meta_title": mt, "meta_description": md, "h1": h1,
            "subtitle": sub, "hint": hint, "long_tail_anchor": anchor, "card_strings": cs,
        })

    en_pages = json.load(open(os.path.join(CONTENT, "pages.json"), encoding="utf-8"))
    pages = {}
    for name, en in en_pages.items():
        pages[name] = build_page(en, m.PAGES[name], m.PAGE_META[name])
    dump(os.path.join(out_dir, "pages.json"), pages)

    ui = dict(m.UI)
    nav = dict(h1s)
    nav["percentage-calculator"] = m.HOME_NAME
    nav.update(getattr(m, "NAV_OVERRIDES", {}))
    ui["nav_names"] = dict(sorted(nav.items()))
    dump(os.path.join(out_dir, "ui.json"), ui)

    if failed:
        raise SystemExit("incomplete -- fix the items above")
    errs = 0
    for slug in slugs + ["pages", "ui"]:
        e = v.check(lang, slug)
        if e:
            errs += 1
            print("FAIL", lang, slug)
            for line in e:
                print("   -", line)
    if errs:
        raise SystemExit(f"{errs} file(s) failed validation")
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
    print(f"{lang}: {len(slugs)} tool files + pages + ui written, all valid; checklist ticked")


if __name__ == "__main__":
    main(sys.argv[1])
