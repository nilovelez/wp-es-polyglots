#!/usr/bin/env python3
"""Build the installable plugin in wordpress-translator-es/ from this repository.

The plugin has one folder per skill in skills/; each SKILL.md is written by hand.
All the skills share references/, which this script regenerates:
  po_tool.py          copy of skill/scripts/po_tool.py
  glossary.csv        resources/glossary.csv (official export; the skill refreshes it with glossary-update)
  glossary-overrides.csv  the team's exceptions, applied by po_tool on top of the glossary
  style-guide.md      resources/quick-reference.md + resources/style-guide.md,
                      without development-only parts (translation memory, internal files)
and writes dist/wordpress-translator-es.zip (ignored by git) with the whole plugin.

Usage: python3 skill/package.py
Run it after every change to resources/ or po_tool.py, and commit the result.
"""
import csv
import io
import os
import re
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'resources')
OUT = os.path.join(ROOT, 'wordpress-translator-es')
warnings = []


def sub(text, old, new, label):
    """Replace a literal piece of text; warn if the source changed and it is gone."""
    if old not in text:
        warnings.append(f'{label}: not found: {old[:60]!r}')
        return text
    return text.replace(old, new)


def drop_section(text, heading, label):
    """Remove a '## heading' section up to the next '## ' heading."""
    m = re.search(rf'^## {re.escape(heading)}.*?(?=^## |\Z)', text, re.M | re.S)
    if not m:
        warnings.append(f'{label}: section not found: {heading!r}')
        return text
    return text[:m.start()] + text[m.end():]


def glossary():
    rows = list(csv.DictReader(open(os.path.join(RES, 'glossary.csv'), encoding='utf-8', newline='')))
    extra = list(csv.DictReader(open(os.path.join(RES, 'glossary-overrides.csv'), encoding='utf-8', newline='')))
    terms = {r['en'].strip().lower() for r in extra}
    rows = [r for r in rows if r['en'].strip().lower() not in terms] + extra
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=['en', 'es', 'pos', 'description'], lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in ['en', 'es', 'pos', 'description']})
    return buf.getvalue(), len(rows)


def style_guide():
    qr = open(os.path.join(RES, 'quick-reference.md'), encoding='utf-8').read()
    sg = open(os.path.join(RES, 'style-guide.md'), encoding='utf-8').read()

    qr = re.sub(r'^Resumen de los criterios.*?\n\n', '', qr, flags=re.S | re.M)
    qr = sub(qr, 'Prioridad si hay conflicto: instrucciones del revisor → glosario → guía.',
             'Prioridad si hay conflicto: instrucciones del usuario → glosario → guía.', 'quick-reference')
    qr = sub(qr, ' Está en `glossary-overrides.csv`, que manda sobre `glossary.csv`.', '', 'quick-reference')
    qr = re.sub(r'^- Fallos habituales de la herramienta:.*\n?', '', qr, flags=re.M)
    qr = qr.replace('# Referencia rápida de criterios es_ES', '## Referencia rápida', 1)
    # Demote the quick reference's own sections one level, below «Referencia rápida».
    qr = re.sub(r'^## (?!Referencia rápida)', '### ', qr, flags=re.M)

    sg = drop_section(sg, '8. Memoria de traducción', 'style-guide')
    sg = sub(sg, '4. **Memoria de traducción** (`resources/translation-memory.csv`): referencia de consistencia para frases completas.\n',
             '', 'style-guide')
    sg = sub(sg, '2. Antes de cada cadena, consulta el glosario y la memoria de traducción (coincidencias exactas y parecidas).',
             '2. Antes de cada cadena, consulta el glosario.', 'style-guide')
    sg = sub(sg, '6. Si una respuesta establece un criterio general, añádelo a las reglas o a la memoria de traducción.\n',
             '', 'style-guide')
    sg = sub(sg, ', es claramente poco natural o inconsistente con la memoria de traducción',
             ' o es claramente poco natural', 'style-guide')
    sg = sub(sg, ' Contrasta con la memoria de traducción y con las traducciones ya aprobadas del proyecto, si están disponibles.',
             '', 'style-guide')

    head, _, body = sg.partition('\n---\n')
    return f'{head}\n---\n\n{qr.strip()}\n\n---\n{body}'


def zip_dir(src, zpath, top):
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(src):
            for f in files:
                if f.endswith('.pyc') or f == '.DS_Store':
                    continue
                full = os.path.join(base, f)
                z.write(full, os.path.join(top, os.path.relpath(full, src)))


def main():
    # One shared folder for all the skills of the package.
    refs = os.path.join(OUT, 'references')
    os.makedirs(refs, exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'skill', 'scripts', 'po_tool.py'), os.path.join(refs, 'po_tool.py'))
    for f in ('glossary.csv', 'glossary-overrides.csv'):
        shutil.copy(os.path.join(RES, f), os.path.join(refs, f))
    open(os.path.join(refs, 'style-guide.md'), 'w', encoding='utf-8').write(style_guide())
    _, n = glossary()
    skills = sorted(d for d in os.listdir(os.path.join(OUT, 'skills'))
                    if os.path.exists(os.path.join(OUT, 'skills', d, 'SKILL.md')))
    dist = os.path.join(ROOT, 'dist')
    os.makedirs(dist, exist_ok=True)
    zpath = os.path.join(dist, 'wordpress-translator-es.zip')
    zip_dir(OUT, zpath, 'wordpress-translator-es')
    print(f'{OUT}: {len(skills)} skills ({", ".join(skills)}); glossary {n} rows; zip {zpath}')
    for w in warnings:
        print('WARNING', w)
    sys.exit(1 if warnings else 0)


if __name__ == '__main__':
    main()
