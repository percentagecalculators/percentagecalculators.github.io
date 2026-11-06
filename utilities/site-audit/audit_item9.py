"""Item 9: trailing-slash consistency. Usage: python3 audit_item9.py [public_dir]
Rule: every page URL is folder-style with a trailing slash, except the root home page,
which is always the bare origin (https://host) in canonical, hreflang, JSON-LD and sitemap."""
import os, re, sys
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public'))
ORIGIN = 'https://percentagecalculators.github.io'
ASSET = re.compile(r'\.(css|js|ico|webp|png|svg|xml|woff2|txt|jpg)$')
bad = []; n = 0
def chk(rel, kind, u):
    if u.startswith(ORIGIN): path = u[len(ORIGIN):]
    elif u.startswith('/') and not u.startswith('//'): path = u
    else: return
    if ASSET.search(path): return
    if u.startswith(ORIGIN) and path in ('', '/'):
        if path == '/': bad.append((rel, kind, u + '  (home must be non-slashed)'))
    elif u.startswith('/') and path == '/': return  # root-relative home link
    elif not path.endswith('/') or path.endswith('.html') or 'index' in path.rsplit('/', 1)[-1]:
        bad.append((rel, kind, u))
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.html') or f.startswith('google'): continue
        n += 1; p = os.path.join(d, f); rel = os.path.relpath(p, ROOT); h = open(p, encoding='utf-8').read()
        for m in re.finditer(r'(?:href|action)="([^"#?]*)', h): chk(rel, 'href', m.group(1))
        for m in re.finditer(r'"(?:url|item|@id)":\s*"([^"]*)"', h): chk(rel, 'jsonld', m.group(1))
sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
for u in re.findall(r'<loc>([^<]*)</loc>', sm): chk('sitemap.xml', 'loc', u)
home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
if '<link rel="canonical" href="%s">' % ORIGIN not in home: bad.append(('index.html', 'canonical', 'not bare origin'))
print(n, 'pages checked;', len(bad), 'problems')
for b in bad[:20]: print(' ', *b)
sys.exit(1 if bad else 0)
