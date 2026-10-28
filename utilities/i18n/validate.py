#!/usr/bin/env python3
"""Check that a translation file differs from its English source only in text.

Usage: validate.py <lang> <slug> [<lang> <slug> ...]   or   validate.py --all
Use slug "ui" for a language's chrome strings (ui.json: nav, footer, buttons, nav names).
Use slug "pages" for a language's static pages (src/content/i18n/<lang>/pages.json),
which also checks section/paragraph/list counts and identical tags + link hrefs.
Checks: same tag sequence (tag names + attributes) in subtitle/content_html,
same LaTeX math, same FAQ count, and every translatable string in
card.fields_html (label text, placeholder, aria-label) has a card_strings entry.
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
CONTENT = os.path.join(ROOT, "src", "content")
TAG_RE = re.compile(r"<[^>]+>")
MATH_RE = re.compile(r"\$\$.*?\$\$|\\\(.*?\\\)", re.DOTALL)
CARD_TEXT_RE = re.compile(r">([^<>{}]*[^\s<>{}][^<>{}]*)<|(?:placeholder|aria-label|title)=\"([^\"]+)\"")


NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")


def numbers(text):
    """Sorted numeric tokens of the visible text (tags stripped)."""
    return sorted(NUM_RE.findall(TAG_RE.sub(" ", text)))


def skeleton(html):
    return [re.sub(r"\s+", " ", t) for t in TAG_RE.findall(html)]


def card_strings(fields_html):
    out = set()
    for m in CARD_TEXT_RE.finditer(fields_html):
        s = (m.group(1) or m.group(2)).strip()
        if s and re.search(r"[^\W\d_]", s):  # skip strings with no letters (1, 2, :, %)
            out.add(s)
    return out


def check_pages(lang):
    path = os.path.join(CONTENT, "i18n", lang, "pages.json")
    try:
        t = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return [f"cannot load {path}: {e}"]
    en = json.load(open(os.path.join(CONTENT, "pages.json"), encoding="utf-8"))
    errs = []
    for name in en:
        if name not in t:
            errs.append(f"{name}: missing")
            continue
        e, x = en[name], t[name]
        for f in ("h1", "subtitle"):
            if e.get(f) and not x.get(f):
                errs.append(f"{name}.{f}: missing")
        for f in ("meta_title", "meta_description"):
            if not x.get(f):
                errs.append(f"{name}.{f}: missing")
        if set(e) | {"meta_title", "meta_description"} != set(x):
            errs.append(f"{name}: keys differ ({sorted((set(e) | {'meta_title', 'meta_description'}) ^ set(x))})")
        if len(e["sections"]) != len(x.get("sections", [])):
            errs.append(f"{name}: section count differs")
            continue
        for i, (se, sx) in enumerate(zip(e["sections"], x["sections"])):
            if set(se) != set(sx):
                errs.append(f"{name}.sections[{i}]: keys differ")
                continue
            for k in ("paragraphs", "list"):
                if len(se.get(k, [])) != len(sx.get(k, [])):
                    errs.append(f"{name}.sections[{i}].{k}: item count differs")
                    continue
                for j, (a, b) in enumerate(zip(se.get(k, []), sx.get(k, []))):
                    if skeleton(a) != skeleton(b):
                        errs.append(f"{name}.sections[{i}].{k}[{j}]: tags/attributes differ")
    for name in t:
        if name not in en:
            errs.append(f"{name}: unknown page")
    return errs


def check_ui(lang):
    """ui.json: every chrome string, category, company link and nav name."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import generate
    try:
        ui = json.load(open(os.path.join(CONTENT, "i18n", lang, "ui.json"), encoding="utf-8"))
    except Exception as e:
        return [f"cannot load ui.json: {e}"]
    site = json.load(open(os.path.join(ROOT, "src", "data", "site.json"), encoding="utf-8"))
    errs = [f"missing {k}" for k in list(generate.UI_EN) + ["footer_tagline", "native_name"] if not ui.get(k)]
    for g in site["nav_groups"]:
        for k in ("label", "short_label", "tagline"):
            if not ui.get("nav_groups", {}).get(g["key"], {}).get(k):
                errs.append(f"nav_groups.{g['key']}.{k}: missing")
    for l in site["company_links"]:
        if not ui.get("company_links", {}).get(l["href"]):
            errs.append(f"company_links[{l['href']}]: missing")
    for fn in os.listdir(CONTENT):
        if fn.endswith(".json") and fn != "pages.json" and not ui.get("nav_names", {}).get(fn[:-5]):
            errs.append(f"nav_names[{fn[:-5]}]: missing")
    return errs


