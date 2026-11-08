import json, sys
a, b = int(sys.argv[1]), int(sys.argv[2])
for l in open('/Volumes/Datos/repos/wp-es-polyglots/review/rounds/20-twt-aeo-ultimate-stable/entries.jsonl'):
    e = json.loads(l)
    if not (a <= e['n'] <= b):
        continue
    if 'msgstr_plural' in e:
        s = ' || '.join(f'[{i}] {x}' for i, x in enumerate(e['msgstr_plural']))
        print(f"{e['n']} S: {e['msgid']} || {e['msgid_plural']}\n   T: {s}")
    else:
        print(f"{e['n']} S: {e['msgid']}\n   T: {e['msgstr']}")
