#!/usr/bin/env python3
"""Merges a translated article and/or FAQ into src/content/i18n/<lang>/<slug>.json.

    python3 utilities/i18n/add_content.py <lang> <slug> --html article.html [--faq faq.json]

article.html is the translated content_html; faq.json is a list of
{"question": ..., "answer": ...} in the English order. The tool file is
rewritten with the same key order and formatting, then validated; on any
validation error the file is restored and nothing changes.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate as v  # noqa: E402


# Typographic spacing the language requires: characters that take a non-breaking
# space before them, and whether guillemets «» take one inside. Applied to text
# only (never inside tags, LaTeX or <code>), so authors can type plain spaces.
TYPO = {"fr": (":;?!%»", True), "de": ("%", False), "ru": ("%", False)}
SKIP_RE = re.compile(r"(<code>.*?</code>|\$\$.*?\$\$|\\\(.*?\\\)|<[^>]+>)", re.DOTALL)


def typography(lang, text, nbsp):
    if lang not in TYPO:
        return text
    before, guillemets = TYPO[lang]
    parts = SKIP_RE.split(text) if nbsp == "&nbsp;" else [text]
    for i in range(0, len(parts), 2 if nbsp == "&nbsp;" else 1):
        seg = re.sub(r"[ \u00a0\u202f]([%s])" % re.escape(before), nbsp + r"\1", parts[i])
        if guillemets:
            seg = re.sub(r"«[ \u00a0\u202f]", "«" + nbsp, seg)
        parts[i] = seg
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lang")
    ap.add_argument("slug")
    ap.add_argument("--html")
    ap.add_argument("--faq")
    a = ap.parse_args()
    if not (a.html or a.faq):
        ap.error("give --html and/or --faq")
    path = os.path.join(v.CONTENT, "i18n", a.lang, f"{a.slug}.json")
    original = open(path, encoding="utf-8").read()
    doc = json.loads(original)
    if a.html:
        doc["content_html"] = typography(a.lang, open(a.html, encoding="utf-8").read().strip(), "&nbsp;")
    if a.faq:
        doc["faq"] = [{k: typography(a.lang, v, "\u00a0") for k, v in item.items()} for item in json.load(open(a.faq, encoding="utf-8"))]
    open(path, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    errs = v.check(a.lang, a.slug)
    if errs:
        open(path, "w", encoding="utf-8").write(original)
        print(f"{a.lang}/{a.slug}: NOT merged")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print(f"{a.lang}/{a.slug}: merged and valid")


if __name__ == "__main__":
    main()
