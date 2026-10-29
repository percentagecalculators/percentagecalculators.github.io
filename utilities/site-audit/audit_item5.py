"""Item 5 (static part): desktop nav vs mobile drawer parity + no sticky/fixed nav. Usage: python3 audit_item5.py [public_dir]"""
import os, re, sys, collections
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public'))
def seg(h, marker):
    i = h.find(marker)
    if i < 0: return None
    st = h.rfind('<', 0, i + 1); name = re.match(r'<(\w+)', h[st:]).group(1); depth = 0
    for m in re.finditer(r'<(/?)%s\b[^>]*>' % name, h[st:]):
        depth += -1 if m.group(1) else 1
        if depth == 0: return h[st:st + m.end()]
links = lambda s: re.findall(r'<a [^>]*?href="([^"]*)"', s)
bad = collections.defaultdict(list); n = 0; sig = collections.Counter()
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.html') or f.startswith('google'): continue
        n += 1; p = os.path.join(d, f); rel = os.path.relpath(p, ROOT); h = open(p, encoding='utf-8').read()
        hdr, drw, ftr = seg(h, '<header'), seg(h, 'id="navDrawer"'), seg(h, '<footer')
        if not (hdr and drw): bad['missing header/drawer'].append(rel); continue
        # desktop menu = header minus language switcher links (they carry hreflang) and logo
        desk = {l for a in re.findall(r'<a [^>]*>', hdr) for l in [re.search(r'href="([^"]*)"', a).group(1)] if 'hreflang=' not in a}
        mob = {l for a in re.findall(r'<a [^>]*>', drw) for l in [re.search(r'href="([^"]*)"', a).group(1)] if 'hreflang=' not in a}
        if desk - mob: bad['in desktop menu, missing from mobile drawer'].append(f'{rel}: {sorted(desk - mob)[:3]}')
        if mob - desk: bad['in mobile drawer, missing from desktop menu'].append(f'{rel}: {sorted(mob - desk)[:3]}')
        dl = {re.search(r'hreflang="([^"]*)"', a).group(1) for a in re.findall(r'<a [^>]*hreflang=[^>]*>', hdr)}
        ml = {re.search(r'hreflang="([^"]*)"', a).group(1) for a in re.findall(r'<a [^>]*hreflang=[^>]*>', drw)}
        if dl != ml: bad['language list differs desktop vs mobile'].append(rel)
        if 'themeToggleBtn' not in hdr: bad['theme toggle missing in header'].append(rel)
        # the header bar itself must scroll away; the drawer panel is an off-canvas overlay (fixed by design)
        if re.search(r'\b(sticky|fixed)\b', re.search(r'<\w+[^>]*>', hdr).group(0)): bad['header root is sticky/fixed'].append(rel)
        if re.search(r'class="[^"]*\b(sticky|top-0)\b', hdr): bad['sticky/top-0 inside header'].append(rel)
        sig[(len(desk), len(mob))] += 1
print(n, 'pages checked; (desktop unique links, drawer unique links) signatures:', dict(sig))
css = open(os.path.join(ROOT, 'tailwind.min.css')).read() + open(os.path.join(ROOT, 'base.min.css')).read()
print('position:sticky in CSS rules:', len(re.findall(r'position:sticky', css)), '(utility .sticky used on pages:', sum('class="' in open(os.path.join(d, f), encoding='utf-8').read() and bool(re.search(r'class="[^"]*\bsticky\b', open(os.path.join(d, f), encoding='utf-8').read())) for d, _, fs in os.walk(ROOT) for f in fs if f.endswith('.html')), ')')
if not bad: print('NO ISSUES')
for k, v in bad.items(): print(f'\n{k}: {len(v)}'); [print('  ', x) for x in v[:6]]
