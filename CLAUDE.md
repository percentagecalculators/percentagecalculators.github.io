# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website hosted on GitHub Pages at `percentagecalculators.github.io`. A collection of free online percentage calculator tools with multi-language support (19 languages). No build system, framework, or package manager — just plain HTML with inline CSS/JS.

## Architecture

- **No build step.** All pages are static HTML files served directly by GitHub Pages. To preview locally, open any `index.html` in a browser or use a local HTTP server (`python3 -m http.server`).
- **Tailwind CSS via CDN** (`cdn.tailwindcss.com`) — no local Tailwind installation or config files. Custom Tailwind config is inline in each HTML `<head>`.
- **All JavaScript is inline** at the bottom of each HTML file. Calculator logic uses vanilla JS with `oninput` handlers for real-time calculation (no button clicks needed).
- **Dark theme** using Tailwind's slate color palette (bg-slate-900 body, bg-slate-950 header/sections, green-400/500 accents).

## Content Structure

- `/index.html` — Homepage with main calculator (3 tabs: "What is X% of Y?", "X is what % of Y?", "% Change") plus inline increase/decrease/difference/discount calculators
- `/<calculator-name>/index.html` — Dedicated calculator pages (10 total: percentage-increase, percentage-decrease, percentage-change, percentage-difference, percentage-off, fraction-to-percentage, percentage-growth, reverse-percentage, percentage-error, average-percentage)
- `/<lang-code>/` — Localized versions of every calculator page. Language codes: nl, pt, es, fr, de, hi, bn, zh-cn, id, th, zh-tw, it, ja, ms, ar, ko, ru, vi
- `/page/` — Static pages: about, contact, disclaimer, privacy-policy, terms-of-use

## Page Template Pattern

Every page follows the same structure:
1. `<head>` — SEO meta tags, Schema.org JSON-LD (FAQPage + WebApplication), hreflang tags for all languages, canonical URL, favicon links, Tailwind CDN + inline config, inline `<style>`
2. `<header>` — Sticky nav with logo, Calculators dropdown, Language switcher dropdown, mobile hamburger menu
3. `<main>` — Calculator UI + content sections + FAQ accordion
4. `<footer>` — Calculator links grid, static page links, copyright
5. `<script>` — Navigation JS (dropdowns, mobile menu), then page-specific calculator logic

## Key Conventions

- All internal links use absolute paths from root (e.g., `/percentage-increase-calculator/`)
- Each calculator page has its own self-contained JS — no shared JS files
- Schema.org structured data (FAQPage, WebApplication) is included on every calculator page for SEO
- Google AdSense integration via `ads.txt` (pub-5426315045205785)
- Currency symbol is configurable per page via `const currencySymbol = "$"` in the inline script
- Numbers are formatted with `formatNumber()`: integers shown as-is, decimals limited to 4 places
