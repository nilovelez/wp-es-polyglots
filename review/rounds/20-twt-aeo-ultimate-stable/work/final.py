import json,re,sys
ROUND='/Volumes/Datos/repos/wp-es-polyglots/review/rounds/20-twt-aeo-ultimate-stable/'
dec={}
for l in open(ROUND+'decisions.jsonl',encoding='utf-8'):
    d=json.loads(l); dec[d['n']]=d
final={}; src={}
for l in open(ROUND+'entries.jsonl',encoding='utf-8'):
    e=json.loads(l)
    src[e['n']]=e
    if e['n'] in dec:
        d=dec[e['n']]
        final[e['n']]= d.get('msgstr_plural') or d.get('msgstr')
    else:
        final[e['n']]= e.get('msgstr_plural') or e.get('msgstr')
def cur(n):
    v=final[n]; return v if isinstance(v,list) else [v]
def srcs(n):
    e=src[n]; return [e['msgid']]+([e['msgid_plural']] if 'msgid_plural' in e else [])
if __name__=='__main__':
    pat=re.compile(sys.argv[1], re.I)
    mode=sys.argv[2] if len(sys.argv)>2 else 'out'
    cnt=0
    for n in sorted(final):
        for t in cur(n):
            if pat.search(t):
                cnt+=1
                if cnt<=int(sys.argv[3]) if len(sys.argv)>3 else 60:
                    print(n, '|', srcs(n)[0][:90].replace('\n',' '), '||', t[:150].replace('\n',' '))
    print('TOTAL', cnt)
