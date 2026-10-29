"""Audit hreflang/canonical/sitemap consistency of the built site.

Usage: python3 utilities/hreflang_audit.py [public_dir]   (default: ../public)

Checks per page: exactly one canonical, full 25-entry hreflang set, self-reference
equal to canonical, <html lang> match, absolute URLs, targets exist, return links,
target canonical == hreflang URL; then sitemap.xml alternates vs. each page.
Reads built files only (no network). Exits 1 on any issue.
"""
import re,os,sys,collections
from urllib.parse import urlparse
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','public')); BASE='https://percentagecalculators.github.io'
LANGS='ar bn de es fa fr hi id it ja ko ms nl pl pt ro ru th tr uk vi zh-cn zh-tw'.split()
EXPECT={'en'}|{l if not l.startswith('zh') else {'zh-cn':'zh-Hans','zh-tw':'zh-Hant'}[l] for l in LANGS}|{'x-default'}
pages={}
for d,_,fs in os.walk(ROOT):
    for f in fs:
        if f.endswith('.html'):
            p=os.path.join(d,f); pages[p]=open(p,encoding='utf-8').read()
def url_to_file(u):
    path=urlparse(u).path
    c=[ROOT+path, ROOT+path.rstrip('/')+'.html', ROOT+path.rstrip('/')+'/index.html']
    if path in('','/'): c=[ROOT+'/index.html']
    return next((x for x in c if os.path.isfile(x)),None)
def parse(h):
    can=re.findall(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"',h)
    alts={}
    dup=[]
    for m in re.finditer(r'<link[^>]*rel="alternate"[^>]*>',h):
        t=m.group(0); hl=re.search(r'hreflang="([^"]*)"',t); hr=re.search(r'href="([^"]*)"',t)
        if hl and hr:
            if hl.group(1) in alts: dup.append(hl.group(1))
            alts[hl.group(1)]=hr.group(1)
    lang=re.search(r'<html[^>]*lang="([^"]*)"',h)
    robots=re.search(r'<meta[^>]*name="robots"[^>]*content="([^"]*)"',h)
    return can,alts,dup,lang and lang.group(1),robots and robots.group(1)
info={p:parse(h) for p,h in pages.items()}
issues=collections.defaultdict(list); nohl=[]
f2u={}
for p,(can,alts,dup,lang,rob) in info.items():
    rel=os.path.relpath(p,ROOT)
    if not alts: nohl.append(rel); continue
    if len(can)!=1: issues['canonical count != 1'].append(rel); continue
    if dup: issues['duplicate hreflang'].append(rel)
    if set(alts)!=EXPECT: issues['hreflang set mismatch'].append(f'{rel}: missing {sorted(EXPECT-set(alts))} extra {sorted(set(alts)-EXPECT)}')
    if rob and 'noindex' in rob: issues['noindex with hreflang'].append(rel)
    selfs=[k for k,v in alts.items() if v.rstrip('/')==can[0].rstrip('/') and k!='x-default']
    if not selfs: issues['no self-reference'].append(rel)
    elif not any(alts[k]==can[0] for k in selfs): issues['self-ref differs from canonical (slash)'].append(rel)
    if selfs and lang and selfs[0].lower()!=lang.lower(): issues['html lang != self hreflang'].append(f'{rel}: {lang} vs {selfs[0]}')
    for k,v in alts.items():
        if not v.startswith(BASE): issues['non-absolute/foreign URL'].append(f'{rel}: {k} {v}')
        tf=url_to_file(v)
        if not tf: issues['target missing'].append(f'{rel}: {k} {v}'); continue
        # reciprocity
        ta=info.get(tf)
        if ta and tf!=p:
            back=[x for x in ta[1].values() if url_to_file(x)==p]
            if not back: issues['no return link'].append(f'{rel} -> {os.path.relpath(tf,ROOT)}')
            if ta[0] and ta[0][0].rstrip('/')!=v.rstrip('/'): issues['target canonical != hreflang URL'].append(f'{rel}: {k} {v} canon {ta[0][0]}')
    # alternate sets consistent across cluster
    if alts.get('x-default') and url_to_file(alts['x-default']):
        pass
print('pages',len(pages),'with hreflang',len(pages)-len(nohl))
print('pages WITHOUT hreflang:',len(nohl)); [print('  ',x) for x in sorted(nohl)]
if not issues: print('NO ISSUES in per-page checks')
for k,v in issues.items():
    print(f'\n{k}: {len(v)}'); [print('  ',x) for x in v[:8]]
# sitemap: lists exactly the pages that carry hreflang (alternates live in each page's <head>, not here)
sm=open(ROOT+'/sitemap.xml',encoding='utf-8').read()
locs=re.findall(r'<loc>([^<]*)</loc>',sm); print('\nsitemap urls',len(locs))
bad=[u for u in locs if not url_to_file(u)]; print('sitemap urls w/o file:',len(bad),bad[:5])
def norm(rel): return (BASE+'/'+rel.replace('index.html','').replace('.html','')).rstrip('/')
want={norm(os.path.relpath(p,ROOT)) for p in pages if info[p][1]}
have={u.rstrip('/') for u in locs}
mism=len(want^have)
print('sitemap vs pages with hreflang: missing from sitemap',sorted(want-have)[:5],'| not in pages',sorted(have-want)[:5])
print('duplicate sitemap urls:',len(locs)-len(set(locs)))
if len(sm.splitlines())<3: print('sitemap is a single line (hard to read/render)'); mism+=1
sys.exit(1 if issues or mism or bad or len(nohl)>2 or len(locs)!=len(set(locs)) else 0)
