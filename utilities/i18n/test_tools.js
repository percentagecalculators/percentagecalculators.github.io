#!/usr/bin/env node
/* Functional test of every calculator on every built page, all languages.
 *
 *   npm install --prefix .test-cache jsdom      (once; folder is gitignored)
 *   NODE_PATH=.test-cache/node_modules node utilities/i18n/test_tools.js [lang ...]
 *
 * For each tool the English page is the oracle: its inputs are filled with the
 * first value preset that yields results, every <output> is recorded, and each
 * translated page must (1) load with no script errors, (2) expose the same
 * input/output ids, (3) produce identical outputs for the same inputs, and
 * (4) clear all inputs/outputs with its reset button. Uses the built public/. */
const { JSDOM, VirtualConsole, requestInterceptor } = require("jsdom");
const fs = require("fs");
const path = require("path");

const PUB = path.resolve(__dirname, "..", "..", "public");
const SRC = path.resolve(__dirname, "..", "..", "src");
const slugs = fs.readdirSync(path.join(SRC, "content")).filter(f => f.endsWith(".json") && f !== "pages.json").map(f => f.slice(0, -5)).sort();
const HOME = "percentage-calculator";
const langs = fs.readdirSync(path.join(SRC, "content", "i18n")).sort();
const wanted = process.argv.slice(2);
const PRESETS = [
  [200, 15, 12, 5, 30, 40, 25, 8],
  [80, 20, 4, 10, 50, 100, 7, 3],
  [1500, 6.5, 36, 12, 2, 90, 45, 15],
];

function pageFile(lang, slug) {
  if (lang === "en") return path.join(PUB, slug === HOME ? "index.html" : slug + ".html");
  return path.join(PUB, lang, slug === HOME ? "index.html" : path.join(slug, "index.html"));
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// Pages load the shared script as <script defer src="/site.min.js?v=..">: serve it from public/;
// every other external resource (KaTeX CDN, gtag) answers an empty 200, as if it were not fetched at all.
const ORIGIN = "https://percentagecalculators.github.io";
const loader = {
  interceptors: [requestInterceptor(request => {
    const u = new URL(request.url);
    if (u.origin === ORIGIN && u.pathname === "/site.min.js")
      return new Response(fs.readFileSync(path.join(PUB, "site.min.js")), { headers: { "Content-Type": "application/javascript" } });
    return new Response("", { status: 200 });
  })],
};

async function load(file) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", e => errors.push(String(e.message || e).split("\n")[0]));
  const dom = new JSDOM(fs.readFileSync(file, "utf8"), {
    url: ORIGIN + "/",
    runScripts: "dangerously", pretendToBeVisual: true, virtualConsole: vc, resources: loader,
    // browser APIs jsdom lacks that the site's nav script touches on load
    beforeParse(w) {
      w.matchMedia = w.matchMedia || (q => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} }));
      w.ResizeObserver = w.ResizeObserver || class { observe() {} unobserve() {} disconnect() {} };
      w.IntersectionObserver = w.IntersectionObserver || class { observe() {} unobserve() {} disconnect() {} };
    },
  });
  dom.window.addEventListener("error", e => errors.push("window.onerror: " + e.message));
  if (dom.window.document.readyState !== "complete") await new Promise(r => dom.window.addEventListener("load", r));
  await sleep(30);
  return { dom, doc: dom.window.document, win: dom.window, errors };
}

function fields(doc) {
  return [...doc.querySelectorAll(".tool-section form input[id], .tool-section form textarea[id]")]
    .filter(el => !["submit", "button", "hidden"].includes(el.type));
}
function outputs(doc) {
  const o = {};
  doc.querySelectorAll("output[id]").forEach(el => { o[el.id] = el.textContent.trim(); });
  return o;
}
const isEmpty = t => t === "" || t === "–" || t === "-" || /^\$?\?$/.test(t);  // "?" / "$?": legacy reset glyph (noted, not a failure)
const legacyGlyph = new Set();  // tools whose reset shows ? instead of an en dash

