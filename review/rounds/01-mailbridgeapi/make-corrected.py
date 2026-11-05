import os, re
# Builds corrected.po for this round from original.po and repaired.po.
d=os.path.dirname(os.path.abspath(__file__))+os.sep
O=d+'original.po'
R=d+'repaired.po'
def parse(p):
    out=[];cur=None;mode=None
    for line in open(p,encoding='utf8'):
        line=line.rstrip('\n')
        if line.startswith('#'):
            if cur is None or cur.get('done'):
                cur={'c':[],'id':'','str':''};out.append(cur)
            cur['c'].append(line);continue
        if line.startswith('msgid '):
            if cur is None or cur.get('done'):
                cur={'c':[],'id':'','str':''};out.append(cur)
            mode='id';cur['id']=line[6:].strip()[1:-1];continue
        if line.startswith('msgstr '):
            mode='str';cur['str']=line[7:].strip()[1:-1];continue
        if line.startswith('"'):
            cur[mode]+=line[1:-1];continue
        if line=='' and cur: cur['done']=True
    return out
o=parse(O); r=parse(R)
om={e['id']:e for e in o if e['id']}
rm={e['id']:e['str'] for e in r if e['id']}
def key(s): return next(k for k in om if k.startswith(s))
fix={
 key('Add the <code>mailbridgeapi_email_delivery_source'):"Añadido el filtro <code>mailbridgeapi_email_delivery_source</code> para integraciones especializadas de WordPress.",
 key('Add the translation template'):"Añadida la plantilla de traducción.",
 key('Detect common competing'):"Añadida la detección de plugins SMTP y de entrega de correo electrónico habituales que pueden entrar en conflicto.",
 key('Add real end-to-end'):"Añadida la entrega real de correos electrónicos de prueba de extremo a extremo con resultado persistente del proveedor e ID de mensaje.",
 key('Secure dashboard email/password'):"Conexión segura con el correo electrónico y la contraseña del escritorio y selección bloqueada del buzón.",
 key('Email compatibility'):"Compatibilidad con el correo electrónico",
 key('Show a clear in-progress'):"Mostrado un estado de progreso claro mientras se ejecuta una prueba de conexión.",
 key('Harden administrator'):"Reforzada la validación de las solicitudes del administrador y documentados los filtros de solo lectura.",
 key('Sanitize every administrator'):"Saneados todos los campos de las solicitudes del administrador antes de utilizarlos, incluidos los datos de verificación de nonce.",
}
h=key('The plugin does not store SMTP host names')
fix[h]=om[h]['str'].replace('nombres de servidor SMTP','nombres de host SMTP'); assert fix[h]!=om[h]['str']
hdr=open(O,encoding='utf8').read().split('\n\n')[0]
out=[hdr,''];n=0
for e in o:
    if not e['id']: continue
    t=fix.get(e['id'],rm.get(e['id'],e['str']))
    if t==e['str']: continue
    n+=1
    for c in e['c']: out.append(c)
    out.append('msgid ""');out.append('"'+e['id']+'"');out.append('msgstr ""');out.append('"'+t+'"');out.append('')
p=d+'corrected.po'
open(p,'w',encoding='utf8').write('\n'.join(out))
print(n,'cambios de',len([e for e in o if e['id']]))
bad=0
for e in o:
    if not e['id']: continue
    t=fix.get(e['id'],rm.get(e['id'],e['str']))
    for pat in (r'<[^>]+>',r'%\d?\$?[sd]|%i',r'&\w+;',r'\{[^}]+\}'):
        if sorted(re.findall(pat,e['id']))!=sorted(re.findall(pat,t)): bad+=1;print('MISMATCH',e['id'][:40])
print('mismatches',bad)
