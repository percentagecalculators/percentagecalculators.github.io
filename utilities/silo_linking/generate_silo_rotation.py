#!/usr/bin/env python3
"""
Monthly silo link rotation for percentagecalculators.github.io.

Adapted from mic-tests.github.io's "Advanced Silo" internal-linking system, but the link
carrier is different: instead of injecting inline sentence+anchor links into content_html
paragraphs, this script overwrites the existing "related tools" card grid
(<aside class="related-tools" ...>, see src/template.html) that already sits next to every
tool card. Each of the grid's 4 cards *is* the silo link -- no article copy is required, which
matters here because the 30 tools added in the Phase 2 expansion all still have empty
content_html (a separate, decoupled content-writing pass, not a prerequisite for this script).

Two pillars, 3 hubs each, supporters underneath every hub:

  Pillar 1: percentage-calculator (index.html)      -- "percentage calculator" 1.83M/mo
    Hub A: fraction-to-percentage-calculator          -- Converters
    Hub B: sgpa-to-percentage-calculator              -- Education
    Hub C: win-loss-percentage-calculator             -- Everyday & Niche

  Pillar 2: percentage-difference-calculator          -- "percentage difference calculator" 301K/mo
    Hub D: percentage-increase-calculator              -- Core comparison
    Hub E: apy-calculator                              -- Finance/Interest
    Hub F: profit-percentage-calculator                -- Finance/Profit

No cross-pillar bridging -- the two pillar groups rotate and bridge independently. See this
project's CLAUDE.md ("Internal Linking Strategy - Advanced Silo") for the full writeup.

Every page's <aside class="related-tools"> is fully regenerated each run (there is no
surrounding prose to preserve, unlike mic-tests' inline-sentence approach), so the
SILO_START/SILO_END comment markers are documentation for humans reading the source, not
something the script depends on for locating its target -- it locates the aside by its class
attribute directly.

Every built language (src/content/i18n/<lang>/ui.json) gets its own independent silo with the
same structure and the same monthly shuffle: its pages link only to pages of the same language
(/es/..., /th/...), with card text taken from that language's translated tool names/teasers.
English stays at the top level. The per-page hard rules are audited on every run (and on
--dry-run); any violation prints "AUDIT ..." and exits non-zero.

Run via GitHub Actions on the 1st-3rd of each month, or manually:
  python3 utilities/silo_linking/generate_silo_rotation.py --dry-run [--verbose]
  python3 utilities/silo_linking/generate_silo_rotation.py
"""

import datetime
import hashlib
import os
import random
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(REPO_ROOT, "src")
PAGES_DIR = os.path.join(REPO_ROOT, "public")

# Runs as the LAST step of the build (after build_data.py + generate.py), patching the
# already-minified public/*.html files in place. generate.py's html-minifier-terser call uses
# --remove-comments, so any comment markers must be injected after that step, never before.
sys.path.insert(0, SRC_DIR)
import generate as gen  # noqa: E402  (reuses TOOL_ACCENTS, extract_tool_icon, truncate_teaser)

# ---------------------------------------------------------------------------
# Silo structure
# ---------------------------------------------------------------------------

PILLARS = ["pillar_1", "pillar_2"]

PILLAR_SLUG = {
    "pillar_1": "percentage-calculator",
    "pillar_2": "percentage-difference-calculator",
}

HUBS = {
    "pillar_1": ["fraction-to-percentage-calculator", "sgpa-to-percentage-calculator", "win-loss-percentage-calculator"],
    "pillar_2": ["percentage-increase-calculator", "apy-calculator", "profit-percentage-calculator"],
}

