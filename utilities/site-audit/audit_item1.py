"""Item 1: SEO/technical audit of built pages. Usage: python3 audit_item1.py [public_dir]"""
import os, re, sys, collections
from html.parser import HTMLParser
from urllib.parse import urlparse, urldefrag, unquote
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public'))
BASE = 'https://percentagecalculators.github.io'
pages = {}
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(d, f); pages[p] = open(p, encoding='utf-8').read()

def page_url(p):
    rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
    if rel.endswith('index.html'): rel = rel[:-len('index.html')]
    elif rel.endswith('.html'): rel = rel[:-5]
    return '/' + rel
def resolve(path):
    """URL path -> file under ROOT or None (GitHub Pages rules)."""
    path = unquote(path)
    c = [ROOT + path, ROOT + path + '.html', ROOT + path.rstrip('/') + '/index.html'] if path != '/' else [ROOT + '/index.html']
    if path.endswith('/'): c = [ROOT + path + 'index.html']
    return next((x for x in c if os.path.isfile(x)), None)

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=False); s.tags = []; s.ids = set(); s.links = []; s.assets = []; s.stack = []
        s.in_title = False; s.title = ''; s.in_head = False
    def handle_starttag(s, t, a):
        s.tags.append((t, a, [k for k, _ in a], s.getpos()))
        d = dict(a)
        if 'id' in d: s.ids.add(d['id'])
        if t == 'a' and 'href' in d: s.links.append(d['href'])
        if t in ('img', 'script', 'source') and 'src' in d: s.assets.append(d['src'])
        if t == 'link' and 'href' in d: s.assets.append(d['href'])
        if t == 'title': s.in_title = True
    def handle_endtag(s, t):
        if t == 'title': s.in_title = False
    def handle_data(s, d):
        if s.in_title: s.title += d
info = {}
for p, h in pages.items():
    x = P(); x.feed(h); info[p] = x

issues = collections.defaultdict(list)
def bad(k, p, msg=''): issues[k].append(os.path.relpath(p, ROOT) + (': ' + msg if msg else ''))
LANGS = 'ar bn de es fr hi id it ja ko ms nl pt ru th vi zh-cn zh-tw'.split()
def lang_of(rel):
    f = rel.split(os.sep)[0]
    return f if os.sep in rel and f in LANGS else 'en'
titles = collections.defaultdict(list); descs = collections.defaultdict(list)
for p, x in info.items():
    h = pages[p]; rel = os.path.relpath(p, ROOT)
    is_special = rel in ('google7cc5de103ad575d0.html',)
    if is_special: continue
    metas = [(a, k) for t, a, k, _ in x.tags if t == 'meta']
    md = lambda n: [dict(a) for a, _ in metas if dict(a).get('name') == n]
    title = x.title.strip()
    if not title: bad('missing <title>', p)
    else:
        titles[(lang_of(rel), title)].append(rel)
        if len(title) > 70: bad('title > 70 chars', p, f'{len(title)}')
    d = md('description')
    if rel != '404.html':
        if len(d) != 1: bad('meta description count != 1', p, str(len(d)))
        elif not d[0].get('content', '').strip(): bad('empty meta description', p)
        else:
            descs[(lang_of(rel), d[0]['content'])].append(rel)
            if len(d[0]['content']) > 200: bad('description > 200 chars', p, str(len(d[0]['content'])))
    vp = md('viewport')
    if len(vp) != 1 or vp[0].get('content').replace(' ', '') not in ('width=device-width,initial-scale=1.0', 'width=device-width,initial-scale=1'): bad('viewport missing/odd', p, str(vp))
    if not any(dict(a).get('charset') for a, _ in metas): bad('no charset', p)
    can = [dict(a) for t, a, k, _ in x.tags if t == 'link' and dict(a).get('rel') == 'canonical']
    if rel != '404.html':
        if len(can) != 1: bad('canonical count != 1', p, str(len(can)))
        else:
            exp = BASE + page_url(p)
            if can[0]['href'] != exp: bad('canonical != own URL', p, f"{can[0]['href']} vs {exp}")
    if not re.search(r'<html[^>]*\blang="[^"]+"', h): bad('html lang missing', p)
    # attribute order
    for t, a, keys, pos in x.tags:
        if t == 'meta' and 'content' in keys and any(k in keys for k in ('name', 'property', 'http-equiv')):
            if keys.index('content') < min(keys.index(k) for k in ('name', 'property', 'http-equiv') if k in keys): bad('reversed attr order <meta content before name>', p, str(keys))
        if t == 'link' and 'rel' in keys and 'href' in keys and keys.index('href') < keys.index('rel'): bad('reversed attr order <link href before rel>', p, str(keys))
        if t == 'link' and 'hreflang' in keys and keys.index('hreflang') < keys.index('rel'): bad('reversed <link hreflang before rel>', p)
    # invalid chars
    for rx, name in ((r'�', 'U+FFFD replacement char'), (r'[\x00-\x08\x0b\x0c\x0e-\x1f]', 'control chars'), (r'â€|Ã.|Â\s', 'mojibake'), (r'&(?=[A-Za-z0-9#])(?!(?:[a-zA-Z0-9]+|#\d+|#x[0-9a-fA-F]+);)', 'ambiguous & (looks like an entity but is not)')):
        hs = re.sub(r'<script\b[^>]*>.*?</script>', '', h, flags=re.S)
        m = re.search(rx, hs)
        if m: bad('invalid char: ' + name, p, repr(hs[max(0, m.start() - 25):m.end() + 25]))
    # links
    for href in x.links:
        if href.startswith(('mailto:', 'tel:', 'javascript:')) or href == '': 
            if href == '': bad('empty href', p)
            continue
        u = urlparse(href)
        if u.scheme in ('http', 'https') and u.netloc != 'percentagecalculators.github.io': continue
        path = u.path or page_url(p)
        if u.netloc == 'percentagecalculators.github.io': bad('absolute internal link', p, href)
        if not path.startswith('/') : bad('relative link', p, href); continue
        if path.endswith('.html'): bad('.html in internal link', p, href)
        tf = resolve(path)
        if not tf: bad('BROKEN internal link', p, href); continue
        if u.fragment and tf in info and u.fragment not in info[tf].ids and u.fragment != 'top': bad('broken #anchor', p, href)
    for src in x.assets:
        u = urlparse(src)
        if u.scheme or src.startswith('//') or src.startswith('data:'): continue
        if not src.startswith('/'): bad('relative asset', p, src); continue
        if not os.path.exists(ROOT + unquote(u.path)): bad('BROKEN asset', p, src)