function fill(page, preset) {
  const { doc, win } = page;
  let n = 0, t = 0;
  for (const el of fields(doc)) {
    if (el.tagName === "TEXTAREA") el.value = t++ === 0 ? "30, 50, 20, 40" : "10, 20, 30, 40";
    else el.value = String(preset[n++ % preset.length]);
    el.dispatchEvent(new win.Event("input", { bubbles: true }));
  }
  doc.querySelectorAll("button[onclick]").forEach(b => {
    if (/^calc/i.test(b.getAttribute("onclick"))) b.click();
  });
  return outputs(doc);
}

async function oracle(slug) {
  for (let i = 0; i < PRESETS.length; i++) {
    const page = await load(pageFile("en", slug));
    const out = fill(page, PRESETS[i]);
    const ids = fields(page.doc).map(e => e.id);
    page.win.close();
    if (Object.values(out).some(v => !isEmpty(v))) return { preset: i, out, ids, errors: page.errors };
  }
  return null;
}

async function main() {
  const targets = wanted.length ? wanted : ["en", ...langs];
  const oracles = {};
  const failures = [];
  let tested = 0;
  for (const slug of slugs) {
    oracles[slug] = await oracle(slug);
    if (!oracles[slug]) failures.push(`en/${slug}: no preset produced a result (cannot test)`);
    else if (oracles[slug].errors.length) failures.push(`en/${slug}: script errors: ${oracles[slug].errors.join("; ")}`);
  }
  const perLang = {};
  for (const lang of targets) {
    perLang[lang] = { pass: 0, fail: 0 };
    for (const slug of slugs) {
      const o = oracles[slug];
      if (!o) continue;
      const tag = `${lang}/${slug}`;
      const problems = [];
      let page;
      try { page = await load(pageFile(lang, slug)); } catch (e) { failures.push(`${tag}: cannot load (${e.message})`); perLang[lang].fail++; continue; }
      if (page.errors.length) problems.push("script errors: " + page.errors.join("; "));
      const ids = fields(page.doc).map(e => e.id);
      if (JSON.stringify(ids) !== JSON.stringify(o.ids)) problems.push(`input ids differ: ${ids} vs ${o.ids}`);
      const out = fill(page, PRESETS[o.preset]);
      for (const id of Object.keys(o.out)) {
        if (out[id] !== o.out[id]) problems.push(`output #${id}: "${out[id]}" != English "${o.out[id]}"`);
      }
      // reset button clears every field and result
      const reset = page.doc.querySelector(".reset-btn");
      if (!reset) problems.push("no reset button");
      else {
        reset.click();
        await sleep(5);
        const left = fields(page.doc).filter(e => e.value !== "").map(e => e.id);
        const stale = Object.entries(outputs(page.doc)).filter(([, v]) => !isEmpty(v)).map(([k]) => k);
        Object.values(outputs(page.doc)).forEach(v => { if (/^\$?\?$/.test(v)) legacyGlyph.add(slug); });
        if (left.length) problems.push("reset left values in: " + left);
        if (stale.length) problems.push("reset left outputs in: " + stale);
      }
      page.win.close();
      tested++;
      if (problems.length) { perLang[lang].fail++; failures.push(`${tag}: ${problems.join(" | ")}`); }
      else perLang[lang].pass++;
    }
    process.stdout.write(`${lang.padEnd(6)} ${perLang[lang].pass} pass, ${perLang[lang].fail} fail\n`);
  }
  console.log(`\n${tested} pages tested across ${targets.length} language(s), ${slugs.length} tools each`);
  if (legacyGlyph.size) console.log(`note: reset shows "?" instead of "–" in ${legacyGlyph.size} tool(s) (same in every language, incl. English): ${[...legacyGlyph].join(", ")}`);
  if (failures.length) {
    console.log(`\n${failures.length} FAILURE(S):`);
    failures.slice(0, 60).forEach(f => console.log(" - " + f));
    process.exit(1);
  }
  console.log("ALL PASS");
}
main().catch(e => { console.error(e); process.exit(2); });
