#!/usr/bin/env python3
"""Deterministic .po helpers for the translation skill (stdlib only).

Commands:
  extract <file.po> [out.jsonl]
      One JSON object per entry: n, ctx, comments, flags, msgid, msgid_plural,
      msgstr (or msgstr_plural). Strings are unescaped (real newlines/quotes).
  check <original.po> <decisions.jsonl>
      Check every proposed translation against its msgid: placeholders, HTML
      tags, entities, newlines, leading/trailing spaces, Spanish quotes.
  build <original.po> <decisions.jsonl> <out.po> [--full] [--report out.md]
      Review mode (default): write the original header plus only the entries
      whose verdict is "fix" or "reject" (the strings to change).
      --full (translation mode): write every entry, applying decisions.
      --report: write a Markdown table of all decisions for the human reviewer.
  compare <reference.po> <candidate.po>
      Compare two corrected/translated files by msgctxt+msgid: same, different,
      only in one of them. Used to benchmark the skill against human output.
  review-po <original.po> <decisions.jsonl> <out.po>
      Every entry for the human reviewer (Poedit). Entries with a proposal get
      it applied, the fuzzy flag, and translator comments with the verdict,
      the reason and the original translation.
  finalize <original.po> <decisions.jsonl> <human.po> <corrected.po> [--report out.md]
      After the human saves the review file: corrected.po with the entries the
      human changed, and a learning report (proposals kept, edited, reverted,
      and changes the model missed).
  glossary <file.po> [glossary.csv]
      Glossary entries whose English term appears in the file, with the
      entry numbers where they appear. Default: resources/glossary.csv.
  lint <file.po> [glossary.csv]
      Review hints on the current translations: glossary terms missing or
      left in English, capitals mid-sentence, «ej.», straight quotes.
  --range A-B (extract, glossary, lint): only entries A to B, for large files
      reviewed in slices.
  tm <file.po> [translation-memory.csv]
      Translation memory rows that exactly match a msgid in the file.

decisions.jsonl: one JSON object per changed or doubtful entry:
  {"n": 12, "verdict": "fix|reject|doubt", "msgstr": "...",
   "msgstr_plural": ["...", "..."], "comment": "..."}
Entries not listed are approved as they are.
"""
import json
import re
import sys

RES = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'resources', '')
ESCAPES = {'n': '\n', 't': '\t', 'r': '\r', '"': '"', '\\': '\\', 'a': '\a', 'b': '\b', 'f': '\f', 'v': '\v'}


