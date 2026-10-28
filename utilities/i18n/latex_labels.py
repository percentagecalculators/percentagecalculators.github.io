#!/usr/bin/env python3
"""Translates the words inside LaTeX \\text{...} labels (the only part of a formula
the validator lets differ), from src/content/i18n/<lang>/latex_labels.tsv
(English label <TAB> translation). add_content.py applies it on every merge.

    python3 utilities/i18n/latex_labels.py <lang> --skeleton   # writes the tsv with every English label
    python3 utilities/i18n/latex_labels.py <lang> --apply      # re-applies to all merged articles
    python3 utilities/i18n/latex_labels.py <lang> --check      # lists labels still in English / unmapped
"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CONTENT = os.path.join(ROOT, "src", "content")
LABEL_RE = re.compile(r"(\\text\{)([^}]*)(\})")


def english_labels():
    out = set()
    for f in glob.glob(os.path.join(CONTENT, "*.json")):
        if f.endswith("pages.json"):
            continue
        for m in LABEL_RE.finditer(json.load(open(f, encoding="utf-8")).get("content_html", "")):
            out.add(m.group(2).strip())
    return sorted(out)


def path(lang):
    return os.path.join(CONTENT, "i18n", lang, "latex_labels.tsv")


def load(lang):
    labels = {}
    if os.path.exists(path(lang)):
        for line in open(path(lang), encoding="utf-8"):
            if "\t" in line:
                k, v = line.rstrip("\n").split("\t", 1)
                if v.strip():
                    labels[k] = v
    return labels


def apply(lang, html, labels=None):
    labels = load(lang) if labels is None else labels

    def repl(m):
        raw = m.group(2)
        core = raw.strip()
        if core in labels:
            lead, trail = raw[:len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
            return m.group(1) + lead + labels[core] + trail + m.group(3)
        return m.group(0)
    return LABEL_RE.sub(repl, html)


def main():
    lang, mode = sys.argv[1], sys.argv[2]
    if mode == "--skeleton":
        with open(path(lang), "w", encoding="utf-8") as fh:
            for k in english_labels():
                fh.write(k + "\t\n")
    elif mode == "--apply":
        labels, n = load(lang), 0
        for f in glob.glob(os.path.join(CONTENT, "i18n", lang, "*.json")):
            if f.endswith(("ui.json", "pages.json")):
                continue
            d = json.load(open(f, encoding="utf-8"))
            if d.get("content_html"):
                new = apply(lang, d["content_html"], labels)
                if new != d["content_html"]:
                    d["content_html"] = new
                    open(f, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
                    n += 1
        print(f"{lang}: labels applied in {n} article(s)")
    elif mode == "--check":
        labels, english = load(lang), set(english_labels())
        print("unmapped English labels:", sorted(k for k in english if k not in labels))
        left = set()
        for f in glob.glob(os.path.join(CONTENT, "i18n", lang, "*.json")):
            if f.endswith(("ui.json", "pages.json")):
                continue
            for m in LABEL_RE.finditer(json.load(open(f, encoding="utf-8")).get("content_html", "")):
                if m.group(2).strip() in english and labels.get(m.group(2).strip(), m.group(2).strip()) == m.group(2).strip() and m.group(2).strip() not in ("CGPA", "SGPA", "GPA", "ppm", "ABV", "COGS", "bps", "Proof"):
                    left.add(m.group(2).strip())
        print("still English in articles:", sorted(left))


if __name__ == "__main__":
    main()
