#!/usr/bin/env python3
"""Build the two installable plugins from this repository.

wordpress-translator-es/  base skills translate and review: a .po in, a .po out. Each skill
                          folder is self-contained; this script writes its references/:
  po_tool.py          copy of skill/scripts/po_tool.py (file plumbing only)
  glossary.md         resources/glossary.csv with resources/glossary-overrides.csv merged
                      in, in Markdown: the model reads it whole
  style-guide.md      resources/style-guide.md, resources/guide-exceptions.md (when it has
                      rules) and resources/agent-appendix.md, concatenated; links removed
wordpress-polyglots-es/   GlotPress workflow for moderators, on top of the base skills. Each
                          skill folder gets scripts/: glotpress.py, po_tool.py and the merged
                          glossary.csv (for the precheck).
SKILL.md files are written by hand. dist/ (ignored by git) gets one zip per plugin and, for
claude.ai, one zip per base skill.

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
WORKFLOW = os.path.join(ROOT, 'wordpress-polyglots-es')
warnings = []


def sub(text, old, new, label):
    """Replace a literal piece of text; warn if the source changed and it is gone."""
    if old not in text:
        warnings.append(f'{label}: not found: {old[:60]!r}')
        return text
    return text.replace(old, new)


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


def glossary_md(merged):
    """The whole glossary as Markdown, one line per entry, sorted by term."""
    rows = sorted(csv.DictReader(io.StringIO(merged)), key=lambda r: (r['en'].strip().lower(), r.get('pos', '')))
    out = ['# Glosario es_ES', '',
           'Obligatorio. Formato: término inglés (categoría) → traducción — nota. Las notas también son obligatorias.', '']
    for r in rows:
        if not r['en'].strip():
            continue
        pos = f" ({r['pos'].strip()})" if (r.get('pos') or '').strip() else ''
        desc = ' '.join((r.get('description') or '').split())
        out.append(f"- {r['en'].strip()}{pos} → {r['es'].strip()}" + (f' — {desc}' if desc else ''))
    return '\n'.join(out) + '\n'


def style_guide():
    """The agents' guide: the guide, then the exceptions (when there are any), then the agent
    appendix, concatenated as they are. Only the links are removed."""
    read = lambda f: open(os.path.join(RES, f), encoding='utf-8').read().strip()
    parts = [read('style-guide.md')]
    exceptions = read('guide-exceptions.md')
    if re.search(r'^\s*- ', exceptions, re.M):
        parts.append(exceptions)
    parts.append(read('agent-appendix.md'))
    text = '\n\n---\n\n'.join(p.rstrip().rstrip('-').rstrip() for p in parts) + '\n'
    text = strip_links(text)
    return re.sub(r'\n{3,}', '\n\n', text)


def strip_links(text):
    """The agents' guide has no links, so the model does not try to fetch or browse them.
    A link whose text is an address goes away with its parentheses; any other keeps its text."""
    text = re.sub(r' ?\(\[[^\]]*\.[a-z]{2,}/[^\]]*\]\([^)]*\)\)', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    if re.search(r'https?://|www\.', text):
        warnings.append('style-guide: an address is left in the agents\' guide')
    return text


def zip_dir(src, zpath, top):
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(src):
            for f in files:
                if f.endswith('.pyc') or f == '.DS_Store':
                    continue
                full = os.path.join(base, f)
                z.write(full, os.path.join(top, os.path.relpath(full, src)))


def main():
    scripts = os.path.join(ROOT, 'skill', 'scripts')
    merged, n = glossary()
    guide = style_guide()
    dist = os.path.join(ROOT, 'dist')
    os.makedirs(dist, exist_ok=True)
    # Base skills: each one self-contained, the same folder for Claude Code and claude.ai.
    for s in ('translate', 'review'):
        refs = os.path.join(OUT, 'skills', s, 'references')
        shutil.rmtree(refs, ignore_errors=True)
        os.makedirs(refs)
        shutil.copy(os.path.join(scripts, 'po_tool.py'), refs)
        open(os.path.join(refs, 'glossary.md'), 'w', encoding='utf-8').write(glossary_md(merged))
        open(os.path.join(refs, 'style-guide.md'), 'w', encoding='utf-8').write(guide)
    # Workflow skills: the GlotPress script, the plumbing it imports and the glossary for the precheck.
    wf = sorted(d for d in os.listdir(os.path.join(WORKFLOW, 'skills'))
                if os.path.exists(os.path.join(WORKFLOW, 'skills', d, 'SKILL.md')))
    for s in wf:
        sc = os.path.join(WORKFLOW, 'skills', s, 'scripts')
        shutil.rmtree(sc, ignore_errors=True)
        os.makedirs(sc)
        for f in ('glotpress.py', 'po_tool.py'):
            shutil.copy(os.path.join(scripts, f), sc)
        open(os.path.join(sc, 'glossary.csv'), 'w', encoding='utf-8', newline='').write(merged)
    for plugin in (OUT, WORKFLOW):
        name = os.path.basename(plugin)
        zpath = os.path.join(dist, name + '.zip')
        zip_dir(plugin, zpath, name)
        print(f'{zpath}')
    print(f'glossary {n} rows; workflow skills: {", ".join(wf)}')
    # claude.ai takes one skill per zip: the base skill folders, renamed.
    for s in ('translate', 'review'):
        name = f'wordpress-{s}-es'
        tmp = os.path.join(dist, 'claude-ai', name)
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.copytree(os.path.join(OUT, 'skills', s), tmp, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        md = open(os.path.join(tmp, 'SKILL.md'), encoding='utf-8').read()
        md = sub(md, f'name: {s}\n', f'name: {name}\n', f'claude.ai {s}')
        open(os.path.join(tmp, 'SKILL.md'), 'w', encoding='utf-8').write(md)
        zip_dir(tmp, tmp + '.zip', name)
        shutil.rmtree(tmp)
        print(f'claude.ai: {tmp}.zip')
    for w in warnings:
        print('WARNING', w)
    sys.exit(1 if warnings else 0)


if __name__ == '__main__':
    main()
