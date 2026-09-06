// Compiled-CSS replacement for the old Play CDN runtime config (see
// generate.py's compile_tailwind_css()). `content` is intentionally empty
// here -- generate.py always passes the real glob via the CLI's --content
// flag (pointing at that build's freshly-rendered HTML output directory,
// which doesn't have a fixed path since it's a fresh tempdir on minified
// builds), and --content overrides this array entirely.
//
// Keep colors/fontFamily in sync with base.css's custom-property tokens and
// @font-face names by hand -- this file has no way to read base.css itself.
module.exports = {
  darkMode: "class",
  content: [],
  theme: {
    extend: {
      colors: {
        bg: "rgb(var(--color-bg) / <alpha-value>)",
        "bg-alt": "rgb(var(--color-bg-alt) / <alpha-value>)",
        surface: "rgb(var(--color-surface) / <alpha-value>)",
        "surface-alt": "rgb(var(--color-surface-alt) / <alpha-value>)",
        border: "rgb(var(--color-border) / <alpha-value>)",
        "border-strong": "rgb(var(--color-border-strong) / <alpha-value>)",
        text: "rgb(var(--color-text) / <alpha-value>)",
        "text-alt": "rgb(var(--color-text-alt) / <alpha-value>)",
        "text-secondary": "rgb(var(--color-text-secondary) / <alpha-value>)",
        "text-muted": "rgb(var(--color-text-muted) / <alpha-value>)",
        accent: "rgb(var(--color-accent) / <alpha-value>)",
        "accent-dark": "rgb(var(--color-accent-dark) / <alpha-value>)",
        "accent-darker": "rgb(var(--color-accent-darker) / <alpha-value>)",
        warning: "rgb(var(--color-warning) / <alpha-value>)",
        danger: "rgb(var(--color-danger) / <alpha-value>)",
      },
      fontFamily: {
        sans: ["DM Sans", "DM Sans Fallback", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "JetBrains Mono Fallback", "monospace"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
