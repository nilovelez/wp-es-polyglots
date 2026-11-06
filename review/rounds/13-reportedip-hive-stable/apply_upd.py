import json
ent={}
for l in open('entries.jsonl'):
    e=json.loads(l); ent[e['n']]=e
dec={}
order=[]
for l in open('decisions.jsonl'):
    d=json.loads(l); dec[d['n']]=d; order.append(d['n'])
def fin(n):
    if n in dec and 'msgstr' in dec[n]: return dec[n]['msgstr']
    return ent[n].get('msgstr')
AUTH_CMT='Según el glosario y la guía, «authentication» se traduce como «identificación» y «two-factor» como «dos pasos»; no se usan anglicismos.'
WL_CMT='Según el criterio del equipo, «whitelist» como verbo o adjetivo se traduce como «añadir a los admitidos» o «admitido»; «lista blanca» se mantiene como sustantivo.'
AUTH_SPECIFIC={
 174:('Autenticador','App de identificación'),
 181:('Código del autenticador','Código de la app de identificación'),
 420:('El autenticador no ha confirmado','El dispositivo de identificación no ha confirmado'),
}
AUTH_REPL=[('autenticación de dos factores','identificación en dos pasos'),('Autenticación de dos factores','Identificación en dos pasos'),('dos factores','dos pasos'),('Dos factores','Dos pasos'),('autenticación','identificación'),('Autenticación','Identificación')]
AUTH=[173,174,175,180,181,192,202,219,220,293,333,353,354,355,358,361,362,369,385,387,388,396,400,420,427,449,456,457,460,461,463,464,590,610,727,928,1070,1084,1086,1111,1181,1183,1188,1192,1193,1218,1224,1227,1244,1252,1261,1266,1761,1958]
WL={57:[('añade una dirección a la lista blanca','añade una dirección a los admitidos')],
 496:[('añadir esta IP a la lista blanca','añadir esta IP a los admitidos')],
 506:[('añadir a la lista blanca','añadir a los admitidos')],
 507:[('Añadida manualmente a la lista blanca','Añadida manualmente a los admitidos')],
 865:[('IP añadida a la lista blanca','IP admitida')],
 873:[('(en lista blanca)','(admitida)')],
 955:[('ya está en la lista blanca','ya está entre las admitidas')],
 956:[('añadido a la lista blanca','añadido a los admitidos')],
 957:[('añadir la dirección IP a la lista blanca','añadir la dirección IP a los admitidos')],
 963:[('una dirección IP de la lista blanca','una dirección IP admitida')],
 1297:[('IP en lista blanca','IP admitida')],
 1306:[('IP en la lista blanca','IP admitidas')],
 1450:[('En la lista blanca','Admitida')],
 1687:[('a la lista blanca','a los admitidos')],
 1730:[('a la lista blanca','a los admitidos')],
 1948:[('IP en lista blanca','IP admitidas')],
 2016:[('añade una dirección a la lista blanca','añade una dirección a los admitidos')],
 2018:[('o en la lista blanca aquí','o admitida aquí')],
 2239:[('IP en lista blanca','IP admitidas')],
}
changes={}
for n in AUTH:
    cur=fin(n)
    new=cur
    if n in AUTH_SPECIFIC:
        a,b=AUTH_SPECIFIC[n]; new=new.replace(a,b)
    for a,b in AUTH_REPL: new=new.replace(a,b)
    if new!=cur: changes[n]=(new,AUTH_CMT)
for n,reps in WL.items():
    cur=fin(n); new=cur
    for a,b in reps: new=new.replace(a,b)
    if new!=cur: changes[n]=(new,WL_CMT)
    else: print('NO CHANGE for whitelist', n, cur[:80])
for n,(new,cmt) in sorted(changes.items()):
    base=dec.get(n,{})
    row={'n':n,'verdict':'reject','msgstr':new,'comment':cmt}
    if n in dec: dec[n]=row
    else: dec[n]=row; order.append(n)
    if n in ent and n not in ent: print('missing',n)
with open('decisions.jsonl','w') as f:
    for n in order:
        f.write(json.dumps(dec[n],ensure_ascii=False)+'\n')
print('updated', sorted(changes.keys()))
print('unchanged auth (false positives):', [n for n in AUTH if n not in changes])
