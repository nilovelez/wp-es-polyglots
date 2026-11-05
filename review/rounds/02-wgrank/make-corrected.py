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
def key(s):
    ks=[k for k in om if k.startswith(s)]
    assert len(ks)==1,(s,len(ks))
    return ks[0]

full={
 'WGRank Translate – Fast &amp; Indexable':'WGRank Translate – Traducción multilingüe rápida e indexable',
 '<strong>R-Z:':'<strong>R-Z:</strong> Rumano, ruso, samoano, gaélico escocés, serbio, sesotho, shona, sindhi, cingalés, eslovaco, esloveno, somalí, español, sundanés, suajili, sueco, tayiko, tamil, telugu, tailandés, turco, ucraniano, urdu, uzbeko, vietnamita, galés, xhosa, yidis, yoruba, zulú.',
 '<strong>L-P:':'<strong>L-P:</strong> Lao, latín, letón, lituano, luxemburgués, macedonio, malgache, malayo, malayalam, maltés, maorí, maratí, mongol, Myanmar (birmano), nepalí, noruego, pastún, persa, polaco, portugués, panyabí.',
 '<strong>F-K:':'<strong>F-K:</strong> Filipino, finés, francés, frisón, gallego, georgiano, alemán, griego, guyaratí, criollo haitiano, hausa, hawaiano, hebreo, hindi, hmong, húngaro, islandés, igbo, indonesio, irlandés, italiano, japonés, javanés, canarés, kazajo, jemer, coreano, kurdo (kurmanji), kirguís.',
 '<strong>A-E:':'<strong>A-E:</strong> Afrikáans, albanés, amárico, árabe, armenio, azerbaiyano, vasco, bielorruso, bengalí, bosnio, búlgaro, catalán, cebuano, chichewa, chino (simplificado), chino (tradicional), corso, croata, checo, danés, holandés, inglés, esperanto, estonio.',
 'WGRank Translate supports 103+':'WGRank Translate es compatible con más de 103 idiomas, lo que te permite llegar a una audiencia verdaderamente global. Nuestros idiomas compatibles incluyen:',
 'Is it SEO friendly?':'¿Está optimizado para SEO?',
 '<strong>Auto-Sitemap Generation:':'<strong>Generación automática de mapas del sitio:</strong> Ganchos completos de <code>wp-sitemap</code> específicos por idioma creados de forma nativa para una indexación eficiente en Google.',
 '<strong>Full DOM Interception:':'<strong>Interceptación completa del DOM:</strong> Captura todo, desde la cabecera hasta el pie de página, garantizando una experiencia coherente de plugin de idiomas para WordPress.',
 'Advanced settings panel':'Panel de ajustes avanzados para vaciar la caché, eliminar mapas del sitio y activar el registro de depuración.',
 'Tweak: Renamed':'Retoque: Se renombró la pestaña «Caché» a «Traducciones» en la interfaz de administración de WP para mayor claridad.',
 'Enhancement: Expanded language support':'Mejora: Soporte de idiomas ampliado a 104 idiomas nativos, incluyendo localización completa de los menús y las cadenas de la administración.',
 'Feature: Added Word Limit Tracking':'Característica: Se añadió seguimiento del límite de palabras y un aviso visualmente mejorado en el escritorio para usuarios del plan gratuito.',
 'Added native localized SEO sitemap':'Se añadió indexación nativa de mapas del sitio SEO localizados.',
}
rep={
 'Yes! WGRank Translate includes a generous':[('Plan Gratuito','plan gratuito'),('monitorizar','supervisar'),('desde el panel del plugin','desde el escritorio del plugin'),('puedes actualizar fácilmente','puedes mejorar fácilmente')],
 'No! WGRank Translate is completely':[(r'\"Plug &amp; Play\"','«Plug &amp; Play»'),('Nube de Traducción con IA','nube de traducción con IA')],
 '<strong>Language Selection:':[("'Seleccionar todo' o 'Deseleccionar todo'",'«Seleccionar todo» o «Anular toda la selección»')],
 '<strong>Language Switcher:':[('(ej. Bandera + Nombre)','(p. ej., bandera + nombre)')],
 'Storing content in a pre-compressed':[('Tiempo hasta el Primer Byte','tiempo hasta el primer byte')],
 'WGRank helps you reach':[('los rankings de búsqueda y el compromiso de los visitantes','el posicionamiento en las búsquedas y la participación de los visitantes')],
 'Yes, WGRank is 100% compatible':[('plugins de formularios y sliders','plugins de formularios y carruseles')],
 'Yes. It translates JSON-LD':[('fragmentos enriquecidos (rich snippets) multilingües','snippets enriquecidos multilingües')],
 'No. Our ':[(r'\"Anti-Flash\"','«Anti-Flash»')],
 'Head to <a href':[('Sitio Oficial de WGRank','sitio oficial de WGRank')],
 '<strong>Content Shielding:':[(r'\"Anti-Flash\"','«Anti-Flash»')],
 'This plugin connects to external':[('API en la Nube de WGRank','API en la nube de WGRank')],
 '<strong>103+ Languages Supported:':[('Más de 103 idiomas admitidos','Más de 103 idiomas compatibles')],
 '<strong>Native Names:':[('(ej. ','(p. ej., ')],
 '<strong>Multiple Styles:':[('Visualización como Bandera + Nombre, Solo bandera o Solo nombre','Visualización como bandera + nombre, solo bandera o solo nombre')],
 '<strong>Secure Checkout:':[('Checkout seguro','Pago seguro')],
 '<strong>Cloudflare Ready:':[('firewalls de aplicaciones web','cortafuegos de aplicaciones web')],
 '<strong>Auto-Sitemaps:':[('Sitemaps automáticos','Mapas del sitio automáticos')],
 '<strong>SEO Metadata &amp; Schema:':[('Metadados SEO','Metadatos SEO'),('meta descripciones','meta descriptions'),('fragmentos enriquecidos','snippets enriquecidos')],
 'Tweak: Sitemap file naming':[('Ajuste:','Retoque:'),('archivos de sitemap','archivos del mapa del sitio')],
 'Tweak: Minor performance':[('Ajuste:','Retoque:')],
 'Feature: Added Translation Exclusions':[('ajuste de Exclusiones de traducción','ajuste de exclusiones de traducción')],
 'Hotfix: Fixed fresh-install':[('en el frontend','en la parte pública')],
 'Hotfix: Fixed an issue where the JavaScript':[('en el frontend','en la parte pública')],
 'Hotfix: Resolved a fatal error':[('selector del frontend','selector de la parte pública')],
 'Resolved Plugin Directory':[('Directorio de Plugins','Directorio de plugins')],
}
revert=['Patched caching','AI Website Translation &amp; Core','<strong>Zero PHP Processing']
target={}
for k,v in full.items(): target[key(k)]=v
for k,lst in rep.items():
    kk=key(k); s=om[kk]['str']
    for a,b in lst:
        assert a in s,(k,a)
        s=s.replace(a,b)
    target[kk]=s
for k in revert: target[key(k)]=om[key(k)]['str']

hdr=open(O,encoding='utf8').read().split('\n\n')[0]
out=[hdr,''];n=0
for e in o:
    if not e['id']: continue
    t=target.get(e['id'],rm.get(e['id'],e['str']))
    if t==e['str']: continue
    n+=1
    for c in e['c']: out.append(c)
    out.append('msgid ""');out.append('"'+e['id']+'"');out.append('msgstr ""');out.append('"'+t+'"');out.append('')
    print('-',e['id'][:70].replace('\n',' '))
p=d+'corrected.po'
open(p,'w',encoding='utf8').write('\n'.join(out))
print(n,'cambios de',len([e for e in o if e['id']]))
bad=0
for e in o:
    if not e['id']: continue
    t=target.get(e['id'],rm.get(e['id'],e['str']))
    for pat in (r'<[^>]+>',r'%\d?\$?[sd]|%i',r'&\w+;',r'\{[^}]+\}',r'https?://[^\s"\\<]+',r'\\n'):
        if sorted(re.findall(pat,e['id']))!=sorted(re.findall(pat,t)): bad+=1;print('MISMATCH',pat,e['id'][:50])
print('mismatches',bad)