SILO_SUPPORTERS = {
    "fraction-to-percentage-calculator": [
        "decimal-to-percentage-calculator", "ratio-to-percentage-calculator", "ppm-to-percentage-calculator",
        "basis-points-calculator", "slope-percentage-calculator", "alcohol-proof-calculator",
    ],
    "sgpa-to-percentage-calculator": [
        "marks-percentage-calculator", "gpa-to-percentage-calculator", "cgpa-to-percentage-calculator",
        "percentile-to-percentage-calculator",
    ],
    "win-loss-percentage-calculator": [
        "tip-calculator", "bakers-percentage-calculator", "food-cost-percentage-calculator",
        "percent-solution-calculator",
    ],
    "percentage-increase-calculator": [
        "percentage-decrease-calculator", "percentage-change-calculator", "percentage-off-calculator",
        "reverse-percentage-calculator", "percentage-error-calculator", "average-percentage-calculator",
        "percentage-point-calculator", "percentage-of-a-percentage-calculator",
    ],
    "apy-calculator": [
        "apr-calculator", "apr-apy-converter", "simple-interest-calculator",
        "compound-interest-calculator", "loan-interest-calculator", "percentage-growth-calculator",
    ],
    "profit-percentage-calculator": [
        "profit-margin-calculator", "markup-calculator", "gross-margin-calculator",
        "salary-increase-calculator", "commission-calculator", "depreciation-calculator",
    ],
}

# Reverse lookups built once at import time.
HUB_PILLAR = {hub: pk for pk, hubs in HUBS.items() for hub in hubs}
SUPPORTER_HUB = {sup: hub for hub, sups in SILO_SUPPORTERS.items() for sup in sups}

ALL_SILO_SLUGS = (
    set(PILLAR_SLUG.values())
    | set(HUB_PILLAR.keys())
    | set(SUPPORTER_HUB.keys())
)

ASIDE_RE = re.compile(r'(<aside class="related-tools[^"]*"[^>]*>)(.*?)(</aside>)', re.DOTALL)

# ---------------------------------------------------------------------------
# Deterministic monthly shuffles
# ---------------------------------------------------------------------------


def _seed(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)


def shuffled_hubs(pillar_key, today):
    key = "%d-%02d-pillar_%s" % (today.year, today.month, pillar_key)
    hubs = list(HUBS[pillar_key])
    random.Random(_seed(key)).shuffle(hubs)
    return hubs


def shuffled_supporters(hub_slug, today):
    key = "%d-%02d-silo_%s" % (today.year, today.month, hub_slug)
    sup = list(SILO_SUPPORTERS[hub_slug])
    random.Random(_seed(key)).shuffle(sup)
    return sup


# ---------------------------------------------------------------------------
# Per-page card assignment -- strict counts matching the classic Advanced Silo
# methodology: pillar exactly 1, hub up to 4 (fewer at the ends of its
# pillar's hub order -- no left/right neighbor there, and that slot is simply
# omitted rather than backfilled), supporter up to 3 (fewer at the absolute
# ends of the whole pillar-wide supporter chain, where there's no bridge).
# ---------------------------------------------------------------------------


def pillar_cards(pillar_key, today):
    hubs = shuffled_hubs(pillar_key, today)
    return [hubs[0]]  # exactly 1 outgoing link, hoards authority on the pillar


def hub_cards(hub_slug, today):
    pillar_key = HUB_PILLAR[hub_slug]
    hubs = shuffled_hubs(pillar_key, today)
    pos = hubs.index(hub_slug)
    chain = shuffled_supporters(hub_slug, today)

    card1 = PILLAR_SLUG[pillar_key]  # up
    card2 = hubs[pos - 1] if pos > 0 else None  # left neighbor (empty if first)
    card3 = hubs[pos + 1] if pos < len(hubs) - 1 else None  # right neighbor (empty if last)
    card4 = chain[0]  # down to first supporter in this month's chain

    return [c for c in [card1, card2, card3, card4] if c]


def supporter_cards(supporter_slug, today):
    hub_slug = SUPPORTER_HUB[supporter_slug]
    pillar_key = HUB_PILLAR[hub_slug]
    hubs = shuffled_hubs(pillar_key, today)
    hub_pos = hubs.index(hub_slug)
    chain = shuffled_supporters(hub_slug, today)
    pos = chain.index(supporter_slug)
    n = len(chain)

    card1 = hub_slug  # up

    if pos == 0:
        card2 = chain[1] if n > 1 else None  # next
        if hub_pos > 0:
            left_hub = hubs[hub_pos - 1]
            card3 = shuffled_supporters(left_hub, today)[-1]  # backward bridge
        else:
            card3 = None  # first hub in this pillar's order has no backward bridge
    elif pos == n - 1:
        card2 = chain[pos - 1]  # prev
        if hub_pos < len(hubs) - 1:
            right_hub = hubs[hub_pos + 1]
            card3 = shuffled_supporters(right_hub, today)[0]  # forward bridge
        else:
            card3 = None  # last hub in this pillar's order has no forward bridge
    else:
        card2 = chain[pos - 1]  # prev
        card3 = chain[pos + 1]  # next

    return [c for c in [card1, card2, card3] if c]


