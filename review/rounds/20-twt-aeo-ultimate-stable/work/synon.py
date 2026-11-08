import re,sys
sys.path.insert(0,'/Volumes/Datos/repos/wp-es-polyglots/review/rounds/20-twt-aeo-ultimate-stable/work')
from final import final, src, cur, srcs
checks=[
 (r'\bcheck', r'\brevis|\bcompar', 'check -> comprobar'),
 (r'\bnext\b', r'próxim', 'next -> siguiente'),
 (r'\bfix\b', r'soluci', 'fix -> corrección'),
 (r'\bdelete', r'elimin', 'delete -> borrar'),
 (r'\bset\b', r'configur', 'set -> establecer (set up ok)'),
 (r'\bcaption', r'pie de', 'caption -> leyenda'),
 (r'\bhover', r'pasa(r)? el rat', 'hover -> al pasar el cursor'),
 (r'\bFAQ', r'preguntas frecuentes', 'FAQ no traducir'),
 (r'\brole', r'\brol\b', 'role -> perfil'),
 (r'\bmembership', r'afiliaci', 'membership -> membresía'),
 (r'\bmonitor', r'monitoriz', 'monitor -> supervisar'),
 (r'\bauthenticat', r'autentic', 'authentication -> identificación'),
 (r'\bwhitelist', r'permitid', 'whitelist -> lista blanca'),
 (r'\bdefault', r'predeterminad', 'default -> por defecto'),
 (r'\bupload', r'cargar|\bcarga\b', 'upload -> subir'),
 (r'\bsettings?\b', r'\bopciones\b', 'settings -> ajustes'),
 (r'\bcart\b', r'carro|cesta', 'cart -> carrito'),
 (r'\bvariation', r'variante', 'variation -> variación (WooCommerce)'),
 (r'\bhomepage|\bhome page', r'página principal', 'homepage -> página de inicio'),
 (r'\bcategor', r'\bcategorías?\b', None),
 (r'\bdashboard', r'\bpanel\b', 'dashboard (WP) -> escritorio'),
 (r'\bmerchant\b(?! center| api)', r'comerciante|vendedor', 'merchant generic'),
 (r'\bemail\b', r'\bcorreo\b(?! electrónico)', 'correo a secas en textos largos'),
]
for msg_pat, bad_pat, label in checks:
    if not label: continue
    hits=[]
    for n in sorted(final):
        ss=srcs(n)
        if not any(re.search(msg_pat, s, re.I) for s in ss): continue
        for t in cur(n):
            if re.search(bad_pat, t, re.I):
                hits.append((n, ss[0][:80].replace('\n',' '), t[:120].replace('\n',' ')))
    print(f'== {label}: {len(hits)}')
    for h in hits[:12]: print('  ',h)
