"""Cheap numbers for a round before any model reviews it (pre-review script).

Usage: python3 review/precheck.py <round-folder>

Prints what decides whether a batch deserves a review or is rejected whole: lint hint
count by kind, strings identical to the source, a source that is not in English,
form of address (tú/usted), Latin American forms, literal translations from English,
and a small random sample.
"""
import collections
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'skill', 'scripts'))
import po_tool as p  # noqa: E402

folder = sys.argv[1]
po = os.path.join(folder, 'original.po')
_, es = p.parse(po)


def tr(e):
    return e.get('msgstr') or ' '.join(e.get('msgstr_plural') or [])


lint = subprocess.run([sys.executable, os.path.join(HERE, '..', 'skill', 'scripts', 'po_tool.py'), 'lint', po],
                      capture_output=True, text=True).stdout
with open(os.path.join(folder, 'lint.txt'), 'w', encoding='utf-8') as f:
    f.write(lint)
kinds = collections.Counter()
for line in lint.splitlines():
    for h in re.sub(r' \[nota: [^\]]*\]', '', line.split(': ', 1)[-1]).split(' | '):
        m = re.match(r'(glossary: [\w -]+? →|glossary term left in English: [\w -]+? →|capitals mid-sentence|non-Spanish quotes|«#%d»|«ej\.»|glossary: [\w -]+? is not translated)', h)
        kinds[m.group(1) if m else h[:40]] += 1
print(f'{len(es)} strings · {len(lint.splitlines())} with lint hints')
print('  ' + ' · '.join(f'{k} {v}' for k, v in kinds.most_common(10)))

same = [e for e in es if tr(e) and tr(e) == (e['msgid'] + (' ' + e['msgid_plural'] if e.get('msgid_plural') else ''))
        or (e.get('msgstr') and e['msgstr'] == e['msgid'])]
print(f'identical to the source: {len(same)}  ' + ', '.join(f'#{e["n"]} {e["msgid"][:25]!r}' for e in same[:12]))

spanish_src = [e for e in es if re.search(r'\b(el|la|los|las|de|que|para|con)\b', e['msgid'])
               and not re.search(r'\b(the|and|to|of|is|your|for|a|an)\b', e['msgid'], re.I)]
print(f'source looks Spanish: {len(spanish_src)}')

your = [e for e in es if re.search(r'\byour\b', e['msgid'], re.I)]
su = sum(1 for e in your if re.search(r'\b[Ss]us?\b', tr(e)))
tu = sum(1 for e in your if re.search(r'\b[Tt]us?\b', tr(e)))
usted = [e for e in es if re.search(r'\b(usted|Por favor,? (?:seleccione|introduzca|ingrese|vuelva|compruebe|espere|intente)|'
                                    r'Busque|Seleccione|Introduzca|Ingrese|Haga clic|Compruebe|Pulse|Elija|Revise|Guarde)\b', tr(e))]
print(f'address: "your" → su {su}, tu {tu} · usted forms in {len(usted)} strings')

latam = [e for e in es if re.search(r'\b(computadora?|celular|ingres[ae]|ingresar|video\b|reporte|carro de compras|órdenes|ordenes|'
                                    r'aplicar los cambios|desplegar|cliquea|clickea|hacer click)', tr(e), re.I)]
print(f'Latin American forms: {len(latam)}  ' + ' | '.join(f'#{e["n"]} {tr(e)[:40]!r}' for e in latam[:4]))

calques = [e for e in es if re.search(r'\b(ha sido|han sido|fue|fueron) \w+(ado|ido|ada|ida)s?\b|\bfalló\b|^Opcionalmente\b', tr(e))]
print(f'passives and calques: {len(calques)}  ' + ' | '.join(f'#{e["n"]} {tr(e)[:40]!r}' for e in calques[:4]))

random.seed(2)
print('sample:')
for e in random.sample(es, min(10, len(es))):
    print(f'  #{e["n"]} {e["msgid"][:70]!r} → {tr(e)[:80]!r}')
