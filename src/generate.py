#!/usr/bin/env python3
"""Renders template.html/template-page.html/template-404.html x data/*.json
into public/, minifying HTML by default. Run `python3 src/build_data.py`
first to (re)generate data/site.json, data/tools.json, data/pages.json.

    python3 src/generate.py             # full build, minified HTML
    python3 src/generate.py --no-minify # fast iteration, unminified output

Every tool is one file — content/<slug>.json carries meta_title/
meta_description, h1/subtitle, the card config, script (the tool's own fully
self-contained JS — no shared runtime file), content_html, and faq. Every
tool uses the "raw" card layout: card["fields_html"] is the tool's ENTIRE
card grid, authored directly in its own JSON file — every calculator here
has different inputs/outputs, so there is exactly one Python-side render
branch to maintain regardless of tool count.

Styling is Tailwind via the Play CDN (<script src="https://cdn.tailwindcss.
com">, loaded in every page's <head>) — there is no compiled/purged Tailwind
build and no PostCSS step. src/base.css carries only what Tailwind utilities
can't express: the self-hosted @font-face rules and a set of CSS custom
properties (light theme on :root, dark theme under .dark) that
TAILWIND_CONFIG below exposes to Tailwind as semantic color names (bg,
surface, border, text, accent, ...). Every utility class built from those
names auto-themes when `.dark` is toggled on <html> — no `dark:` variants
needed in tool markup itself. THEME_INIT is a small inline script (see
render_page()) that sets `.dark` before Tailwind's CDN script runs, reading
localStorage first and falling back to prefers-color-scheme, so there's no
flash of the wrong theme on load.

Unlike passwordhive, there is no typed what_/how_/article_sections fallback.
If a tool has no content_html, render_main_sections() renders nothing below
the tool card for it — an honestly empty section, never synthesized filler.
No Google Analytics: the legacy site never had any GA wiring to port, and no
measurement ID is invented here. No AdSense either — the ad-slot markup,
ads.txt, and adsbygoogle.js loader from the legacy site were deliberately
not carried over.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "public")

HTML_MINIFIER_PKG = "html-minifier-terser@7.2.0"
CLEAN_CSS_PKG = "clean-css-cli@5.6.3"

# Per-category 2-letter badges for the nav dropdowns/mobile drawer — same
# lightweight-icon idea as passwordhive's CATEGORY_META, avoiding a
# per-category SVG authoring burden.
CATEGORY_BADGES = {
    "core": "%",
    "converters": "=",
    "health-fitness": "+",
    "education": "ED",
    "finance": "$",
    "everyday": "..",
}

# A distinct Tailwind stock color per built tool, used for its related-card
# icon badge tint elsewhere on the site (soundtest.io-style varied accents,
# rather than every card sharing the single site accent color).
TOOL_ACCENTS = {
    "percentage-calculator": "emerald",
    "percentage-increase-calculator": "blue",
    "percentage-decrease-calculator": "rose",
    "percentage-change-calculator": "violet",
    "percentage-difference-calculator": "amber",
    "percentage-off-calculator": "orange",
    "reverse-percentage-calculator": "cyan",
    "percentage-error-calculator": "red",
    "average-percentage-calculator": "indigo",
    "fraction-to-percentage-calculator": "pink",
    "percentage-growth-calculator": "teal",
}
RELATED_COUNT = 4

CHEVRON_SVG = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'
CLOSE_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12" stroke-linecap="round"/></svg>'
HAMBURGER_SVG = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18" stroke-linecap="round"/></svg>'
DEFAULT_TOOL_ICON_SVG = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>'

# Sets .dark on <html> (and color-scheme, for native form-control theming)
# before Tailwind's CDN script runs and before body paint, so there's no
# flash of the wrong theme. Reads localStorage first, falls back to the OS
# preference. Wrapped in try/catch since localStorage can throw in some
# privacy-mode contexts.
THEME_INIT = (
    "(function(){try{"
    "var s=localStorage.getItem('theme');"
    "var d=s?s==='dark':matchMedia('(prefers-color-scheme: dark)').matches;"
    "document.documentElement.classList.toggle('dark',d);"
    "document.documentElement.style.colorScheme=d?'dark':'light';"
    "}catch(e){}})();"
)

# Exposes base.css's CSS-custom-property color tokens to Tailwind as
# semantic names, and maps the self-hosted fonts. darkMode:'class' means
# every dark: variant (and every semantic color utility) is driven by the
# .dark class THEME_INIT/initThemeToggle() toggle on <html>, not by
# prefers-color-scheme directly.
TAILWIND_CONFIG = (
    "tailwind.config={darkMode:'class',theme:{extend:{colors:{"
    "bg:'rgb(var(--color-bg) / <alpha-value>)',"
    "'bg-alt':'rgb(var(--color-bg-alt) / <alpha-value>)',"
    "surface:'rgb(var(--color-surface) / <alpha-value>)',"
    "'surface-alt':'rgb(var(--color-surface-alt) / <alpha-value>)',"
    "border:'rgb(var(--color-border) / <alpha-value>)',"
    "'border-strong':'rgb(var(--color-border-strong) / <alpha-value>)',"
    "text:'rgb(var(--color-text) / <alpha-value>)',"
    "'text-alt':'rgb(var(--color-text-alt) / <alpha-value>)',"
    "'text-secondary':'rgb(var(--color-text-secondary) / <alpha-value>)',"
    "'text-muted':'rgb(var(--color-text-muted) / <alpha-value>)',"
    "accent:'rgb(var(--color-accent) / <alpha-value>)',"
    "'accent-dark':'rgb(var(--color-accent-dark) / <alpha-value>)',"
    "'accent-darker':'rgb(var(--color-accent-darker) / <alpha-value>)',"
    "warning:'rgb(var(--color-warning) / <alpha-value>)',"
    "danger:'rgb(var(--color-danger) / <alpha-value>)'"
    "},fontFamily:{"
    "sans:['DM Sans','DM Sans Fallback','system-ui','-apple-system','sans-serif'],"
    "mono:['JetBrains Mono','JetBrains Mono Fallback','monospace']"
    "}}}};"
)

# ---------------------------------------------------------------------------
# Tool-card rendering — "raw" is the only layout on this site (see module
# docstring): card["fields_html"] is the tool's entire card grid.
# ---------------------------------------------------------------------------

def render_tool_card_body(tool):
    card = tool.get("card", {})
    layout = card.get("layout", "raw")
    if layout != "raw":
        raise ValueError("Unknown card layout: %r on tool %r (only 'raw' is implemented on this site)" % (layout, tool.get("slug")))
    # The page's one <h1> plus a short one-line usage hint both live inside
    # the tool card's own title bar (see module docstring / the redesign
    # this pattern came from) rather than floating outside it — fields_html
    # carries literal "{{H1}}"/"{{HINT}}" placeholders at that spot,
    # resolved here from tool["h1"]/tool["hint"] so the text has one source
    # of truth instead of being duplicated per file. tool["subtitle"] (the
    # longer marketing-copy paragraph) is intentionally not rendered here —
    # kept in the content JSON for potential future use, not shown on-page.
    body = card.get("fields_html", "")
    body = body.replace("{{H1}}", html.escape(tool["h1"]))
    body = body.replace("{{HINT}}", html.escape(tool.get("hint", "")))
    return body


# ---------------------------------------------------------------------------
# Related calculators — derived from build_data.py's CATEGORY_GROUPS, never
# from a group's "tools" placeholder list (those are unbuilt Phase-2 tools
# that 404 today; they must never appear as links in this prominent,
# above-the-fold slot on every page).
# ---------------------------------------------------------------------------

TOOL_ICON_RE = re.compile(r'<svg class="icon"[^>]*>.*?</svg>', re.DOTALL)


def extract_tool_icon(tool):
    match = TOOL_ICON_RE.search(tool.get("card", {}).get("fields_html", ""))
    return match.group(0) if match else DEFAULT_TOOL_ICON_SVG


def truncate_teaser(text, limit=78):
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def related_tools_for(tool, site, tools):
    slug = tool["slug"]
    same_category = []
    for group in site["nav_groups"]:
        if slug in group.get("slugs", []):
            for s in group["slugs"]:
                if s != slug and s not in same_category:
                    same_category.append(s)
    backfill = [t["slug"] for t in tools if t["slug"] != slug and t["slug"] not in same_category]
    return (same_category + backfill)[:RELATED_COUNT]


def render_related_calculators(tool, site, by_slug, tools):
    cards = []
    for slug in related_tools_for(tool, site, tools):
        related = by_slug[slug]
        color = TOOL_ACCENTS.get(slug, "emerald")
        teaser = truncate_teaser(related["meta_description"])
        cards.append(
            '<a href="%s" class="related-card group flex flex-col gap-3 rounded-xl border border-border bg-surface p-4 hover:border-border-strong hover:shadow-sm">'
            '<span class="flex h-9 w-9 items-center justify-center rounded-lg bg-%s-100 text-%s-600 dark:bg-%s-500/15 dark:text-%s-400">%s</span>'
            '<span class="text-sm font-semibold text-text group-hover:text-accent">%s</span>'
            '<span class="text-xs leading-snug text-text-muted">%s</span></a>'
            % (
                tool_url(related, site), color, color, color, color,
                extract_tool_icon(related), html.escape(related["nav_name"]), html.escape(teaser),
            )
        )
    return "".join(cards)


# ---------------------------------------------------------------------------
# Main sections (content_html split at each <h2>, plus FAQ) — same mechanism
# as passwordhive/webcamtest's raw-HTML-override path.
# ---------------------------------------------------------------------------

H2_SPLIT_RE = re.compile(r"(?=<h2\b)", re.IGNORECASE)

ARTICLE_PROSE_CLASSES = (
    "article prose dark:prose-invert max-w-none "
    "prose-headings:text-text prose-p:text-text-secondary prose-li:text-text-secondary prose-ol:text-text-secondary prose-ul:text-text-secondary "
    "prose-a:text-accent prose-a:no-underline hover:prose-a:underline "
    "prose-strong:text-text prose-em:text-text-alt "
    "prose-code:font-mono prose-code:text-accent prose-code:bg-accent/10 prose-code:rounded prose-code:px-1 prose-code:font-normal prose-code:before:content-none prose-code:after:content-none "
    "prose-th:text-text prose-td:text-text-secondary prose-thead:border-border prose-tr:border-border "
    "prose-blockquote:border-accent prose-blockquote:text-text-secondary prose-hr:border-border"
)


def split_content_by_h2(content_html):
    parts = [p for p in H2_SPLIT_RE.split(content_html) if p.strip()]
    if parts and not re.match(r"^\s*<h2\b", parts[0], re.IGNORECASE):
        lead = parts.pop(0)
        if parts:
            parts[0] = lead + parts[0]
        else:
            parts = [lead]
    return parts


def render_faq_section(tool, alt):
    if not tool.get("faq"):
        return None
    items = "".join(
        '<div class="faq-item border-b border-border py-5 last:border-0">'
        '<dt class="mb-2 flex gap-2 text-base font-bold text-text"><span class="flex-none text-accent">Q.</span><span>%s</span></dt>'
        '<dd class="pl-6 text-[0.92rem] leading-relaxed text-text-secondary">%s</dd></div>'
        % (html.escape(f["question"]), f["answer"])
        for f in tool["faq"]
    )
    bg = "bg-bg-alt" if alt else "bg-bg"
    return (
        '<section class="block py-10 %s sm:py-14"><div class="block-inner mx-auto max-w-5xl px-4 sm:px-6">'
        '<div class="section-header mb-6"><h2 class="text-2xl font-bold text-text">Frequently Asked Questions</h2></div>'
        '<dl class="faq-list grid grid-cols-1 gap-x-10 md:grid-cols-2">%s</dl>'
        '</div></section>' % (bg, items)
    )


def render_main_sections(tool):
    """Renders everything below the tool card from tool["content_html"]
    (split into alternating bg-bg/bg-bg-alt sections) plus a FAQ section. No
    content fallback: a tool with no content_html renders no content
    sections, never synthesized filler."""
    parts = []
    section_count = 0
    if tool.get("content_html"):
        chunks = split_content_by_h2(tool["content_html"])
        for chunk in chunks:
            bg = "bg-bg-alt" if section_count % 2 == 1 else "bg-bg"
            parts.append(
                '<section class="block py-10 %s sm:py-14"><div class="block-inner mx-auto max-w-3xl px-4 sm:px-6">'
                '<div class="content-card rounded-2xl border border-border bg-surface p-6 sm:p-8">'
                '<div class="%s">%s</div></div></div></section>'
                % (bg, ARTICLE_PROSE_CLASSES, chunk)
            )
            section_count += 1
    faq_section = render_faq_section(tool, alt=(section_count % 2 == 1))
    if faq_section:
        parts.append(faq_section)
        section_count += 1
    return "\n".join(parts)


def render_info_content(page):
    out = ""
    for sec in page.get("sections", []):
        out += "<h2>%s</h2>" % html.escape(sec["heading"])
        for p in sec.get("paragraphs", []):
            out += "<p>%s</p>" % p
        if sec.get("list"):
            out += "<ul>" + "".join("<li>%s</li>" % li for li in sec["list"]) + "</ul>"
    return out


# ---------------------------------------------------------------------------
# Nav (header dropdowns + mobile drawer) and footer — Priority+ pattern,
# same as passwordhive/webcamtest's own render_category_dropdowns()/
# render_more_menu()/render_mobile_drawer(). Dropdown/drawer/section
# open-close state is the native `hidden` attribute (toggled directly in
# template.html's JS), not a custom CSS class — no component CSS needed.
# ---------------------------------------------------------------------------

DROPDOWN_LINK_CLASSES = "block rounded-lg px-3 py-2 text-sm text-text-secondary hover:bg-surface-alt hover:text-text"
NAV_BTN_CLASSES = "cat-menu-btn inline-flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-sm font-medium text-text-secondary hover:bg-surface-alt hover:text-text"


def tool_url(tool, site):
    if tool["slug"] == site["home_slug"]:
        return "/"
    return "/%s" % tool["slug"]


def group_links(group, site, by_slug):
    links = []
    for slug in group.get("slugs", []):
        links.append((tool_url(by_slug[slug], site), by_slug[slug]["nav_name"]))
    for t in group.get("tools", []):
        links.append(("/" if t["slug"] == site["home_slug"] else "/%s" % t["slug"], t["name"]))
    return links


def render_category_dropdowns(site, by_slug):
    items = [
        '<div class="cat-menu-item shrink-0"><a href="/" class="%s">Home</a></div>' % NAV_BTN_CLASSES
    ]
    for group in site["nav_groups"]:
        panel_id = "catmenu-%s" % group["key"]
        badge = CATEGORY_BADGES.get(group["key"], "")
        links = "".join(
            '<a href="%s" class="%s">%s</a>' % (url, DROPDOWN_LINK_CLASSES, html.escape(name))
            for url, name in group_links(group, site, by_slug)
        )
        items.append(
            '<div class="cat-menu-item relative shrink-0" data-cat-key="%s">'
            '<button type="button" class="%s" aria-expanded="false" aria-controls="%s">%s%s</button>'
            '<div class="tools-menu cat-menu fixed z-50 w-72 rounded-2xl border border-border bg-surface p-2 shadow-lg" id="%s" hidden>'
            '<div class="menu-panel-header flex items-start gap-3 border-b border-border p-3">'
            '<span class="more-menu-icon flex h-8 w-8 flex-none items-center justify-center rounded-lg bg-accent/10 text-sm font-bold text-accent">%s</span>'
            '<div><strong class="block text-sm font-semibold text-text">%s</strong><p class="mt-0.5 text-xs text-text-muted">%s</p></div></div>'
            '<div class="menu-panel-links flex flex-col p-1">%s</div>'
            '</div>'
            '</div>' % (
                group["key"], NAV_BTN_CLASSES, panel_id, html.escape(group["short_label"]), CHEVRON_SVG, panel_id,
                html.escape(badge), html.escape(group["label"]), html.escape(group["tagline"]), links,
            )
        )
    return "".join(items)


def render_more_menu(site, by_slug):
    sections = []
    for group in site["nav_groups"]:
        badge = CATEGORY_BADGES.get(group["key"], "")
        links = "".join(
            '<a href="%s" class="%s">%s</a>' % (url, DROPDOWN_LINK_CLASSES, html.escape(name))
            for url, name in group_links(group, site, by_slug)
        )
        sections.append(
            '<div class="more-menu-section p-1" data-cat-key="%s" hidden>'
            '<div class="more-menu-heading flex items-center gap-2 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-text-muted">'
            '<span class="more-menu-icon flex h-5 w-5 flex-none items-center justify-center rounded bg-accent/10 text-[0.65rem] font-bold text-accent">%s</span>%s</div>%s'
            '</div>' % (group["key"], html.escape(badge), html.escape(group["label"]), links)
        )
    return (
        '<div class="cat-menu-item relative shrink-0" id="moreMenuItem" hidden>'
        '<button type="button" class="%s" id="moreMenuBtn" aria-expanded="false" aria-controls="moreMenuPanel">More%s</button>'
        '<div class="tools-menu more-menu fixed z-50 max-h-[70vh] w-72 overflow-y-auto rounded-2xl border border-border bg-surface p-2 shadow-lg" id="moreMenuPanel" hidden>%s</div>'
        '</div>' % (NAV_BTN_CLASSES, CHEVRON_SVG, "".join(sections))
    )


def render_mobile_drawer(site, by_slug):
    sections = []
    for group in site["nav_groups"]:
        panel_id = "drawer-%s" % group["key"]
        badge = CATEGORY_BADGES.get(group["key"], "")
        links = "".join(
            '<a href="%s" class="block rounded-lg px-3 py-2 text-sm text-text-secondary hover:bg-surface-alt hover:text-text">%s</a>' % (url, html.escape(name))
            for url, name in group_links(group, site, by_slug)
        )
        sections.append(
            '<div class="nav-drawer-section border-b border-border" data-cluster="%s">'
            '<button type="button" class="drawer-section-btn flex w-full items-center gap-3 px-4 py-3 text-left" aria-expanded="false" aria-controls="%s">'
            '<span class="more-menu-icon flex h-8 w-8 flex-none items-center justify-center rounded-lg bg-accent/10 text-sm font-bold text-accent">%s</span>'
            '<span class="flex-1 text-sm font-semibold text-text">%s</span>'
            '<span class="flex-none text-text-muted">%s</span></button>'
            '<div class="nav-drawer-section-links px-4 pb-3" id="%s" hidden>%s</div>'
            '</div>' % (
                group["key"], panel_id, html.escape(badge), html.escape(group["label"]),
                CHEVRON_SVG, panel_id, links,
            )
        )
    return (
        '<div id="navDrawerBackdrop" class="fixed inset-0 z-40 bg-black/50 opacity-0 transition-opacity duration-200" hidden></div>'
        '<div class="nav-drawer-panel fixed inset-y-0 right-0 z-50 w-[85vw] max-w-sm translate-x-full overflow-y-auto bg-bg-alt shadow-xl transition-transform duration-200" id="navDrawer" role="dialog" aria-modal="true" aria-label="Site navigation" hidden>'
        '<button type="button" class="nav-drawer-close absolute right-3 top-3 rounded-full p-2 text-text-secondary hover:bg-surface-alt" id="navDrawerClose" aria-label="Close menu">%s</button>'
        '<div class="border-b border-border p-4"><a href="/" class="block text-sm font-semibold text-text">Home</a></div>'
        '%s'
        '</div>' % (CLOSE_SVG, "".join(sections))
    )


def render_footer_mega(site, by_slug):
    rows = []
    for group in site["nav_groups"]:
        pairs = group_links(group, site, by_slug)
        links = "".join(
            "<a href=\"%s\" class=\"footer-mega-link inline-block py-1 text-[0.85rem] text-text-secondary hover:text-accent after:ml-2.5 after:text-text-muted after:content-['•'] last:after:content-none\">%s</a>"
            % (url, html.escape(name))
            for url, name in pairs
        )
        rows.append(
            '<div class="footer-mega-row border-b border-border py-4 last:border-0">'
            '<div class="footer-mega-label text-sm font-semibold text-text">%s <span class="footer-mega-count font-normal text-text-muted">(%d)</span></div>'
            '<div class="footer-mega-links mt-2 leading-7">%s</div></div>'
            % (html.escape(group["label"]), len(pairs), links)
        )
    return "\n".join(rows)


def render_footer_company(site):
    return "".join(
        '<a href="%s" class="text-text-secondary hover:text-accent">%s</a>' % (l["href"], html.escape(l["label"]))
        for l in site["company_links"]
    )


def breadcrumb_trail_for_tool(tool, site):
    if tool["slug"] == site["home_slug"]:
        return []
    return [("Home", "/"), (tool["nav_name"], None)]


def render_breadcrumbs(trail):
    if not trail:
        return ""
    items = []
    for i, (label, url) in enumerate(trail):
        if i > 0:
            items.append('<li aria-hidden="true" class="mx-2 text-border-strong">/</li>')
        if url:
            items.append('<li><a href="%s" class="text-text-secondary hover:text-accent">%s</a></li>' % (url, html.escape(label)))
        else:
            items.append('<li aria-current="page" class="text-text">%s</li>' % html.escape(label))
    return '<nav class="breadcrumbs mx-auto max-w-7xl px-4 pt-3 text-sm sm:px-6" aria-label="Breadcrumb"><ol class="flex flex-wrap items-center">%s</ol></nav>' % "".join(items)


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------

def webapp_jsonld(tool, canonical):
    data = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": tool["h1"],
        "url": canonical,
        "description": tool["meta_description"],
        "applicationCategory": "CalculatorApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }
    return json.dumps(data, separators=(",", ":"))


def faq_jsonld(items):
    if not items:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": it["question"],
                "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", it["answer"])},
            }
            for it in items
        ],
    }
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, separators=(",", ":"))


def breadcrumb_jsonld(trail, domain):
    if not trail:
        return ""
    items = []
    for i, (label, url) in enumerate(trail):
        entry = {"@type": "ListItem", "position": i + 1, "name": label}
        if url:
            entry["item"] = "https://%s/" % domain if url == "/" else "https://%s%s" % (domain, url)
        items.append(entry)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, separators=(",", ":"))


def website_jsonld(site):
    data = {"@context": "https://schema.org", "@type": "WebSite", "name": site["site_name"], "url": "https://%s/" % site["domain"]}
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------

def apply_tokens(template, tokens):
    out = template
    for k, v in tokens.items():
        out = out.replace("{{%s}}" % k, v)
    return out


def render_page(tool, site, by_slug, tools, template):
    canonical = "https://%s%s" % (site["domain"], tool_url(tool, site))
    trail = breadcrumb_trail_for_tool(tool, site)
    card = tool.get("card", {})
    data_attrs = "".join(' data-%s="%s"' % (k, html.escape(str(v))) for k, v in card.get("data_attrs", {}).items())

    tokens = {
        "META_DESCRIPTION": html.escape(tool["meta_description"]),
        "SITE_NAME": site["site_name"],
        "CANONICAL_URL": canonical,
        "META_TITLE": html.escape(tool["meta_title"]),
        "WEBAPP_JSONLD": webapp_jsonld(tool, canonical),
        "WEBSITE_JSONLD": website_jsonld(site) if tool["slug"] == site["home_slug"] else "",
        "FAQ_JSONLD": faq_jsonld(tool.get("faq", [])),
        "THEME_INIT": THEME_INIT,
        "TAILWIND_CONFIG": TAILWIND_CONFIG,
        "CATEGORY_DROPDOWNS": render_category_dropdowns(site, by_slug),
        "MORE_MENU": render_more_menu(site, by_slug),
        "MOBILE_DRAWER": render_mobile_drawer(site, by_slug),
        "HAMBURGER_ICON": HAMBURGER_SVG,
        "BREADCRUMBS": render_breadcrumbs(trail) + breadcrumb_jsonld(trail, site["domain"]),
        "H1": tool["h1"],
        "SUBTITLE": tool["subtitle"],
        "TOOL_MODE": card.get("mode", ""),
        "TOOL_LAYOUT": card.get("layout", "raw"),
        "TOOL_DATA_ATTRS": data_attrs,
        "TOOL_CARD_BODY": render_tool_card_body(tool),
        "TOOL_WARNING": "",
        "TOOL_EXTRA_SCRIPTS": "",
        "TOOL_SCRIPT": tool.get("script", ""),
        "CODE_SNIPPET": "",
        "RELATED_CALCULATORS": render_related_calculators(tool, site, by_slug, tools),
        "MAIN_SECTIONS": render_main_sections(tool),
        "FOOTER_TAGLINE": site["footer_tagline"],
        "FOOTER_MEGA": render_footer_mega(site, by_slug),
        "FOOTER_COMPANY": render_footer_company(site),
        "YEAR": "2026",
    }
    return apply_tokens(template, tokens)


def render_info_page(page, site, by_slug, template):
    canonical = "https://%s/%s" % (site["domain"], page["slug"])
    trail = [("Home", "/"), (page["h1"], None)]
    tokens = {
        "META_DESCRIPTION": html.escape(page["meta_description"]),
        "SITE_NAME": site["site_name"],
        "CANONICAL_URL": canonical,
        "META_TITLE": html.escape(page["meta_title"]),
        "THEME_INIT": THEME_INIT,
        "TAILWIND_CONFIG": TAILWIND_CONFIG,
        "CATEGORY_DROPDOWNS": render_category_dropdowns(site, by_slug),
        "MORE_MENU": render_more_menu(site, by_slug),
        "MOBILE_DRAWER": render_mobile_drawer(site, by_slug),
        "HAMBURGER_ICON": HAMBURGER_SVG,
        "BREADCRUMBS": render_breadcrumbs(trail) + breadcrumb_jsonld(trail, site["domain"]),
        "H1": page["h1"],
        "SUBTITLE": page.get("subtitle", ""),
        "PAGE_CONTENT": render_info_content(page),
        "FOOTER_TAGLINE": site["footer_tagline"],
        "FOOTER_MEGA": render_footer_mega(site, by_slug),
        "FOOTER_COMPANY": render_footer_company(site),
        "YEAR": "2026",
    }
    return apply_tokens(template, tokens)


def render_404_page(site, by_slug, template_404):
    tokens = {
        "SITE_NAME": site["site_name"],
        "THEME_INIT": THEME_INIT,
        "TAILWIND_CONFIG": TAILWIND_CONFIG,
        "CATEGORY_DROPDOWNS": render_category_dropdowns(site, by_slug),
        "MORE_MENU": render_more_menu(site, by_slug),
        "MOBILE_DRAWER": render_mobile_drawer(site, by_slug),
        "HAMBURGER_ICON": HAMBURGER_SVG,
        "FOOTER_TAGLINE": site["footer_tagline"],
        "FOOTER_MEGA": render_footer_mega(site, by_slug),
        "FOOTER_COMPANY": render_footer_company(site),
        "YEAR": "2026",
    }
    return apply_tokens(template_404, tokens)


# ---------------------------------------------------------------------------
# Minification / build-tool helpers (pinned versions via npx, same as
# passwordhive/webcamtest)
# ---------------------------------------------------------------------------

def run_npx(args, cwd=None, env=None):
    cmd = ["npx", "--yes"] + args
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Command failed: %s\nSTDOUT:\n%s\nSTDERR:\n%s" % (" ".join(cmd), result.stdout, result.stderr))
    return result


def minify_css_file(src, dst):
    run_npx([CLEAN_CSS_PKG, "-o", dst, src])


def minify_html_dir(src_dir, dst_dir):
    run_npx([
        HTML_MINIFIER_PKG,
        "--input-dir", src_dir,
        "--output-dir", dst_dir,
        "--file-ext", "html",
        "--collapse-whitespace",
        "--remove-comments",
        "--minify-css", "true",
        "--minify-js", "true",
        "--case-sensitive",
    ])


# ---------------------------------------------------------------------------
# Site infra files
# ---------------------------------------------------------------------------

def write_robots_and_sitemap(site, tools, pages, out_dir):
    domain = site["domain"]
    with open(os.path.join(out_dir, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://%s/sitemap.xml\n" % domain)

    urls = ["/"] + ["/%s" % t["slug"] for t in tools if t["slug"] != site["home_slug"]] + ["/%s" % p["slug"] for p in pages]
    entries = "".join(
        "<url><loc>https://%s%s</loc></url>" % (domain, u) for u in urls
    )
    with open(os.path.join(out_dir, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % entries)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    do_minify = "--no-minify" not in sys.argv

    with open(os.path.join(DATA_DIR, "site.json")) as f:
        site = json.load(f)
    with open(os.path.join(DATA_DIR, "tools.json")) as f:
        tools = json.load(f)
    with open(os.path.join(DATA_DIR, "pages.json")) as f:
        pages = json.load(f)

    by_slug = {t["slug"]: t for t in tools}

    with open(os.path.join(BASE_DIR, "template.html")) as f:
        template = f.read()
    with open(os.path.join(BASE_DIR, "template-page.html")) as f:
        template_page = f.read()
    with open(os.path.join(BASE_DIR, "template-404.html")) as f:
        template_404 = f.read()
    with open(os.path.join(BASE_DIR, "base.css")) as f:
        base_css_src = f.read()

    if os.path.exists(OUTPUT_DIR):
        for name in os.listdir(OUTPUT_DIR):
            if name == "fonts":
                continue
            path = os.path.join(OUTPUT_DIR, name)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "fonts"), exist_ok=True)
    for fname in ("dm-sans-variable.woff2", "jetbrains-mono-variable.woff2"):
        shutil.copy(os.path.join(BASE_DIR, "fonts", fname), os.path.join(OUTPUT_DIR, "fonts", fname))
    favicon_path = os.path.join(BASE_DIR, "favicon.ico")
    if os.path.exists(favicon_path):
        shutil.copy(favicon_path, os.path.join(OUTPUT_DIR, "favicon.ico"))
    # Binary/opaque assets that can't be derived from site.json — currently
    # just the Google Search Console verification file carried over from the
    # old site (do not modify its contents; it proves domain ownership).
    static_dir = os.path.join(BASE_DIR, "static")
    if os.path.isdir(static_dir):
        for fname in os.listdir(static_dir):
            shutil.copy(os.path.join(static_dir, fname), os.path.join(OUTPUT_DIR, fname))

    if do_minify:
        base_min_path = os.path.join(OUTPUT_DIR, "base.min.css")
        with tempfile.NamedTemporaryFile("w", suffix=".css", delete=False) as f:
            f.write(base_css_src)
            base_tmp_path = f.name
        minify_css_file(base_tmp_path, base_min_path)
        os.remove(base_tmp_path)
        render_dir = tempfile.mkdtemp(prefix="percentagecalculators_render_")
    else:
        render_dir = OUTPUT_DIR
        with open(os.path.join(OUTPUT_DIR, "base.min.css"), "w") as f:
            f.write(base_css_src)

    for tool in tools:
        out_html = render_page(tool, site, by_slug, tools, template)
        filename = "index.html" if tool["slug"] == site["home_slug"] else "%s.html" % tool["slug"]
        with open(os.path.join(render_dir, filename), "w") as f:
            f.write(out_html)

    for page in pages:
        out_html = render_info_page(page, site, by_slug, template_page)
        with open(os.path.join(render_dir, "%s.html" % page["slug"]), "w") as f:
            f.write(out_html)

    out_html = render_404_page(site, by_slug, template_404)
    with open(os.path.join(render_dir, "404.html"), "w") as f:
        f.write(out_html)

    write_robots_and_sitemap(site, tools, pages, render_dir if not do_minify else OUTPUT_DIR)
    if do_minify:
        write_robots_and_sitemap(site, tools, pages, render_dir)

    if do_minify:
        minify_html_dir(render_dir, OUTPUT_DIR)
        shutil.rmtree(render_dir)

    print("Built %d tool pages + %d info pages into %s (%s)" % (
        len(tools), len(pages), OUTPUT_DIR, "minified" if do_minify else "unminified"
    ))


if __name__ == "__main__":
    main()
