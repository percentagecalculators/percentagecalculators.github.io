"""Item 3: HTML/class consistency per template. Usage: python3 audit_item3.py [public_dir]"""
import os, re, sys, collections
from html.parser import HTMLParser
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public'))
LANGS = 'ar bn de es fa fr hi id it ja ko ms nl pl pt ro ru th tr uk vi zh-cn zh-tw'.split()
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=False); s.el = []; s.stack = []
    def handle_starttag(s, t, a):
        d = dict(a); s.el.append((t, d.get('class', ''), tuple(s.stack))); 
        if t not in ('meta','link','br','hr','img','input','source'): s.stack.append((t, d.get('class', ''), d.get('id', '')))
    def handle_endtag(s, t):
        for i in range(len(s.stack) - 1, -1, -1):
            if s.stack[i][0] == t: del s.stack[i:]; break
def kind(h, rel):
    if rel == '404.html': return '404'
    if 'class="tool-section' in h or 'tool-section' in h[:20000] and '<form' in h: return 'tool'
    return 'page'
agg = collections.defaultdict(lambda: collections.defaultdict(list)); heads = {}; probs = collections.defaultdict(list)
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.html') or f.startswith('google'): continue
        p = os.path.join(d, f); rel = os.path.relpath(p, ROOT); h = open(p, encoding='utf-8').read()
        k = kind(h, rel)
        if rel in ('index.html',) or re.fullmatch(r'[a-z-]+/index\.html', rel): k = 'home' if 'basic-percent' in h else k
        x = P(); x.feed(h)
        main = [e for e in x.el if any(s[2] == 'main-content' or s[0] == 'main' for s in e[2])]
        hl = []
        for t, c, st in main:
            if t in ('h1','h2','h3','h4','h5','h6'):
                hl.append(int(t[1])); 
                ctx = 'article' if any('article' in (s[1] or '').split() or 'prose' in (s[1] or '') for s in st) else 'chrome'
                agg[(k, t, ctx)][c].append(rel)
            if t == 'p':
                ctx = 'article' if any('article' in (s[1] or '').split() for s in st) else 'chrome'
                agg[(k, 'p', ctx)][c].append(rel)
        if hl.count(1) != 1: probs['h1 count != 1'].append(f'{rel}: {hl.count(1)}')
        for a, b in zip(hl, hl[1:]):
            if b - a > 1: probs['skipped heading level'].append(f'{rel}: h{a}->h{b}'); break
        if hl and hl[0] != 1: probs['first heading not h1'].append(rel)
        # layout container widths on direct sections of <main>
        for t, c, st in x.el:
            if t == 'section' and len(st) <= 3: agg[(k, 'section', '')][re.sub(r'\s+', ' ', ' '.join(w for w in c.split() if w.startswith(('max-w', 'px-', 'mx-'))))].append(rel)
            if t == 'nav' or t == 'footer' or t == 'header':
                agg[('all', t, '')][c].append(rel)
        wm = re.findall(r'max-w-[0-9a-z\[\]./]+', ''.join(c for t, c, st in x.el if t in ('section', 'div') and c and 'mx-auto' in c))
        agg[(k, 'max-w-set', '')][' '.join(sorted(set(wm)))].append(rel)
print('page kinds:', collections.Counter(k for (k, *_), v in agg.items() if _[0] == 'section' for _ in [0]))
for key in sorted(agg):
    v = agg[key]
    if len(v) > 1:
        tot = sum(len(x) for x in v.values())
        print(f'{key}: {len(v)} variants over {tot} elements')
        for c, ps in sorted(v.items(), key=lambda kv: -len(kv[1]))[:5]: print(f'     {len(ps):5d}  {c[:110]!r}  e.g. {ps[0]}')
for k, v in probs.items(): print(f'\n{k}: {len(v)}'); [print('  ', x) for x in v[:5]]
