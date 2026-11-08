import json,sys
E={}
for l in open('entries.jsonl',encoding='utf-8'):
    e=json.loads(l); E[e['n']]=e
D={}
for l in open('decisions.jsonl',encoding='utf-8'):
    d=json.loads(l); D[d['n']]=d
def cur(n):
    e=E[n]; d=D.get(n)
    if d: return d.get('msgstr', ' | '.join(d.get('msgstr_plural',[])))
    return e.get('msgstr', ' | '.join(e.get('msgstr_plural',[])) if 'msgstr_plural' in e else '')
