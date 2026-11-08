import json,sys
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for l in open('/Volumes/Datos/repos/wp-es-polyglots/review/rounds/21-gratora-donation-platform-stable/work/entries-all.jsonl'):
    e=json.loads(l)
    if not (lo<=e['n']<=hi): continue
    s='%d'%e['n']
    if 'ctx' in e: s+=' [ctx:%s]'%e['ctx']
    if 'note' in e: s+=' (%s)'%e['note']
    if 'flags' in e: s+=' {%s}'%','.join(e['flags'])
    print(s); print('  S: '+e['msgid'].replace(chr(10),'\\n'))
    if 'msgid_plural' in e: print('  SP: '+e['msgid_plural'])
    print('  T: '+(e['msgstr'].replace(chr(10),'\\n') if 'msgstr' in e else ' || '.join(e['msgstr_plural'])))