def check(lang, slug):
    if slug == "pages":
        return check_pages(lang)
    if slug == "ui":
        return check_ui(lang)
    errs = []
    src_path = os.path.join(CONTENT, "pages.json" if False else f"{slug}.json")
    path = os.path.join(CONTENT, "i18n", lang, f"{slug}.json")
    try:
        t = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return [f"cannot load {path}: {e}"]
    en = json.load(open(src_path, encoding="utf-8"))
    # content_html and faq are a later pass: optional, but checked when present
    for f in ("meta_title", "meta_description", "h1", "subtitle", "hint", "long_tail_anchor"):
        if en.get(f) and not t.get(f):
            errs.append(f"missing {f}")
    if skeleton(en.get("subtitle", "")) != skeleton(t.get("subtitle", "")):
        errs.append("subtitle: tag skeleton differs from English")
    if t.get("content_html") and skeleton(en.get("content_html", "")) != skeleton(t["content_html"]):
        errs.append("content_html: tag skeleton differs from English")
    if t.get("content_html") and MATH_RE.findall(en.get("content_html", "")) != MATH_RE.findall(t["content_html"]):
        # LaTeX \text{...} may be translated, so compare only math-with-text-stripped
        strip = lambda L: [re.sub(r"\\text\{[^}]*\}", r"\\text{}", m) for m in L]
        if strip(MATH_RE.findall(en["content_html"])) != strip(MATH_RE.findall(t["content_html"])):
            errs.append("content_html: LaTeX differs beyond \\text{} labels")
    if t.get("content_html") and numbers(en.get("content_html", "")) != numbers(t["content_html"]):
        a, b = numbers(en["content_html"]), numbers(t["content_html"])
        errs.append("content_html: numbers differ from English (only in EN: %s; only in translation: %s)" % (
            [x for x in a if x not in b][:8], [x for x in b if x not in a][:8]))
    if t.get("faq") and len(en.get("faq", [])) != len(t["faq"]):
        errs.append("faq: item count differs")
    elif t.get("faq"):
        for i, (e, f) in enumerate(zip(en["faq"], t["faq"]), 1):
            if not f.get("question") or not f.get("answer"):
                errs.append(f"faq #{i}: empty question or answer")
            elif "<" in f["question"] + f["answer"]:
                errs.append(f"faq #{i}: HTML in question/answer (plain text only)")
            elif numbers(e["question"] + " " + e["answer"]) != numbers(f["question"] + " " + f["answer"]):
                errs.append(f"faq #{i}: numbers differ from English")
    need = card_strings(en["card"]["fields_html"])
    have = set(t.get("card_strings", {}))
    if need - have:
        errs.append(f"card_strings missing: {sorted(need - have)}")
    if have - need:
        errs.append(f"card_strings unknown (not in English card): {sorted(have - need)}")
    return errs


if __name__ == "__main__":
    args = sys.argv[1:]
    pairs = []
    if args == ["--all"]:
        base = os.path.join(CONTENT, "i18n")
        for lang in sorted(os.listdir(base)):
            for fn in sorted(os.listdir(os.path.join(base, lang))):
                pairs.append((lang, fn[:-5]))
    else:
        pairs = list(zip(args[::2], args[1::2]))
    bad = 0
    for lang, slug in pairs:
        errs = check(lang, slug)
        print(("FAIL" if errs else "ok  "), lang, slug)
        for e in errs:
            print("   -", e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)