for (l, t), ps in titles.items():
    if len(ps) > 1: issues['duplicate <title> within language'].append(f'{len(ps)}x "{t[:60]}": {ps[:3]}')
for (l, t), ps in descs.items():
    if len(ps) > 1: issues['duplicate description'].append(f'{len(ps)}x: {ps[:3]}')

# menu/footer consistency: within each language, header nav + footer must be identical modulo active link / lang switcher
def seg(h, a, b=None):
    """Element whose open tag contains marker `a` (balanced by tag name)."""
    i = h.find(a)
    if i < 0: return None
    st = h.rfind('<', 0, i + 1); name = re.match(r'<(\w+)', h[st:]).group(1)
    depth = 0
    for m in re.finditer(r'<(/?)%s\b[^>]*>' % name, h[st:]):
        depth += -1 if m.group(1) else 1
        if depth == 0: return h[st:st + m.end()]
    return None
variants = collections.defaultdict(lambda: collections.defaultdict(list))
for p, h in pages.items():
    rel = os.path.relpath(p, ROOT)
    if rel == 'google7cc5de103ad575d0.html': continue
    lang = rel.split(os.sep)[0] if os.sep in rel and rel.split(os.sep)[0] in 'ar bn de es fr hi id it ja ko ms nl pt ru th vi zh-cn zh-tw'.split() else 'en'
    hdr = seg(h, '<header'); ftr = seg(h, '<footer'); drw = seg(h, 'id="navDrawer"')
    def norm(s):
        if s is None: return None
        s = re.sub(r'\saria-current="page"', '', s)
        s = re.sub(r'<div class="lang-switch.*?</div></div>|<details class="lang.*?</details>', '', s, flags=re.S)
        s = re.sub(r'<a [^>]*hreflang=[^>]*>.*?</a>', '', s, flags=re.S)  # language switcher links vary per page
        return s
    for name, sgm in (('header', hdr), ('footer', ftr), ('drawer', drw)):
        if sgm is None: issues[f'{name} missing'].append(rel); continue
        variants[(lang, name)][norm(sgm)].append(rel)
print('pages', len(pages))
for (lang, name), v in sorted(variants.items()):
    if len(v) > 1:
        sizes = sorted((len(x) for x in v.values()), reverse=True)
        print(f'  {lang} {name}: {len(v)} variants, page counts {sizes}; e.g. minority: {sorted(v.values(), key=len)[0][:3]}')
if not issues: print('NO ISSUES')
for k, v in sorted(issues.items()):
    print(f'\n{k}: {len(v)}'); [print('  ', x) for x in v[:6]]
