import json,sys
ids=[int(x) for x in sys.argv[1].split(',')]
ent={}
for l in open('entries.jsonl'):
    e=json.loads(l); ent[e['n']]=e
dec={}
for l in open('decisions.jsonl'):
    d=json.loads(l); dec[d['n']]=d
for n in ids:
    e=ent[n]
    fin = dec[n].get('msgstr', e.get('msgstr')) if n in dec else e.get('msgstr')
    print(n, '| verdict:', dec[n]['verdict'] if n in dec else '-', '\n  SRC:', e.get('msgid','')[:160].replace('\n','\\n'), '\n  FIN:', str(fin)[:260].replace('\n','\\n'))
