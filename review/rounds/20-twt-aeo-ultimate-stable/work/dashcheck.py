import json, sys
ROUND='/Volumes/Datos/repos/wp-es-polyglots/review/rounds/20-twt-aeo-ultimate-stable/'
a, b = int(sys.argv[1]), int(sys.argv[2])
decs = {}
for l in open(ROUND+'work/dec-1-750.jsonl' if len(sys.argv)<4 else sys.argv[3], encoding='utf-8'):
    d = json.loads(l); decs[d['n']] = d
def cur(e):
    if 'msgstr_plural' in e: return e['msgstr_plural']
    return [e['msgstr']]
for l in open(ROUND+'entries.jsonl', encoding='utf-8'):
    e = json.loads(l)
    if not (a <= e['n'] <= b): continue
    src = [e['msgid']] + ([e['msgid_plural']] if 'msgid_plural' in e else [])
    if not any('—' in s for s in src): continue
    tgt = decs[e['n']]['msgstr_plural'] if (e['n'] in decs and 'msgstr_plural' in decs[e['n']]) else (
          [decs[e['n']]['msgstr']] if e['n'] in decs else cur(e))
    for i, s in enumerate(src):
        if '—' not in s: continue
        t = tgt[min(i, len(tgt)-1)]
        if '—' not in t:
            print('LOST', e['n'], repr(t[:90]))
        else:
            # spacing: source " — " vs target
            sp_src = ' — ' in s
            sp_tgt = ' — ' in t
            if sp_src and not sp_tgt:
                print('SPACING', e['n'], repr(t[:120]))
