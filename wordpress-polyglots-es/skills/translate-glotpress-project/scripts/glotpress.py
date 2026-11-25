#!/usr/bin/env python3
"""GlotPress workflow for es_ES moderators (stdlib only): everything around the
translate and review skills. It never uploads or approves anything.

Commands:
  prepare <project URL> [--translate] [--window N] [--force]
      Download the waiting strings (or, with --translate, the untranslated ones)
      into <name>.po in the current folder. Review: run the precheck and STOP if
      the batch looks like one to reject whole (--force goes on anyway). Over
      MAX_PART strings, or if it does not fit in one session, split it into
      <name>-partK.po files, one subagent each. Prints which skill to use on
      which file, and the import URL.
  merge <name> [--translate]
      Join the files the skill gave for each <name>-partK.po into one
      <name>-corrected.po (or <name>-es_ES.po) and check it with msgfmt.
  fetch <project url> [folder] [--untranslated]
      Download the waiting (or untranslated) strings into <folder>/original.po.
  precheck <file.po> [--window N]
      Cheap numbers before a review: lint hints by kind, strings identical to
      the source, form of address, glossary alternatives pasted whole, Latin
      American forms, calques, a sample and the size line. Marks FORMAL
      REGISTER THROUGHOUT and SEARCH AND REPLACE WITHOUT CARE.
  size <file.po> [--translate] [--window N]
      Worst-case peak context of the whole file in one session; entry ranges
      if it does not fit.
  lint <file.po> [glossary.csv]
      Hints on current translations, counted by the precheck: glossary terms
      missing or left in English, capitals mid-sentence, «ej.», quotes, length.
  --range A-B (lint): only entries A to B.
"""
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import po_tool  # noqa: E402  (next to this script)
from po_tool import (parse, parse_sel, TAG, length_off, write_entry, cmd_extract, _py,  # noqa: E402
                     _capture)

# Workflow plugin: glossary.csv sits next to this script. Development repository: resources/.
RES = (os.path.join(_HERE, '') if os.path.exists(os.path.join(_HERE, 'glossary.csv'))
       else os.path.join(_HERE, '..', '..', 'resources', ''))
RANGE = None


def read_csv(path):
    import csv
    return list(csv.DictReader(open(path, encoding='utf-8', newline='')))


def read_glossary(gl):
    """Glossary rows. With the default glossary, the team's overrides
    (resources/glossary-overrides.csv) replace every row of the same term."""
    rows = read_csv(gl)
    ov = RES + 'glossary-overrides.csv'
    if os.path.abspath(gl) == os.path.abspath(RES + 'glossary.csv') and os.path.exists(ov):
        extra = read_csv(ov)
        terms = {r['en'].strip().lower() for r in extra}
        rows = [r for r in rows if r['en'].strip().lower() not in terms] + extra
    return rows


def norm(s):
    import unicodedata
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')


def stem_in(option, text):
    """True if every word of a glossary option appears (by a short stem) in text."""
    words = [w for w in re.findall(r'\w+', norm(option)) if len(w) > 2]
    if not words:
        return True
    return all(re.search(r'\b' + re.escape(w[:max(4, len(w) - 3)]), text) for w in words)


