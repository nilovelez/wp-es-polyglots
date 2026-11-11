#!/usr/bin/env python3
"""Build the installable plugin in wordpress-translator-es/ from this repository.

The plugin has one folder per skill in skills/; each SKILL.md is written by hand.
All the skills share references/, which this script regenerates:
  po_tool.py          copy of skill/scripts/po_tool.py
  glossary.csv        resources/glossary.csv with resources/glossary-overrides.csv merged in:
                      the skill sees one glossary
  style-guide.md      resources/style-guide.md with resources/quick-reference.md merged in:
                      the skill sees one guide, without workflow, pending notes or file names
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
        r = dict(r)
        # The overrides say where they come from; the skill sees one glossary, without that.
        r['description'] = re.sub(r'^Decisión del equipo es_ES(, en lugar de [^.]*?\))?\.\s*', '',
                                  r.get('description') or '')
        w.writerow({k: r.get(k, '') for k in ['en', 'es', 'pos', 'description']})
    return buf.getvalue(), len(rows)


def sections(text):
    """Split a Markdown text into (head, {'## title': body})."""
    parts = re.split(r'^(## .*)$', text, flags=re.M)
    return parts[0], {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def style_guide():
    """One guide for the skill: the team's guide with our criteria merged into it.
    No quick reference apart, no workflow (that is the skill's job), no pending notes,
    no mention of files or of how it was put together."""
    qr = open(os.path.join(RES, 'quick-reference.md'), encoding='utf-8').read()
    sg = open(os.path.join(RES, 'style-guide.md'), encoding='utf-8').read()
    _, q = sections(qr)
    when = q.get('## Cuándo cambiar una cadena (revisión)')
    crit = q.get('## Criterios de traducción')
    if when is None or crit is None:
        warnings.append('quick-reference: sections not found')
        when, crit = when or '', crit or ''
    crit = sub(crit, ', aunque el glosario oficial diga que no se traducen. Está en `glossary-overrides.csv`, que manda sobre `glossary.csv`.',
               '.', 'quick-reference')
    crit = re.sub(r'^- Fallos habituales de la herramienta:.*\n?', '', crit, flags=re.M)
    consensus = re.search(r'^El glosario, la guía de estilo y estos criterios.*$', qr, flags=re.M)
    consensus = consensus.group(0).replace('El glosario, la guía de estilo y estos criterios', 'El glosario y esta guía') if consensus else ''

    head, s = sections(sg)
    keys = list(s)
    def get(prefix):
        for k in keys:
            if k.startswith(prefix):
                return k
        warnings.append(f'style-guide: section not found: {prefix!r}')
        return None
    out = [head.rstrip().replace(' para agentes', '') + '\n']
    for k in keys:
        body = s[k]
        if k.startswith('## 1.'):
            body = sub(body, '**Instrucciones explícitas del revisor humano** en la sesión de trabajo',
                       '**Instrucciones explícitas del usuario**', 'style-guide 1')
            body = sub(body, '**Glosario oficial** (`glossary.csv`, exportado de [translate.wordpress.org/locale/es/default/glossary](https://translate.wordpress.org/locale/es/default/glossary/)).',
                       '**Glosario** (`glossary.csv`).', 'style-guide 1')
            body = sub(body, '4. **Memoria de traducción** (`resources/translation-memory.csv`): referencia de consistencia para frases completas.\n',
                       '', 'style-guide 1')
            body = sub(body, ' (ver sección 9), aplica el criterio correcto y señálalo en el informe.',
                       ', aplícala igualmente y señálalo al terminar.', 'style-guide 1')
            body = body.rstrip().rstrip('-').rstrip() + f'\n\n{consensus}\n\n---\n\n'
        elif k.startswith('## 2.'):
            body = sub(body, 'anótalo como duda en el informe', 'márcalo como duda', 'style-guide 2')
            body = body.rstrip().rstrip('-').rstrip() + '\n\n### Casos concretos\n' + crit.rstrip() + '\n\n---\n\n'
        elif k.startswith('## 6.') or k.startswith('## 8.') or k.startswith('## 9.'):
            continue
        elif k.startswith('## 7.'):
            k = '## 6. Revisión'
            body = sub(body, ', es claramente poco natural o inconsistente con la memoria de traducción',
                       ' o es claramente poco natural', 'style-guide 7')
            body = sub(body, '**Dudosa**: se pregunta al revisor al terminar',
                       '**Dudosa**: mejor propuesta y una pregunta concreta', 'style-guide 7')
            body = sub(body, ' Contrasta con la memoria de traducción y con las traducciones ya aprobadas del proyecto, si están disponibles.',
                       ' Las traducciones ya aprobadas no son referencia: aprobada no quiere decir correcta.', 'style-guide 7')
            body = re.sub(r'^\*\*Salida:\*\*.*\n?', '', body, flags=re.M)
            body = body.rstrip().rstrip('-').rstrip() + '\n\n### Cuándo cambiar una cadena\n' + when.rstrip() + '\n\n'
        out.append(k + '\n' + body)
    text = '\n'.join(out).rstrip() + '\n'
    return re.sub(r'\n{3,}', '\n\n', text)


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
    merged, n = glossary()
    open(os.path.join(refs, 'glossary.csv'), 'w', encoding='utf-8', newline='').write(merged)
    stale = os.path.join(refs, 'glossary-overrides.csv')
    if os.path.exists(stale):
        os.remove(stale)
    open(os.path.join(refs, 'style-guide.md'), 'w', encoding='utf-8').write(style_guide())
    skills = sorted(d for d in os.listdir(os.path.join(OUT, 'skills'))
                    if os.path.exists(os.path.join(OUT, 'skills', d, 'SKILL.md')))
    dist = os.path.join(ROOT, 'dist')
    os.makedirs(dist, exist_ok=True)
    zpath = os.path.join(dist, 'wordpress-translator-es.zip')
    zip_dir(OUT, zpath, 'wordpress-translator-es')
    print(f'{OUT}: {len(skills)} skills ({", ".join(skills)}); glossary {n} rows; zip {zpath}')
    # claude.ai takes one skill per ZIP and has no shared folder: build the two base skills
    # self-contained, with references/ inside each one.
    for s in ('translate', 'review'):
        name = f'wordpress-{s}-es'
        tmp = os.path.join(dist, 'claude-ai', name)
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.copytree(os.path.join(OUT, 'skills', s), tmp)
        shutil.copytree(refs, os.path.join(tmp, 'references'), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        md = open(os.path.join(tmp, 'SKILL.md'), encoding='utf-8').read()
        md = sub(md, f'name: {s}\n', f'name: {name}\n', f'claude.ai {s}')
        md = sub(md, "`<refs>` is the package's shared folder, `<skill>/../../references`",
                 "`<refs>` is `<skill>/references`", f'claude.ai {s}')
        md = md.replace(', used by all the skills of the package)', ')')
        open(os.path.join(tmp, 'SKILL.md'), 'w', encoding='utf-8').write(md)
        zip_dir(tmp, tmp + '.zip', name)
        shutil.rmtree(tmp)
        print(f'claude.ai: {tmp}.zip')
    for w in warnings:
        print('WARNING', w)
    sys.exit(1 if warnings else 0)


if __name__ == '__main__':
    main()
