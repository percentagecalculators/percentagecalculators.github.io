// Config for the @tailwindcss/typography build — see build_typography_css() in
// ../generate.py. className: 'article' targets the site's existing `.article`
// div directly (template.html/template-page.html), so raw content_html HTML
// (h2/h3/p/ul/ol/li/strong/code/a/blockquote/table...) gets readable typography
// on top of the hand-written base rules already in ../styles.css. corePlugins
// is off — this build emits only the typography plugin's component CSS, not
// Tailwind's utility framework or preflight reset (this site has its own).
// Colors/fonts below are CSS var references into styles.css's tokens, so this
// build stays in sync with the site palette without duplicating hex values —
// only regenerate (rerun generate.py) if those tokens change.
module.exports = {
  // template.html/template-page.html don't have `class="article"` as literal
  // text — that div is composed in Python (render_main_sections/
  // render_info_content in ../generate.py) and only ever reaches the
  // templates via the {{MAIN_SECTIONS}}/{{PAGE_CONTENT}} tokens at render
  // time. Tailwind's JIT scanner only sees what's literally present in these
  // files, so generate.py has to be a scan target too, or this build
  // silently stops emitting `.article` rules the next time nothing else in
  // these files happens to contain that text.
  content: ["../template.html", "../template-page.html", "../generate.py"],
  corePlugins: false,
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "none",
            "--tw-prose-body": "var(--text-secondary)",
            "--tw-prose-headings": "var(--text)",
            "--tw-prose-lead": "var(--text-secondary)",
            "--tw-prose-links": "var(--accent)",
            "--tw-prose-bold": "var(--text)",
            "--tw-prose-counters": "var(--text-muted)",
            "--tw-prose-bullets": "var(--text-muted)",
            "--tw-prose-hr": "var(--border)",
            "--tw-prose-quotes": "var(--text-alt)",
            "--tw-prose-quote-borders": "var(--accent)",
            "--tw-prose-captions": "var(--text-muted)",
            "--tw-prose-code": "var(--accent)",
            "--tw-prose-pre-code": "#f0f0eb",
            "--tw-prose-pre-bg": "var(--surface-alt)",
            "--tw-prose-th-borders": "var(--border-strong)",
            "--tw-prose-td-borders": "var(--border-strong)",
            a: { textDecoration: "underline", textUnderlineOffset: "2px", fontWeight: "500" },
            // Preflight (disabled above, corePlugins: false) normally supplies the
            // browser-independent `border-style: solid` default every prose ruleset
            // assumes is already in place — without it, blockquote's border-inline-
            // start-width/-color render with an implicit border-style of "none" and
            // the border simply doesn't paint even though width/color are both set.
            blockquote: { borderInlineStartStyle: "solid" },
            hr: { borderTopStyle: "solid" },
            code: {
              fontFamily: "var(--font-mono)",
              backgroundColor: "var(--accent-soft)",
              padding: "0.15em 0.4em",
              borderRadius: "var(--radius-sm)",
              fontWeight: "500",
            },
            "code::before": { content: "none" },
            "code::after": { content: "none" },
          },
        },
      },
    },
  },
  plugins: [
    require("@tailwindcss/typography")({ className: "article" }),
  ],
};
