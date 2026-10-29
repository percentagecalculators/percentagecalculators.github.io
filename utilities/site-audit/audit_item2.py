"""Item 2: unclosed/truncated/mis-nested tags in built pages. Usage: python3 audit_item2.py [public_dir]"""
import os, re, sys, collections
from html.parser import HTMLParser
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public'))
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
# elements whose end tag the HTML spec lets authors omit; flagged anyway for consistency
class C(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=False); s.stack = []; s.errs = []; s.counts = collections.Counter()
    def handle_starttag(s, t, a):
        s.counts[t] += 1
        if t not in VOID: s.stack.append((t, s.getpos()))
    def handle_startendtag(s, t, a):
        s.counts[t] += 1
        if t not in VOID and t not in ('svg','path','circle','rect','line','polyline','polygon','ellipse','g','use'): s.errs.append(f'self-closing non-void <{t}/> at {s.getpos()}')
    def handle_endtag(s, t):
        if t in VOID: s.errs.append(f'end tag for void </{t}> at {s.getpos()}'); return
        if not s.stack or t not in [x for x, _ in s.stack]: s.errs.append(f'stray </{t}> at {s.getpos()}'); return
        while s.stack and s.stack[-1][0] != t:
            s.errs.append(f'<{s.stack[-1][0]}> (line {s.stack[-1][1][0]}) not closed before </{t}> at {s.getpos()}'); s.stack.pop()
        s.stack.pop()
bad = collections.defaultdict(list); n = 0
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.html'): continue
        n += 1; p = os.path.join(d, f); rel = os.path.relpath(p, ROOT)
        h = open(p, encoding='utf-8').read(); c = C(); c.feed(h); c.close()
        for t, pos in c.stack: c.errs.append(f'<{t}> (line {pos[0]}) never closed')
        for t in ('html', 'head', 'body'):
            if c.counts[t] != 1: c.errs.append(f'{c.counts[t]}x <{t}>')
        if not h.startswith('<!DOCTYPE html>'): c.errs.append('no doctype at start')
        if not h.rstrip().endswith('</html>'): c.errs.append('does not end with </html>')
        for t in ('script', 'style', 'svg', 'template', 'textarea', 'select', 'table', 'form', 'details', 'ul', 'ol', 'a', 'p', 'li', 'div', 'section', 'main', 'nav', 'header', 'footer', 'aside', 'button', 'span'):
            o = len(re.findall(r'<%s[\s>]' % t, h)); cl = len(re.findall(r'</%s>' % t, h))
            if o != cl: c.errs.append(f'<{t}> opened {o} closed {cl}')
        # truncation heuristics: dangling '<' / unterminated attribute quote / comment
        if h.count('<!--') != h.count('-->'): c.errs.append('unbalanced comment')
        if re.search(r'<[a-zA-Z][^>]*$', h): c.errs.append('truncated tag at EOF')
        if c.errs: bad[rel] = c.errs
print(n, 'pages checked;', len(bad), 'with problems')
kinds = collections.Counter(re.sub(r'\d+', 'N', e)[:70] for v in bad.values() for e in v)
for k, v in kinds.most_common(12): print(f'  {v:5d}  {k}')
for rel, e in list(bad.items())[:5]: print(rel, e[:4])
sys.exit(1 if bad else 0)
