"""In the applied changes, put back the translator's punctuation where the model only restored an em dash."""
import difflib
import json
import re
import subprocess
import sys

sys.path.insert(0, '../../../skill/scripts')
import po_tool as p

_, es = p.parse('original.po')
E = {e['n']: e for e in es}
A = [json.loads(l) for l in open('audited.jsonl', encoding='utf-8') if l.strip()]
edits = {json.loads(l)['n']: json.loads(l) for l in open('edits.jsonl', encoding='utf-8') if l.strip()}
TOK = re.compile(r'\s*—\s*|\s*[:;]\s*|\s*[(),]\s*|\s+|[^\s—:;(),]+')
PUNCT = re.compile(r'^\s*[—:;(),]\s*$')


def merge(o, h):
    a, b = TOK.findall(o), TOK.findall(h)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        seg_o, seg_h = a[i1:i2], b[j1:j2]
        if tag == 'replace' and any('—' in t for t in seg_h) and all(PUNCT.match(t) or not t.strip() for t in seg_h) \
                and all(PUNCT.match(t) or not t.strip() for t in seg_o):
            out += seg_o
        else:
            out += seg_h
    return ''.join(out)


changed = 0
for r in A:
    o = E[r['n']].get('msgstr')
    h = r.get('msgstr')
    if not o or not h or '—' in o or '—' not in h:
        continue
    m = merge(o, h)
    if m != h and m != o and m.count('—') == 0:
        e = edits.get(r['n'], {'n': r['n'], 'reason': ''})
        e['msgstr'] = m
        e['reason'] = (e.get('reason', '') + ' Se mantiene la puntuación del traductor en lugar de la raya.').strip()
        edits[r['n']] = e
        changed += 1
with open('edits.jsonl', 'w', encoding='utf-8') as f:
    for e in sorted(edits.values(), key=lambda x: x['n']):
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
print('punctuation restored in', changed)
