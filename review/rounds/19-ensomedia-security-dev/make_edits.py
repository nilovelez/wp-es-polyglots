import json
import re

REASON = '«host» aquí es la empresa: «proveedor de alojamiento», no «alojamiento».'
subs = [
    (r'\b(tu|Tu|mi|Mi|el|El) alojamiento (que|creasteis|conocéis|confirmó)', r'\1 proveedor de alojamiento \2'),
    (r'\b(de tu agencia o de tu) alojamiento\b', r'\1 proveedor de alojamiento'),
    (r'\b(desarrollador o a tu) alojamiento\b', r'\1 proveedor de alojamiento'),
]
rows = [json.loads(l) for l in open('decisions.jsonl', encoding='utf-8') if l.strip()]
out = []
for r in rows:
    def fix(s):
        for a, b in subs:
            s = re.sub(a, b, s)
        return s
    if 'msgstr' in r:
        new = fix(r['msgstr'])
        if new != r['msgstr']:
            out.append({'n': r['n'], 'msgstr': new, 'reason': REASON})
    elif 'msgstr_plural' in r:
        new = [fix(s) for s in r['msgstr_plural']]
        if new != r['msgstr_plural']:
            out.append({'n': r['n'], 'msgstr_plural': new, 'reason': REASON})
with open('edits.jsonl', 'w', encoding='utf-8') as f:
    for e in out:
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
print(len(out), [e['n'] for e in out])
