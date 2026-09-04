#!/usr/bin/env python3
"""Authors data/site.json + data/tools.json + data/pages.json for
percentagecalculators.github.io. Run this, then `python3 src/generate.py`, to
(re)build public/. See this project's CLAUDE.md for the full pipeline.

Modeled directly on passwordhive's own build_data.py
(coffee_can_checker_tools_project/individual_websites/passwordhive/src/build_data.py):
every tool is a single file, content/<slug>.json carries the *entire* page
(meta_title/meta_description, h1/subtitle, card, script, content_html, faq —
see src/content/README.md once written). This function just loads and
lightly post-processes those files (nav_name lookup, slug order) via
load_tool() — no per-tool Python builder function.

Phase 1 scope: the 10 tools ported from legacy-bootstrap-site/ (2 of them,
percentage-growth-calculator and reverse-percentage-calculator, had real
calculate() bugs on the old site — fixed here, not carried forward) plus a
new home tool, percentage-calculator (3-mode: X% of Y / Y is what % of X /
% change), replacing the old combined index.html. Phase 2 (not built yet)
adds ~35 more tools from utilities/keyword-research/tool-ideas.md — see
CATEGORY_GROUPS below, where those show up as "tools" placeholder entries
(a 404 until each one's content/<slug>.json is authored and its {slug, name}
pair is moved into a "slugs" list, same pattern passwordhive's own
CATEGORY_GROUPS uses for its own planned expansion).
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONTENT_DIR = os.path.join(BASE_DIR, "content")

SITE_NAME = "Percentage Calculators"
DOMAIN = "percentagecalculators.github.io"
HOME_SLUG = "percentage-calculator"
CONTACT_EMAIL = "buzzsubash@gmail.com"

# Phase 1 — the 10 legacy tools (ported, 2 bug-fixed) + the new home tool.
TOOL_SLUGS = [
    "percentage-calculator",
    "percentage-increase-calculator",
    "percentage-decrease-calculator",
    "percentage-change-calculator",
    "percentage-difference-calculator",
    "percentage-off-calculator",
    "reverse-percentage-calculator",
    "percentage-error-calculator",
    "average-percentage-calculator",
    "fraction-to-percentage-calculator",
    "percentage-growth-calculator",
]

NAV_NAMES = {
    "percentage-calculator": "Percentage Calculator",
    "percentage-increase-calculator": "Percentage Increase Calculator",
    "percentage-decrease-calculator": "Percentage Decrease Calculator",
    "percentage-change-calculator": "Percentage Change Calculator",
    "percentage-difference-calculator": "Percentage Difference Calculator",
    "percentage-off-calculator": "Percentage Off Calculator",
    "reverse-percentage-calculator": "Reverse Percentage Calculator",
    "percentage-error-calculator": "Percentage Error Calculator",
    "average-percentage-calculator": "Average Percentage Calculator",
    "fraction-to-percentage-calculator": "Fraction to Percentage Calculator",
    "percentage-growth-calculator": "Percentage Growth Calculator",
}


def load_tool(slug):
    path = os.path.join(CONTENT_DIR, "%s.json" % slug)
    with open(path) as f:
        tool = json.load(f)
    tool["nav_name"] = NAV_NAMES[slug]
    return tool


def build_tools():
    return [load_tool(slug) for slug in TOOL_SLUGS]


# ---------------------------------------------------------------------------
# Site nav/footer structure — see utilities/keyword-research/tool-ideas.md for
# where every Phase 2 "tools" placeholder entry below comes from. A group's
# "slugs" list is resolved against by_slug (real, built tools); its "tools"
# list is static {slug, name} pairs that render a link today (404 until that
# tool's content/<slug>.json exists) — see group_links() in generate.py.
# ---------------------------------------------------------------------------

CATEGORY_GROUPS = [
    {
        "key": "core",
        "label": "Core Percentage Tools",
        "short_label": "Core",
        "tagline": "The essentials: find a percentage, increase or decrease a number, and compare two values.",
        "slugs": [
            "percentage-calculator", "percentage-increase-calculator", "percentage-decrease-calculator",
            "percentage-change-calculator", "percentage-difference-calculator", "percentage-off-calculator",
            "reverse-percentage-calculator", "percentage-error-calculator", "average-percentage-calculator",
        ],
        "tools": [
            {"slug": "percentage-point-calculator", "name": "Percentage Point Calculator"},
        ],
    },
    {
        "key": "converters",
        "label": "Converters",
        "short_label": "Converters",
        "tagline": "Convert between percentages, fractions, decimals, ratios, and other unit forms.",
        "slugs": ["fraction-to-percentage-calculator"],
        "tools": [
            {"slug": "decimal-to-percentage-calculator", "name": "Decimal to Percentage Calculator"},
            {"slug": "ratio-to-percentage-calculator", "name": "Ratio to Percentage Calculator"},
            {"slug": "ppm-to-percentage-calculator", "name": "PPM to Percentage Calculator"},
            {"slug": "basis-points-calculator", "name": "Basis Points Calculator"},
            {"slug": "slope-percentage-calculator", "name": "Slope Percentage Calculator"},
            {"slug": "alcohol-proof-calculator", "name": "Alcohol Proof Calculator"},
        ],
    },
    {
        "key": "health-fitness",
        "label": "Health & Fitness",
        "short_label": "Health",
        "tagline": "Body fat, BMI, body composition, and weight-loss percentage calculators.",
        "slugs": [],
        "tools": [
            {"slug": "body-fat-percentage-calculator", "name": "Body Fat Percentage Calculator"},
            {"slug": "bmi-calculator", "name": "BMI Calculator"},
            {"slug": "body-composition-calculator", "name": "Body Composition Calculator"},
            {"slug": "weight-loss-percentage-calculator", "name": "Weight Loss Percentage Calculator"},
        ],
    },
    {
        "key": "education",
        "label": "Education",
        "short_label": "Education",
        "tagline": "GPA, CGPA, SGPA, marks, and percentile conversions for students.",
        "slugs": [],
        "tools": [
            {"slug": "gpa-to-percentage-calculator", "name": "GPA to Percentage Calculator"},
            {"slug": "cgpa-to-percentage-calculator", "name": "CGPA to Percentage Calculator"},
            {"slug": "sgpa-to-percentage-calculator", "name": "SGPA to Percentage Calculator"},
            {"slug": "marks-percentage-calculator", "name": "Marks Percentage Calculator"},
            {"slug": "percentile-to-percentage-calculator", "name": "Percentile to Percentage Calculator"},
        ],
    },
    {
        "key": "finance",
        "label": "Finance & Business",
        "short_label": "Finance",
        "tagline": "Interest rates, profit margins, markup, salary raises, and business growth.",
        "slugs": ["percentage-growth-calculator"],
        "tools": [
            {"slug": "apy-calculator", "name": "APY Calculator"},
            {"slug": "apr-calculator", "name": "APR Calculator"},
            {"slug": "apr-apy-converter", "name": "APR to APY Converter"},
            {"slug": "simple-interest-calculator", "name": "Simple Interest Calculator"},
            {"slug": "compound-interest-calculator", "name": "Compound Interest Calculator"},
            {"slug": "loan-interest-calculator", "name": "Loan Interest Calculator"},
            {"slug": "profit-percentage-calculator", "name": "Profit Percentage Calculator"},
            {"slug": "profit-margin-calculator", "name": "Profit Margin Calculator"},
            {"slug": "markup-calculator", "name": "Markup Calculator"},
            {"slug": "gross-margin-calculator", "name": "Gross Margin Calculator"},
            {"slug": "salary-increase-calculator", "name": "Salary Increase Calculator"},
            {"slug": "commission-calculator", "name": "Commission Calculator"},
            {"slug": "depreciation-calculator", "name": "Depreciation Calculator"},
        ],
    },
    {
        "key": "everyday",
        "label": "Everyday & Niche",
        "short_label": "Everyday",
        "tagline": "Tips, win rates, baking ratios, food cost, and solution-concentration percentages.",
        "slugs": [],
        "tools": [
            {"slug": "tip-calculator", "name": "Tip Calculator"},
            {"slug": "win-loss-percentage-calculator", "name": "Win/Loss Percentage Calculator"},
            {"slug": "bakers-percentage-calculator", "name": "Baker's Percentage Calculator"},
            {"slug": "food-cost-percentage-calculator", "name": "Food Cost Percentage Calculator"},
            {"slug": "percent-solution-calculator", "name": "Percent Solution Calculator"},
        ],
    },
]


def build_site(tools):
    return {
        "site_name": SITE_NAME,
        "domain": DOMAIN,
        "home_slug": HOME_SLUG,
        "footer_tagline": "Free online percentage calculators. Every calculation runs entirely in your browser — instant results, no sign-up.",
        "nav_groups": CATEGORY_GROUPS,
        "company_links": [
            {"label": "About", "href": "/about"},
            {"label": "Contact", "href": "/contact"},
            {"label": "Disclaimer", "href": "/disclaimer"},
            {"label": "Privacy Policy", "href": "/privacy-policy"},
            {"label": "Terms of Use", "href": "/terms-of-use"},
        ],
    }


# ---------------------------------------------------------------------------
# Info pages -- ported from legacy-bootstrap-site/page/*/index.html into
# content/pages.json ({slug: {h1, subtitle, sections}}). Only meta_title/
# meta_description are authored here; h1/subtitle/sections come from the
# ported content, in the typed heading+paragraphs(+list) shape
# render_info_content() in generate.py expects.
# ---------------------------------------------------------------------------

PAGE_META = {
    "about": ("About Us | Percentage Calculators",
              "Learn about Percentage Calculators — a free collection of client-side percentage tools built for speed and accuracy."),
    "contact": ("Contact Us | Percentage Calculators", "Get in touch with the Percentage Calculators team."),
    "disclaimer": ("Disclaimer | Percentage Calculators",
                    "Percentage Calculators' disclaimer: our tools are for informational purposes only and are not a substitute for professional advice."),
    "privacy-policy": ("Privacy Policy | Percentage Calculators",
                        "Percentage Calculators' privacy policy: what data we collect (very little), and how our tools handle your input."),
    "terms-of-use": ("Terms of Use | Percentage Calculators", "Terms of use for Percentage Calculators' free online calculators."),
}


def build_pages():
    with open(os.path.join(CONTENT_DIR, "pages.json")) as f:
        ported = json.load(f)
    pages = []
    for slug, (meta_title, meta_description) in PAGE_META.items():
        page = dict(ported[slug])
        page["slug"] = slug
        page["meta_title"] = meta_title
        page["meta_description"] = meta_description
        pages.append(page)
    return pages


def main():
    tools = build_tools()
    site = build_site(tools)
    pages = build_pages()

    with open(os.path.join(DATA_DIR, "tools.json"), "w") as f:
        json.dump(tools, f, indent=2)
    with open(os.path.join(DATA_DIR, "site.json"), "w") as f:
        json.dump(site, f, indent=2)
    with open(os.path.join(DATA_DIR, "pages.json"), "w") as f:
        json.dump(pages, f, indent=2)

    print("Wrote %d tools, %d nav groups, %d info pages." % (len(tools), len(site["nav_groups"]), len(pages)))


if __name__ == "__main__":
    main()
