import json
import re
import sys

BASE = '/Volumes/Datos/repos/wp-es-polyglots/review/rounds/21-gratora-donation-platform-stable/work/final.jsonl'

PATTERNS = {
    'proximo': r'[Pp]róxim',
    'siguiente': r'[Ss]iguiente',
    'vincul': r'[Vv]incul',
    'notificacion': r'[Nn]otific',
    'autentic': r'[Aa]utentic|[Aa]utentif',
    'administracion': r'[Aa]dministraci',
    'entrada': r'[Ee]ntrada',
    'online': r'[Oo]nline',
    'predeterminado': r'[Pp]redeterminad',
    'sitio_web': r'[Ss]itio web',
    'vosotros': r'\b(podéis|tenéis|sois|vuestr\w*|queréis|sabéis|hacéis|debéis|ponéis|usáis)\b',
    'lo_sentimos': r'[Ll]o sentimos',
    'programacion': r'[Pp]rogramaci',
    'defin_imperativo': r'\b(Defin(e|id|ir)|defin(e|as|ir)|Defin(e)?)\b',
    'correo_suelto': r'\bcorreos?\b(?! electr)',
    'interruptor': r'[Ii]nterruptor',
    'conmutador': r'[Cc]onmutador',
    'establec': r'[Ee]stablec|[Ee]stablece',
    'alternar': r'[Aa]lternar',
    'asignar': r'[Aa]signar|[Aa]signa\b',
    'asociar': r'[Aa]socia',
    'cuota': r'[Cc]uota',
    'comision': r'[Cc]omisi',
    'pasarela': r'[Pp]asarela',
    'calendario': r'[Cc]alendario',
    'recurrente': r'[Rr]ecurrente',
    'periodico': r'[Pp]eriódic',
    'valoracion': r'[Vv]aloraci|[Rr]eseña',
    'sandbox': r'[Ss]andbox',
    'feed': r'\b[Ff]eed\b|[Ll]istado',
    'hero': r'[Cc]abecera destacada|[Ss]ección destacada|[Hh]ero',
    'atrevido': r'Atrevido|Negrita',
    'campeon': r'Campe[oó]n|Impulsor',
    'escritorio': r'[Ee]scritorio|[Pp]anel',
    'lienzo': r'[Ll]ienzo|[Cc]anvas',
    'tuteo_usted': r'\b(usted|ustedes)\b',
    'predeterminado2': r'[Pp]redeterminad',
    'por_defecto': r'por defecto',
    'registro': r'[Rr]egistr',
    'desglose': r'[Dd]esglose',
    'ajustes': r'[Aa]justes',
    'configuracion': r'[Cc]onfiguraci',
}

rows = [json.loads(l) for l in open(BASE, encoding='utf-8')]

def text_of(e):
    if 'msgstr' in e:
        return e['msgstr']
    return ' || '.join(e.get('msgstr_plural', []))

want = sys.argv[1:] if len(sys.argv) > 1 else list(PATTERNS)
for name in want:
    rx = re.compile(PATTERNS[name])
    hits = [(e['n'], e['msgid'][:70].replace('\n', ' '), text_of(e)[:140].replace('\n', ' ')) for e in rows if rx.search(text_of(e))]
    print(f'## {name}: {len(hits)}')
    for n, s, t in hits[:60]:
        print(f'  {n} | S: {s} | T: {t}')
