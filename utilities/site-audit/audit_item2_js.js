// Item 2b: every distinct inline <script> and JSON-LD block in public/ must parse (catches truncated scripts).
const fs = require("fs"), path = require("path"), vm = require("vm"), crypto = require("crypto");
const ROOT = path.resolve(process.argv[2] || path.join(__dirname, "..", "..", "public"));
const seen = new Map(); let pages = 0, blocks = 0, bad = [];
(function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : f.endsWith(".html") && check(p); } })(ROOT);
function check(p) {
  pages++; const h = fs.readFileSync(p, "utf8");
  for (const m of h.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)) {
    const attrs = m[1], body = m[2]; if (/\bsrc=/.test(attrs) || !body.trim()) continue;
    const key = crypto.createHash("md5").update(attrs + body).digest("hex"); blocks++;
    if (seen.has(key)) continue; seen.set(key, p);
    try {
      if (/application\/ld\+json/.test(attrs)) JSON.parse(body); else new vm.Script(body);
    } catch (e) { bad.push(`${path.relative(ROOT, p)}: ${e.message.split("\n")[0]}`); }
  }
}
console.log(`${pages} pages, ${blocks} inline blocks, ${seen.size} distinct; ${bad.length} failed to parse`);
bad.slice(0, 10).forEach(x => console.log("  " + x)); process.exit(bad.length ? 1 : 0);