def unescape(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            out.append(ESCAPES.get(s[i + 1], '\\' + s[i + 1]))
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def escape(s):
    return (s.replace('\\', '\\\\').replace('"', '\\"')
             .replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r'))


def parse(path):
    """Return (header_text, entries). header_text is the raw header block."""
    text = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    blocks = re.split(r'\n\s*\n', text.strip('\n'))
    header, entries = None, []
    for block in blocks:
        e = {'comments': [], 'flags': [], 'ctx': None, 'msgid': None,
             'msgid_plural': None, 'msgstr': None, 'msgstr_plural': {}}
        key = None
        for line in block.split('\n'):
            if line.startswith('#~'):
                key = None
                continue
            if line.startswith('#,'):
                e['flags'] += [f.strip() for f in line[2:].split(',') if f.strip()]
                e['comments'].append(line)
                continue
            if line.startswith('#'):
                e['comments'].append(line)
                continue
            m = re.match(r'^(msgctxt|msgid_plural|msgid|msgstr\[(\d+)\]|msgstr)\s+"(.*)"\s*$', line)
            if m:
                kw, idx, val = m.group(1), m.group(2), m.group(3)
                if idx is not None:
                    key = ('plural', int(idx))
                    e['msgstr_plural'][int(idx)] = val
                else:
                    key = {'msgctxt': 'ctx'}.get(kw, kw)
                    e[key] = val
                continue
            m = re.match(r'^"(.*)"\s*$', line)
            if m and key:
                if isinstance(key, tuple):
                    e['msgstr_plural'][key[1]] += m.group(1)
                else:
                    e[key] += m.group(1)
        if e['msgid'] is None:
            continue
        for k in ('ctx', 'msgid', 'msgid_plural', 'msgstr'):
            if e[k] is not None:
                e[k] = unescape(e[k])
        e['msgstr_plural'] = [unescape(e['msgstr_plural'][i]) for i in sorted(e['msgstr_plural'])]
        if e['msgid'] == '' and header is None and e['ctx'] is None:
            header = block
            continue
        e['n'] = len(entries) + 1
        entries.append(e)
    return header, entries


def key_of(e):
    return (e.get('ctx') or '') + '\x04' + e['msgid']


def load_decisions(path):
    out = {}
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError as x:
            sys.exit(f'{path}:{i}: invalid JSON: {x}')
        if d.get('verdict') not in ('fix', 'reject', 'doubt'):
            sys.exit(f'{path}:{i}: verdict must be fix, reject or doubt')
        out[int(d['n'])] = d
    return out


# ---------- checks ----------

PH = re.compile(r'%(?:\d+\$)?[-+ #0]*\d*(?:\.\d+)?[sdifuxXoceEgGb%]|\{[A-Za-z0-9_.-]+\}|\[[a-z_]+\]')
TAG = re.compile(r'</?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>')
ENT = re.compile(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);')
URL = re.compile(r'https?://[^\s"<>)]+')


def bag(rx, s, group=0):
    return sorted(m.group(group) for m in rx.finditer(s))


def check_pair(src, tr):
    problems = []
    if bag(PH, src) != bag(PH, tr):
        problems.append(f'placeholders {bag(PH, src)} != {bag(PH, tr)}')
    if bag(TAG, src, 1) != bag(TAG, tr, 1):
        problems.append(f'HTML tags {bag(TAG, src, 1)} != {bag(TAG, tr, 1)}')
    # "&amp;" may legitimately become "y", so it is not required.
    ents = lambda s: [x for x in bag(ENT, s) if x != '&amp;']
    if ents(src) != ents(tr):
        problems.append(f'entities {ents(src)} != {ents(tr)}')
    if bag(URL, src) != bag(URL, tr):
        problems.append('URLs differ')
    if src.count('\n') != tr.count('\n'):
        problems.append(f'newlines {src.count(chr(10))} != {tr.count(chr(10))}')
    if (src[:1].isspace(), src[-1:].isspace()) != (tr[:1].isspace(), tr[-1:].isspace()):
        problems.append('leading/trailing whitespace differs')
    visible = TAG.sub('', tr)
    if re.search(r'(?<![=\w])"[^"<>=]+"(?![\w>])', visible) or re.search(r'[“”]', visible):
        problems.append('non-Spanish quotes (use «»)')
    if not tr.strip() and src.strip():
        problems.append('empty translation')
    return problems


def translations(e, d=None):
    """List of (source, translation) pairs for an entry, after decision d."""
    if e['msgid_plural'] is not None:
        tr = (d or {}).get('msgstr_plural') or e['msgstr_plural']
        srcs = [e['msgid']] + [e['msgid_plural']] * (len(tr) - 1)
        return list(zip(srcs, tr))
    tr = (d or {}).get('msgstr', e['msgstr']) if d else e['msgstr']
    return [(e['msgid'], tr or '')]


def run_checks(entries, decisions):
    by_n = {e['n']: e for e in entries}
    errors = 0
    for n, d in sorted(decisions.items()):
        if n not in by_n:
            print(f'#{n}: no such entry')
            errors += 1
            continue
        if d['verdict'] == 'doubt' and 'msgstr' not in d and 'msgstr_plural' not in d:
            continue
        e = by_n[n]
        if e['msgid_plural'] is not None and 'msgstr_plural' not in d:
            print(f'#{n}: plural entry needs msgstr_plural')
            errors += 1
            continue
        if e['msgid_plural'] is None and 'msgstr' not in d:
            print(f'#{n}: missing msgstr')
            errors += 1
            continue
        for src, tr in translations(e, d):
            for p in check_pair(src, tr):
                print(f'#{n}: {p}')
                errors += 1
    return errors


# ---------- output ----------

def fmt(kw, s):
    return f'{kw} "{escape(s)}"'


def write_entry(e, d=None):
    lines = [c for c in e['comments'] if not c.startswith('# polyglots:')]
    if e['ctx'] is not None:
        lines.append(fmt('msgctxt', e['ctx']))
    lines.append(fmt('msgid', e['msgid']))
    if e['msgid_plural'] is not None:
        lines.append(fmt('msgid_plural', e['msgid_plural']))
        tr = (d or {}).get('msgstr_plural') or e['msgstr_plural'] or ['', '']
        for i, s in enumerate(tr):
            lines.append(fmt(f'msgstr[{i}]', s))
    else:
        tr = d['msgstr'] if d and 'msgstr' in d else (e['msgstr'] or '')
        lines.append(fmt('msgstr', tr))
    return '\n'.join(lines)


def cell(s):
    return (s or '').replace('|', '\\|').replace('\n', '\\n')


def write_report(path, entries, decisions):
    by_n = {e['n']: e for e in entries}
    counts = {'fix': 0, 'reject': 0, 'doubt': 0}
    for d in decisions.values():
        counts[d['verdict']] += 1
    approved = len(entries) - len(decisions)
    out = [f'Strings: {len(entries)} · approve as is: {approved} · fix: {counts["fix"]} · '
           f'reject: {counts["reject"]} · doubt: {counts["doubt"]}', '',
           '| # | Original | Current | Verdict | Proposed | Comment |', '|---|---|---|---|---|---|']
    for n, d in sorted(decisions.items()):
        e = by_n[n]
        cur = e['msgstr'] if e['msgid_plural'] is None else ' / '.join(e['msgstr_plural'])
        new = d.get('msgstr') if 'msgstr' in d else ' / '.join(d.get('msgstr_plural', []))
        out.append(f'| {n} | {cell(e["msgid"])} | {cell(cur)} | {d["verdict"]} | {cell(new)} | {cell(d.get("comment"))} |')
    open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')


# ---------- commands ----------

RANGE = None  # (first, last) entry numbers, set by --range A-B


def parse_sel(path):
    _, entries = parse(path)
    if RANGE:
        entries = [e for e in entries if RANGE[0] <= e['n'] <= RANGE[1]]
    return entries


def cmd_extract(args):
    entries = parse_sel(args[0])
    out = open(args[1], 'w', encoding='utf-8') if len(args) > 1 else sys.stdout
    for e in entries:
        o = {'n': e['n']}
        if e['ctx'] is not None:
            o['ctx'] = e['ctx']
        notes = [c[2:].strip() for c in e['comments'] if c.startswith('#.')]
        if notes:
            o['note'] = ' '.join(notes)
        if e['flags']:
            o['flags'] = e['flags']
        o['msgid'] = e['msgid']
        if e['msgid_plural'] is not None:
            o['msgid_plural'] = e['msgid_plural']
            o['msgstr_plural'] = e['msgstr_plural']
        else:
            o['msgstr'] = e['msgstr']
        out.write(json.dumps(o, ensure_ascii=False) + '\n')


def cmd_check(args):
    _, entries = parse(args[0])
    errors = run_checks(entries, load_decisions(args[1]))
    print(f'{errors} problem(s)')
    sys.exit(1 if errors else 0)


def cmd_build(args):
    full = '--full' in args
    report = None
    if '--report' in args:
        report = args[args.index('--report') + 1]
    pos = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--report')]
    orig, dec_path, out_path = pos[:3]
    header, entries = parse(orig)
    decisions = load_decisions(dec_path)
    errors = run_checks(entries, decisions)
    blocks = [header] if header else []
    written = 0
    for e in entries:
        d = decisions.get(e['n'])
        change = d is not None and d['verdict'] in ('fix', 'reject')
        if full or change:
            blocks.append(write_entry(e, d if change else None))
            written += 1
    open(out_path, 'w', encoding='utf-8').write('\n\n'.join(blocks) + '\n')
    if report:
        write_report(report, entries, decisions)
    print(f'{out_path}: {written} entries written; {errors} check problem(s)')
    sys.exit(1 if errors else 0)


def cmd_compare(args):
    _, ref = parse(args[0])
    _, cand = parse(args[1])
    r = {key_of(e): e for e in ref}
    c = {key_of(e): e for e in cand}
    val = lambda e: e['msgstr'] if e['msgid_plural'] is None else '\x00'.join(e['msgstr_plural'])
    same = [k for k in r if k in c and val(r[k]) == val(c[k])]
    diff = [k for k in r if k in c and val(r[k]) != val(c[k])]
    only_r = [k for k in r if k not in c]
    only_c = [k for k in c if k not in r]
    print(f'reference {len(r)} · candidate {len(c)} · same {len(same)} · different {len(diff)} · '
          f'only in reference {len(only_r)} · only in candidate {len(only_c)}')
    for title, keys, show in (('DIFFERENT', diff, 'both'), ('ONLY IN REFERENCE', only_r, 'r'), ('ONLY IN CANDIDATE', only_c, 'c')):
        if not keys:
            continue
        print(f'\n## {title}')
        for k in keys:
            e = r.get(k) or c.get(k)
            print(f'\n- {e["msgid"][:120]}')
            if show in ('both', 'r'):
                print(f'  ref:  {val(r[k])}')
            if show in ('both', 'c'):
                print(f'  cand: {val(c[k])}')


def value(e):
    return e['msgstr'] if e['msgid_plural'] is None else '\x00'.join(e['msgstr_plural'])


def proposed(e, d):
    if d.get('msgstr_plural'):
        return '\x00'.join(d['msgstr_plural'])
    return d.get('msgstr', value(e))


def cmd_review_po(args):
    """Every entry for the human reviewer (Poedit): proposals applied and fuzzy,
    with the original translation and the reason as translator comments."""
    orig, dec_path, out_path = args[:3]
    header, entries = parse(orig)
    decisions = load_decisions(dec_path)
    blocks = [header] if header else []
    for e in entries:
        d = decisions.get(e['n'])
        if not d:
            blocks.append(write_entry(e))
            continue
        label = {'fix': 'Corrección', 'reject': 'Rechazo', 'doubt': 'DUDA'}[d['verdict']]
        one_line = lambda s: s.replace('\r', '').replace('\n', '\\n')
        cur = one_line(value(e).replace('\x00', ' / '))
        notes = [f'# [{label}] {one_line(d.get("comment", "").strip())}', f'# Original: {cur}']
        f = dict(e)
        f['comments'] = [c for c in e['comments'] if not c.startswith('#,') and not c.startswith('# polyglots:')]
        flags = [x for x in e['flags'] if x != 'fuzzy'] + ['fuzzy']
        f['comments'] = notes + [c for c in f['comments']] + ['#, ' + ', '.join(flags)]
        blocks.append(write_entry(f, d if ('msgstr' in d or 'msgstr_plural' in d) else None))
    open(out_path, 'w', encoding='utf-8').write('\n\n'.join(blocks) + '\n')
    print(f'{out_path}: {len(entries)} entries, {len(decisions)} with proposals (fuzzy)')


def cmd_finalize(args):
    """Compare original, model proposals and the human's saved file.
    Writes corrected.po (entries the human changed) and a learning report."""
    report = None
    if '--report' in args:
        report = args[args.index('--report') + 1]
    pos = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--report')]
    orig, dec_path, human_path, out_path = pos[:4]
    header, entries = parse(orig)
    decisions = load_decisions(dec_path)
    _, human = parse(human_path)
    hm = {key_of(e): e for e in human}
    cats = {'kept': [], 'edited': [], 'reverted': [], 'missed': [], 'doubt': []}
    blocks = [header] if header else []
    still_fuzzy, missing = [], []
    for e in entries:
        h = hm.get(key_of(e))
        if h is None:
            missing.append(e['n'])
            continue
        if 'fuzzy' in h['flags']:
            still_fuzzy.append(e['n'])
        o, fin = value(e), value(h)
        d = decisions.get(e['n'])
        m = proposed(e, d) if d else o
        if fin != o:
            ne = dict(e)
            blocks.append(write_entry(ne, {'msgstr': h['msgstr']} if e['msgid_plural'] is None else {'msgstr_plural': h['msgstr_plural']}))
        row = (e, o, m, fin, d)
        if d and d['verdict'] == 'doubt':
            cats['doubt'].append(row)
        elif m != o and fin == m:
            cats['kept'].append(row)
        elif m != o and fin == o:
            cats['reverted'].append(row)
        elif m != o:
            cats['edited'].append(row)
        elif fin != o:
            cats['missed'].append(row)
    open(out_path, 'w', encoding='utf-8').write('\n\n'.join(blocks) + '\n')
    changed = len(blocks) - (1 if header else 0)
    proposals = sum(len(cats[k]) for k in ('kept', 'edited', 'reverted'))
    summary = (f'Strings {len(entries)} · human changes {changed} · model proposals {proposals} · '
               f'kept {len(cats["kept"])} · edited {len(cats["edited"])} · reverted {len(cats["reverted"])} · '
               f'missed {len(cats["missed"])} · doubts {len(cats["doubt"])}')
    print(f'{out_path}: {changed} entries')
    print(summary)
    if still_fuzzy:
        print(f'WARNING: still fuzzy in the human file (not reviewed?): {still_fuzzy}')
    if missing:
        print(f'WARNING: missing in the human file: {missing}')
    if report:
        titles = {'kept': 'Model proposal kept', 'edited': 'Model proposal edited by the reviewer',
                  'reverted': 'Model proposal reverted (should have been approved)',
                  'missed': 'Missed by the model (reviewer changed it)', 'doubt': 'Doubts'}
        out = [summary, '']
        for k in ('missed', 'reverted', 'edited', 'doubt', 'kept'):
            if not cats[k]:
                continue
            out += [f'## {titles[k]} ({len(cats[k])})', '']
            for e, o, m, fin, d in cats[k]:
                out.append(f'- #{e["n"]} {e["msgid"]}'.replace('\n', '\\n'))
                out.append(f'  - original: {o}'.replace('\x00', ' / ').replace('\n', '\\n'))
                if m != o:
                    out.append(f'  - model: {m}'.replace('\x00', ' / ').replace('\n', '\\n'))
                    if d and d.get('comment'):
                        out.append(f'  - reason: {d["comment"]}')
                if fin not in (o, m):
                    out.append(f'  - final: {fin}'.replace('\x00', ' / ').replace('\n', '\\n'))
            out.append('')
        open(report, 'w', encoding='utf-8').write('\n'.join(out))


def read_csv(path):
    import csv
    return list(csv.DictReader(open(path, encoding='utf-8', newline='')))


def cmd_glossary(args):
    """Glossary entries whose English term appears in the file's msgids."""
    po, gl = args[0], (args[1] if len(args) > 1 else RES + 'glossary.csv')
    entries = parse_sel(po)
    text = '\n'.join(e['msgid'] + '\n' + (e['msgid_plural'] or '') for e in entries)
    text = TAG.sub(' ', text).lower()
    hits = {}
    for row in read_csv(gl):
        term = row['en'].strip().lower()
        if not term:
            continue
        rx = r'(?<![\w-])' + re.escape(term) + r'(?:s|es|ed|d|ing)?(?![\w-])'
        found = [e['n'] for e in entries if re.search(rx, TAG.sub(' ', e['msgid'] + ' ' + (e['msgid_plural'] or '')).lower())]
        if found:
            hits.setdefault(term, []).append((row, found))
    for term in sorted(hits):
        for row, found in hits[term]:
            desc = ' '.join(row.get('description', '').split())
            pos = row.get('pos', '')
            print(f'- {row["en"]} ({pos}) → {row["es"]}' + (f' — {desc}' if desc else '') + f'  [#{",".join(map(str, found[:15]))}{"…" if len(found) > 15 else ""}]')


def cmd_tm(args):
    """Translation memory rows that exactly match a msgid in the file."""
    po, tm = args[0], (args[1] if len(args) > 1 else RES + 'translation-memory.csv')
    _, entries = parse(po)
    rows = {r['en'].strip(): r for r in read_csv(tm)}
    for e in entries:
        r = rows.get(e['msgid'].strip())
        if r:
            print(f'#{e["n"]}: {r["en"]} → {r["es"]}' + (f' ({r["notas"]})' if r.get('notas') else ''))


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
    for row in read_csv(gl):
        en = row['en'].strip()
        es = row['es'].strip()
        desc = norm(row.get('description', ''))
        if not en or not es or len(en) < 3:
            continue
        m = merged.setdefault(en.lower(), {'en': en, 'es': [], 'opts': [], 'keep': False})
        m['keep'] |= 'no se traduce' in desc or norm(en) == norm(es)
        if es not in m['es']:
            m['es'].append(es)
        m['opts'] += [o.strip() for o in re.split(r'\s*/\s*', es) if o.strip()]
    rows = [(m['en'], ' | '.join(m['es']), m['opts'], m['keep']) for m in merged.values()]
    code = re.compile(r'<code>.*?</code>|https?://\S+', re.S)
    for e in entries:
        src = e['msgid'] + ' ' + (e['msgid_plural'] or '')
        tr = e['msgstr'] if e['msgid_plural'] is None else ' '.join(e['msgstr_plural'])
        if not tr.strip():
            continue
        s_plain, t_plain = TAG.sub(' ', code.sub(' ', src)), TAG.sub(' ', code.sub(' ', tr))
        s_low, t_norm = s_plain.lower(), norm(t_plain)
        hints = []
        for en, es, opts, keep in rows:
            rx = r'(?<![\w-])' + re.escape(en.lower()) + r'(?:s|es|ed|d|ing)?(?![\w-])'
            if not re.search(rx, s_low):
                continue
            if keep:
                if not re.search(rx, t_plain.lower()):
                    hints.append(f'glossary: {en} is not translated ({es})')
                continue
            if re.search(rx, t_plain.lower()):
                hints.append(f'glossary term left in English: {en} → {es}')
            elif not any(stem_in(o, t_norm) for o in opts):
                hints.append(f'glossary: {en} → {es}?')
        # Capitalized words mid-sentence that are not in the source (Title Case).
        caps = []
        for m in re.finditer(r'(?<=[^\s.:!?¡¿*>«(\-–—])\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñü]+)', t_plain):
            w = m.group(1)
            if w not in s_plain and w not in caps:
                caps.append(w)
        if caps:
            hints.append('capitals mid-sentence: ' + ', '.join(caps))
        if re.search(r'(?<!p\. )\bej\.', tr):
            hints.append('«ej.» → «p. ej.»')
        visible = TAG.sub('', tr)
        if re.search(r'(?<![=\w])"[^"<>=]+"(?![\w>])', visible) or re.search(r"(?<![\w=])'[^'<>]+'(?!\w)", visible) or re.search(r'[“”‘’]', visible):
            hints.append('non-Spanish quotes')
        if hints:
            print(f'#{e["n"]}: ' + ' | '.join(hints))


COMMANDS = {'extract': cmd_extract, 'check': cmd_check, 'build': cmd_build, 'compare': cmd_compare,
            'glossary': cmd_glossary, 'tm': cmd_tm, 'lint': cmd_lint,
            'review-po': cmd_review_po, 'finalize': cmd_finalize}

if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--range' in argv:
        k = argv.index('--range')
        a, b = argv[k + 1].split('-')
        RANGE = (int(a), int(b))
        del argv[k:k + 2]
    sys.argv = sys.argv[:1] + argv
    if len(sys.argv) < 3 or sys.argv[1] not in COMMANDS:
        sys.exit(__doc__)
    COMMANDS[sys.argv[1]](sys.argv[2:])
