"""Second audit: the em dash is not a reason to change a string; Toggle X = «Alternar X»."""
import json
import re
import subprocess
import sys

sys.path.insert(0, '../../../skill/scripts')
import po_tool as p

_, es = p.parse('original.po')
E = {e['n']: e for e in es}
D = [json.loads(l) for l in open('decisions.jsonl', encoding='utf-8') if l.strip()]
edits = {json.loads(l)['n']: json.loads(l) for l in open('edits.jsonl', encoding='utf-8') if l.strip()}
KEEP = {n: edits[n] for n in (202, 2361)}


def text(r):
    return r.get('msgstr') or ' ||| '.join(r.get('msgstr_plural') or [])


def bare(s):
    return re.sub(r'[\s—:;,.()\-]', '', s)


drops = {}
for d in D:
    n = d['n']
    o = text(E[n])
    h = text(edits.get(n, d))
    if bare(o) == bare(h):
        drops[n] = 'Solo cambiaba la puntuación (raya por «:», «;» o paréntesis); no es motivo de cambio.'
for n in (5, 190, 366, 373, 382, 699, 703, 1246, 1581, 1854, 2022, 2869):
    drops.setdefault(n, 'Solo cambiaba el espaciado de la raya.')
drops[560] = 'Se mantiene «preguntas frecuentes» del traductor.'
for n in (310, 481, 594, 678, 915, 925, 1164, 2106, 3073, 499, 1370):
    drops[n] = 'La raya no es motivo de cambio y el resto es una reformulación de algo correcto.'
drops[712] = '«Open Knowledge File» es el nombre de un formato; no se traduce.'
for n in drops:
    edits.pop(n, None)
edits.update(KEEP)

TOGGLE = {
    2038: 'Alternar la negociación Markdown',
    2044: 'Alternar llms.txt',
    2047: 'Alternar Agent Skills Index',
    2086: 'Alternar las migas de pan semánticas',
    2093: 'Alternar la cabecera Vary',
    2101: 'Alternar la API de búsqueda para agentes',
    2115: 'Alternar la integración MCP',
    2120: 'Alternar el límite de solicitudes',
    2130: 'Alternar la lista blanca de IP',
    2134: 'Alternar la verificación de User-Agent',
    2147: 'Alternar el descubrimiento OAuth',
    2181: 'Alternar los metadatos de recurso protegido',
}
for n, s in TOGGLE.items():
    edits[n] = {'n': n, 'msgstr': s, 'reason': '«Toggle» = «alternar»; «activar o desactivar» alarga mucho la etiqueta.'}

with open('edits.jsonl', 'w', encoding='utf-8') as f:
    for e in sorted(edits.values(), key=lambda x: x['n']):
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
args = ['python3', '../../audit_decisions.py', '.', '--edits', 'edits.jsonl'] + [f'{n}={r}' for n, r in sorted(drops.items())]
subprocess.run(args, check=True)