def cards_for_slug(slug, today):
    if slug in PILLAR_SLUG.values():
        pillar_key = [k for k, v in PILLAR_SLUG.items() if v == slug][0]
        return pillar_cards(pillar_key, today)
    if slug in HUB_PILLAR:
        return hub_cards(slug, today)
    if slug in SUPPORTER_HUB:
        return supporter_cards(slug, today)
    raise KeyError("slug not in silo map: %s" % slug)


# ---------------------------------------------------------------------------
# HTML rendering + patching -- reuses generate.py's own card markup/helpers so
# styling stays byte-identical to the default (non-rotated) related-card grid.
# ---------------------------------------------------------------------------


def render_card_html(target_slug, by_slug, site):
    tool = by_slug[target_slug]
    color = gen.TOOL_ACCENTS.get(target_slug, "emerald")
    teaser = gen.truncate_teaser(tool["meta_description"])
    return (
        '<a href="%s" class="related-card group flex flex-col gap-3 rounded-xl border border-border bg-surface p-4 hover:border-border-strong hover:shadow-sm">'
        '<span class="flex h-9 w-9 items-center justify-center rounded-lg bg-%s-100 text-%s-600 dark:bg-%s-500/15 dark:text-%s-400">%s</span>'
        '<span class="text-sm font-semibold text-text group-hover:text-accent">%s</span>'
        '<span class="text-xs leading-snug text-text-muted">%s</span></a>'
        % (
            gen.tool_url(tool, site), color, color, color, color,
            gen.extract_tool_icon(tool), gen.html.escape(tool["nav_name"]), gen.html.escape(teaser),
        )
    )


def patch_file(path, cards, by_slug, site, dry_run):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    cards_html = "".join(render_card_html(s, by_slug, site) for s in cards)
    marked = "<!-- SILO_START:grid -->" + cards_html + "<!-- SILO_END:grid -->"

    new_html, count = ASIDE_RE.subn(lambda m: m.group(1) + marked + m.group(3), html, count=1)
    if count == 0:
        print("  WARNING: no <aside class=\"related-tools\"> found in %s -- skipped" % path)
        return False

    if new_html == html:
        return False
    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
    return True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def parse_date_arg(argv):
    for arg in argv:
        if arg.startswith("--date="):
            year, month = arg[len("--date="):].split("-")
            return datetime.date(int(year), int(month), 1)
    return datetime.date.today()


def pillar_of(slug):
    """Pillar key a silo slug belongs to (pillars, hubs and supporters)."""
    for pk, pslug in PILLAR_SLUG.items():
        if slug == pslug:
            return pk
    if slug in HUB_PILLAR:
        return HUB_PILLAR[slug]
    return HUB_PILLAR[SUPPORTER_HUB[slug]]


def audit_cards(slug, cards):
    """Hard rules from CLAUDE.md ("Internal Linking Strategy"); returns violations."""
    bad = []
    if slug in cards:
        bad.append("links to itself")
    if len(cards) != len(set(cards)):
        bad.append("duplicate target")
    for c in cards:
        if c not in ALL_SILO_SLUGS:
            bad.append("target %s is not in the silo map" % c)
        elif pillar_of(c) != pillar_of(slug):
            bad.append("cross-pillar link to %s" % c)
    if slug in PILLAR_SLUG.values():
        if len(cards) != 1:
            bad.append("pillar must have exactly 1 card, has %d" % len(cards))
        if cards and cards[0] not in HUB_PILLAR:
            bad.append("pillar must link to a hub")
    elif slug in HUB_PILLAR:
        if not 3 <= len(cards) <= 4:
            bad.append("hub must have 3-4 cards, has %d" % len(cards))
        for c in cards:
            if c in SUPPORTER_HUB and SUPPORTER_HUB[c] != slug:
                bad.append("hub links to another hub's supporter %s" % c)
    else:
        if not 2 <= len(cards) <= 3:
            bad.append("supporter must have 2-3 cards, has %d" % len(cards))
        if any(c in PILLAR_SLUG.values() for c in cards):
            bad.append("supporter links directly to a pillar")
    return bad