def cmd_lint(args):
    """Hints for review: glossary terms whose translation is missing or left in
    English, mid-sentence capitals, «ej.», straight quotes. Hints, not verdicts."""
    po, gl = args[0], (args[1] if len(args) > 1 else RES + 'glossary.csv')
    entries = parse_sel(po)
    merged = {}
    for row in read_glossary(gl):
        en = row['en'].strip()
        es = row['es'].strip()
        desc = norm(row.get('description', ''))
        if not en or not es or len(en) < 3:
            continue
        m = merged.setdefault(en.lower(), {'en': en, 'es': [], 'opts': [], 'keep': False, 'notes': []})
        m['keep'] |= 'no se traduce' in desc or norm(en) == norm(es)
        if es not in m['es']:
            m['es'].append(es)
        note = ' '.join(row.get('description', '').split())
        if note and note not in m['notes']:
            m['notes'].append(note)
        m['opts'] += [o.strip() for o in re.split(r'\s*/\s*', es) if o.strip()]
    rows = [(m['en'], ' | '.join(m['es']), m['opts'], m['keep'],
             (' [nota: ' + ' / '.join(m['notes']) + ']') if m['notes'] else '') for m in merged.values()]
    code = re.compile(r'<code>.*?</code>|https?://\S+', re.S)
    for e in entries:
        src = e['msgid'] + ' ' + (e['msgid_plural'] or '')
        tr = e['msgstr'] if e['msgid_plural'] is None else ' '.join(e['msgstr_plural'])
        if not tr.strip():
            continue
        s_plain, t_plain = TAG.sub(' ', code.sub(' ', src)), TAG.sub(' ', code.sub(' ', tr))
        s_low, t_norm = s_plain.lower(), norm(t_plain)
        hints = []
        for en, es, opts, keep, note in rows:
            rx = r'(?<![\w-])' + re.escape(en.lower()) + r'(?:s|es|ed|d|ing)?(?![\w-])'
            # A match that is itself another glossary term (fee + d = feed) is that term, not this one.
            if not any(m.group(0) not in merged or m.group(0) == en.lower() for m in re.finditer(rx, s_low)):
                continue
            if keep:
                if not re.search(rx, t_plain.lower()):
                    hints.append(f'glossary: {en} is not translated ({es}){note}')
                continue
            if re.search(rx, t_plain.lower()):
                hints.append(f'glossary term left in English: {en} → {es}{note}')
            elif not any(stem_in(o, t_norm) for o in opts):
                hints.append(f'glossary: {en} → {es}?{note}')
        # Capitalized words mid-sentence that are not in the source (Title Case).
        caps = []
        for m in re.finditer(r'(?<=[^\s.:!?¡¿*>«(\-–—])\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñü]+)', t_plain):
            w = m.group(1)
            if w not in s_plain and w not in caps:
                caps.append(w)
        if caps:
            hints.append('capitals mid-sentence: ' + ', '.join(caps))
        if '#%' in src and re.search(r'n\.\s?º\s?%', tr):
            hints.append('«#%d» → keep «#», not «n.º»')
        if re.search(r'(?<!p\. )\bej\.', tr):
            hints.append('«ej.» → «p. ej.»')
        visible = TAG.sub('', tr)
        if re.search(r'(?<![=\w])"[^"<>=]+"(?![\w>])', visible) or re.search(r"(?<![\w=])'[^'<>]+'(?!\w)", visible) or re.search(r'[“”‘’]', visible):
            hints.append('non-Spanish quotes')
        pairs = [(e['msgid'], e['msgstr'])] if e['msgid_plural'] is None else \
            list(zip([e['msgid'], e['msgid_plural']], e['msgstr_plural']))
        for s, t in pairs:
            r = length_off(s, t)
            if r is not None:
                hints.append(f'length: translation {r:.1f} times the source (GlotPress flags over 5 or under 0.2)')
                break
        if hints:
            print(f'#{e["n"]}: ' + ' | '.join(hints))


def cmd_fetch(args):
    """Download strings of a translate.wordpress.org project (no login needed)."""
    import urllib.parse
    import urllib.request
    status = 'untranslated' if '--untranslated' in args else 'waiting'
    pos = [a for a in args if not a.startswith('--')]
    url = pos[0].split('?')[0].rstrip('/') + '/'
    m = re.match(r'https://translate\.wordpress\.org/projects/(.+?)/$', url)
    if not m:
        sys.exit('Not a translate.wordpress.org project URL')
    path = m.group(1)
    if not re.search(r'/[a-z]{2,3}(?:-[a-z]+)?/default$', path):
        path += '/es/default'
    base = f'https://translate.wordpress.org/projects/{path}/'
    folder = pos[1] if len(pos) > 1 else '.'
    os.makedirs(folder, exist_ok=True)
    q = urllib.parse.urlencode({'filters[status]': status, 'format': 'po'})
    req = urllib.request.Request(f'{base}export-translations/?{q}',
                                 headers={'User-Agent': 'wordpress-translator-es skill'})
    data = urllib.request.urlopen(req, timeout=60).read()
    out = os.path.join(folder, 'original.po')
    open(out, 'wb').write(data)
    count = data.decode('utf-8', 'replace').count('\nmsgid ') - 1
    print(f'{out}: {count} {status} strings')


def size_estimate(po, translate=False, window=1_000_000):
    """Worst-case peak context of doing the whole file in one session, and how to split it
    if it does not fit. Measured on Haiku sessions (rounds 38-48): peak context
    ~ 55,000 + 0.46 x bytes of entries.jsonl + 1.07 x bytes of decisions written (the base
    is what an isolated session holds before the first block: system, skill, guide,
    glossary; the per-byte numbers fall short on round 46, so they are not lowered). The
    decisions are not known in advance: a review assumes a bad batch (decisions = 60% of
    the entries' bytes, the worst measured); a translation writes every string (120%).
    One session may use 85% of the window."""
    import math
    _, entries = parse(po)
    entries = [e for e in entries if not RANGE or RANGE[0] <= e['n'] <= RANGE[1]]
    sizes = []
    for e in entries:
        o = {'n': e['n'], 'ctx': e['ctx'], 'msgid': e['msgid'], 'msgid_plural': e['msgid_plural'],
             'msgstr': e['msgstr'], 'msgstr_plural': e['msgstr_plural']}
        sizes.append(len(json.dumps(o, ensure_ascii=False).encode('utf-8')) + 1)
    base, per_byte = 55_000, 0.46 + 1.07 * (1.2 if translate else 0.6)
    peak = base + per_byte * sum(sizes)
    limit = 0.85 * window
    if peak <= limit:
        return peak, limit, None
    # As few parts as fit, of equal bytes (long strings fill the context faster than short ones).
    budget = (limit - base) / per_byte
    target = sum(sizes) / math.ceil(sum(sizes) / budget)
    parts, acc, start = [], 0, entries[0]['n']
    for e, s in zip(entries, sizes):
        if acc + s > target * 1.001 and acc:
            parts.append((start, prev))
            start, acc = e['n'], 0
        acc += s
        prev = e['n']
    parts.append((start, prev))
    return peak, limit, parts


def cmd_size(args):
    """Does the review (or with --translate, the translation) of the file fit in one
    session? --window N: the model's context window in tokens (default 1,000,000)."""
    translate = '--translate' in args
    window = 1_000_000
    if '--window' in args:
        window = int(args[args.index('--window') + 1])
    peak, limit, parts = size_estimate(args[0], translate, window)
    if parts is None:
        print(f'size: about {peak / 1000:.0f}k tokens at most of a {window / 1000:.0f}k window: '
              f'fits in one session. Do it all in this session; do not split it.')
    else:
        print(f'size: about {peak / 1000:.0f}k tokens at most of a {window / 1000:.0f}k window: '
              f'does not fit in one session. Parts (entry ranges, one session each, one after another): '
              + ', '.join(f'{a}-{b}' for a, b in parts))


def cmd_precheck(args):
    """Cheap numbers before a review: is the batch worth reviewing, or should it
    be rejected whole? Lint hint counts, strings identical to the source, source
    not in English, form of address, Latin American forms, calques, a sample."""
    import collections
    import contextlib
    import io
    import random
    po = args[0]
    _, es = parse(po)

    def tr(e):
        return e.get('msgstr') or ' '.join(e.get('msgstr_plural') or [])

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_lint([po])
    lint = buf.getvalue()
    kinds = collections.Counter()
    for line in lint.splitlines():
        for h in re.sub(r' \[nota: [^\]]*\]', '', line.split(': ', 1)[-1]).split(' | '):
            m = re.match(r'(glossary: [\w -]+? →|glossary term left in English: [\w -]+? →|capitals mid-sentence|'
                         r'non-Spanish quotes|«#%d»|«ej\.»|length|glossary: [\w -]+? is not translated)', h)
            kinds[m.group(1) if m else h[:40]] += 1
    print(f'{len(es)} strings · {len(lint.splitlines())} with lint hints')
    print('  ' + ' · '.join(f'{k} {v}' for k, v in kinds.most_common(10)))
    same = [e for e in es if e.get('msgstr') and e['msgstr'] == e['msgid']]
    print(f'identical to the source: {len(same)}  ' + ', '.join(f'#{e["n"]} {e["msgid"][:25]!r}' for e in same[:12]))
    spanish_src = [e for e in es if re.search(r'\b(el|la|los|las|de|que|para|con)\b', e['msgid'])
                   and not re.search(r'\b(the|and|to|of|is|your|for|a|an)\b', e['msgid'], re.I)]
    print(f'source looks Spanish: {len(spanish_src)}')
    your = [e for e in es if re.search(r'\byour\b', e['msgid'], re.I)]
    su = sum(1 for e in your if re.search(r'\b[Ss]us?\b', tr(e)))
    tu = sum(1 for e in your if re.search(r'\b[Tt]us?\b', tr(e)))
    usted = [e for e in es if re.search(r'\b(usted|Por favor,? (?:seleccione|introduzca|ingrese|vuelva|compruebe|espere|intente)|'
                                        r'Busque|Seleccione|Introduzca|Ingrese|Haga clic|Compruebe|Pulse|Elija|Revise|Guarde)\b', tr(e))]
    formal = su >= 5 and tu * 4 <= su
    print(f'address: "your" → su {su}, tu {tu} · usted forms in {len(usted)} strings'
          + (' · FORMAL REGISTER THROUGHOUT (su far above tu; the usted count misses most imperatives)' if formal else ''))
    import csv
    alts = set()
    for name in ('glossary.csv', 'glossary-overrides.csv'):
        if os.path.exists(RES + name):
            with open(RES + name, encoding='utf-8') as f:
                alts |= {r[1].strip().lower() for r in csv.reader(f) if len(r) > 1 and ' / ' in r[1]}
    slashes = [e for e in es if '/' not in e['msgid'] + (e.get('msgid_plural') or '')
               and any(a in tr(e).lower() for a in alts)]
    print(f'glossary alternatives pasted whole (" / " list from the glossary): {len(slashes)}  '
          + ' | '.join(f'#{e["n"]} {tr(e)[:50]!r}' for e in slashes[:4])
          + (' · SEARCH AND REPLACE WITHOUT CARE' if slashes else ''))
    latam = [e for e in es if re.search(r'\b(computadora?|celular|ingres[ae]|ingresar|reporte|carro de compras|órdenes|ordenes|'
                                        r'desplegar|cliquea|clickea|hacer click|qué tan\b)', tr(e), re.I)]
    print(f'Latin American forms: {len(latam)}  ' + ' | '.join(f'#{e["n"]} {tr(e)[:40]!r}' for e in latam[:4]))
    calques = [e for e in es if re.search(r'\b(ha sido|han sido|fue|fueron) \w+(ado|ido|ada|ida)s?\b|\bfalló\b|^Opcionalmente\b', tr(e))]
    print(f'passives and calques: {len(calques)}  ' + ' | '.join(f'#{e["n"]} {tr(e)[:40]!r}' for e in calques[:4]))
    cmd_size([po] + args[1:])
    random.seed(2)
    print('sample:')
    for e in random.sample(es, min(10, len(es))):
        print(f'  #{e["n"]} {e["msgid"][:70]!r} → {tr(e)[:80]!r}')