def load_language(lang, site, tools):
    """(site, by_slug) as rendered for a language: English straight from
    src/data, other languages with their translated tool names, teasers and
    nav text -- the same overlays generate.py applies when building them."""
    if lang == "en":
        gen.set_locale("en")
    else:
        loc = gen.load_locale(lang)
        gen.set_locale(lang, loc["ui"])
        site = gen.localize_site(site, loc["ui"])
        tools = gen.localize_tools(tools, loc)
    return site, {t["slug"]: t for t in tools}


def aside_hrefs(path):
    with open(path, encoding="utf-8") as f:
        m = ASIDE_RE.search(f.read())
    return re.findall(r'<a href="([^"]+)"', m.group(2)) if m else []


def main():
    import json
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    today = parse_date_arg(sys.argv)

    with open(os.path.join(SRC_DIR, "data", "site.json")) as f:
        en_site = json.load(f)
    with open(os.path.join(SRC_DIR, "data", "tools.json")) as f:
        en_tools = json.load(f)
    with open(os.path.join(SRC_DIR, "data", "pages.json")) as f:
        pages = json.load(f)

    # generate.py's URL helpers (tool_url, localize_href, ...) read this module state;
    # generate.main() normally fills it in.
    langs = gen.discover_languages()
    gen.BUILT_LANGS[:] = langs
    gen.TOOL_SLUGS.update(t["slug"] for t in en_tools)
    gen.PAGE_SLUGS.update(p["slug"] for p in pages)

    built_slugs = {t["slug"] for t in en_tools}
    missing_from_silo = built_slugs - ALL_SILO_SLUGS
    missing_from_build = ALL_SILO_SLUGS - built_slugs
    if missing_from_silo:
        print("WARNING: tools built but not in the silo map (won't get rotated links): %s"
              % ", ".join(sorted(missing_from_silo)))
    if missing_from_build:
        print("WARNING: silo map references tools that don't exist in the build: %s"
              % ", ".join(sorted(missing_from_build)))

    silo_slugs = sorted(ALL_SILO_SLUGS & built_slugs)
    total = changed_total = problems = 0
    for lang in langs:
        site, by_slug = load_language(lang, en_site, en_tools)
        changed = 0
        for slug in silo_slugs:
            cards = cards_for_slug(slug, today)
            for v in audit_cards(slug, cards):
                problems += 1
                print("  AUDIT %s/%s: %s" % (lang, slug, v))
            kind = "home" if slug == site["home_slug"] else "tool"
            path = os.path.join(PAGES_DIR, gen.out_rel_path(lang, kind, slug))
            if not os.path.exists(path):
                print("  WARNING: %s not found, skipping %s/%s" % (path, lang, slug))
                continue
            if patch_file(path, cards, by_slug, site, dry_run):
                changed += 1
                if verbose:
                    print("%s %s/%-45s -> %s" % ("would update" if dry_run else "updated", lang, slug, ", ".join(cards)))
            if not dry_run:
                # every link in a language's grid must stay inside that language
                prefix = "/" if lang == "en" else "/%s/" % lang
                for h in aside_hrefs(path):
                    wrong = (not h.startswith(prefix)) if lang != "en" else (h[1:2] and h.split("/")[1] in langs[1:])
                    if wrong:
                        problems += 1
                        print("  AUDIT %s/%s: link %s leaves the language" % (lang, slug, h))
        total += len(silo_slugs)
        changed_total += changed
        print("%-6s %d/%d silo pages %s" % (lang, changed, len(silo_slugs), "would change" if dry_run else "changed"))
    gen.set_locale("en")

    print("\n%d/%d silo pages %s across %d language(s) (%d unchanged); %d audit problem(s)." % (
        changed_total, total, "would change" if dry_run else "changed", len(langs), total - changed_total, problems,
    ))
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