def _url_name(url):
    """translate.wordpress.org project URL -> (name, project path, import URL)."""
    m = re.match(r'https://translate\.wordpress\.org/projects/(.+?)/?$', url.split('?')[0])
    if not m:
        sys.exit('Not a translate.wordpress.org project URL')
    path = re.sub(r'/[a-z]{2,3}(?:-[a-z]+)?/default$', '', m.group(1).rstrip('/'))
    parts = path.split('/')
    name = '-'.join(parts[1:] if parts[0] in ('wp-plugins', 'wp-themes', 'meta', 'apps') and len(parts) > 1 else parts)
    return name, path, f'https://translate.wordpress.org/projects/{path}/es/default/import-translations/'


def cmd_prepare(args):
    """prepare <project URL> [--translate] [--window N] [--force]"""
    import shutil
    import tempfile
    translate = '--translate' in args
    window = int(args[args.index('--window') + 1]) if '--window' in args else 1_000_000
    url = [a for i, a in enumerate(args) if not a.startswith('--') and args[i - 1] != '--window'][0]
    name, _, imp = _url_name(url)
    skill = 'translate' if translate else 'review'
    tmp = tempfile.mkdtemp()
    try:
        _capture(cmd_fetch, [url, tmp] + (['--untranslated'] if translate else []))
        po = os.path.abspath(f'{name}.po')
        shutil.move(os.path.join(tmp, 'original.po'), po)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    header, entries = parse(po)
    if not entries:
        print(f'STOP: no {"untranslated" if translate else "waiting"} strings in {url}. Tell the user and stop.')
        return
    if not translate:
        pre = _capture(cmd_precheck, [po, '--window', str(window)])
        open(os.path.abspath(f'{name}-precheck.txt'), 'w', encoding='utf-8').write(pre)
        m = re.search(r'source looks Spanish: (\d+)', pre)
        spanish = m and int(m.group(1)) * 3 > len(entries)
        if ('FORMAL REGISTER THROUGHOUT' in pre or 'SEARCH AND REPLACE WITHOUT CARE' in pre or spanish) \
                and '--force' not in args:
            print(pre)
            print('STOP: these numbers point to a batch to reject whole. Show the user the numbers above and the sample, '
                  'and ask whether to review it or reject it whole. Do nothing else until they answer; if they say '
                  f'review it, run: {_py()} {os.path.abspath(__file__)} prepare {url} --force')
            return
    ranges = _parts(po, entries, translate, window)
    files = [po]
    if len(ranges) > 1:
        files = []
        for k, (a, b) in enumerate(ranges, 1):
            f = os.path.abspath(f'{name}-part{k}.po')
            blocks = ([header] if header else []) + [write_entry(e) for e in entries if a <= e['n'] <= b]
            open(f, 'w', encoding='utf-8').write('\n\n'.join(blocks) + '\n')
            files.append(f)
    print(f'{len(entries)} strings to {skill} in {len(files)} file(s).')
    if len(files) == 1:
        print(f'Now use the {skill} skill of the wordpress-translator-es plugin on: {files[0]}')
    else:
        print(f'Do the parts one at a time, in order, never in parallel. For each part, start a subagent (a new, '
              f'clean context) and give it only this task: "Use the {skill} skill of the wordpress-translator-es '
              f'plugin on <part file>. Follow it fully. Answer only with the path of the file it gives and its '
              f'doubts." Wait for it before starting the next part:')
        for f in files:
            print(f'   {f}')
        print(f'When all the parts are done, run: {_py()} {os.path.abspath(__file__)} merge {name}'
              f'{" --translate" if translate else ""}')
        print('It joins the parts into one file. Give the user that file and the doubts of all the parts.')
        print(f'If you cannot start subagents, tell the user, and offer to {skill} one part per new conversation '
              'and then run merge.')
    print(f'When the skill gives the file, add this import URL to your answer: {imp}')


MAX_PART = 500  # strings per session: past this a small model starts skipping rules it has loaded (round 42)


def _parts(po, entries, translate, window):
    """Entry ranges, one per session: as many as the size estimate needs, and never more than
    MAX_PART strings each (rounds 42-48: 2437 strings in one session left about half of the
    glossary errors, in any reading order; four sessions of ~610 fixed nearly all)."""
    import math
    _, _, ranges = size_estimate(po, translate, window)
    ranges = ranges or [(entries[0]['n'], entries[-1]['n'])]
    out = []
    for a, b in ranges:
        ns = [e['n'] for e in entries if a <= e['n'] <= b]
        k = math.ceil(len(ns) / MAX_PART)
        step = math.ceil(len(ns) / k)
        out += [(ns[i], ns[min(i + step, len(ns)) - 1]) for i in range(0, len(ns), step)]
    return out


def cmd_merge(args):
    """merge <name> [--translate]: join the files the skill gave for <name>-partK.po into one."""
    import glob
    import shutil
    import subprocess
    translate = '--translate' in args
    name = [a for a in args if not a.startswith('--')][0]
    parts = sorted(glob.glob(f'{name}-part*.po'), key=lambda f: int(re.search(r'-part(\d+)\.po$', f).group(1))
                   if re.search(r'-part(\d+)\.po$', f) else 0)
    parts = [f for f in parts if re.search(r'-part\d+\.po$', f)]
    if not parts:
        sys.exit(f'STOP: no {name}-partK.po files here. Run merge in the folder where prepare ran.')
    suffix = '-es_ES.po' if translate else '-corrected.po'
    done = [f[:-3] + suffix for f in parts]
    missing = [d for d in done if not os.path.exists(d)]
    if missing:
        sys.exit(f'Missing: {", ".join(missing)}. Do those parts with the skill and run merge again.')
    header, blocks = None, []
    for d in done:
        h, es = parse(d)
        header = header or h
        blocks += [write_entry(e) for e in es]
    out = os.path.abspath(name + suffix)
    open(out, 'w', encoding='utf-8').write('\n\n'.join(([header] if header else []) + blocks) + '\n')
    msgfmt = shutil.which('msgfmt')
    if msgfmt:
        r = subprocess.run([msgfmt, '--check', '-o', os.devnull, out], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr.strip())
            sys.exit(f'msgfmt found the problems above in {out}. Fix them in the part they come from, '
                     'run the skill\'s finish for that part, and run merge again.')
    else:
        print('Tell the user: the file could not be checked with msgfmt because msgfmt is not installed.')
    print(f'OK: {out} · {len(blocks)} strings from {len(parts)} parts.')


COMMANDS = {'prepare': cmd_prepare, 'merge': cmd_merge, 'fetch': cmd_fetch, 'precheck': cmd_precheck, 'size': cmd_size, 'lint': cmd_lint}


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--range' in argv:
        k = argv.index('--range')
        a, b = argv[k + 1].split('-')
        po_tool.RANGE = (int(a), int(b))
        del argv[k:k + 2]
    if not argv or argv[0] not in COMMANDS:
        sys.exit(__doc__)
    COMMANDS[argv[0]](argv[1:])
