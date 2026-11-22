#!/usr/bin/env python3
"""Repository tools for maintainers and training rounds (stdlib only). Not
shipped in any plugin.

Commands:
  glossary-update [--locale es]
      Download the official glossary from translate.wordpress.org into
      resources/glossary.csv. Then run skill/package.py.
  glossary <file.po> [glossary.csv]
      Glossary entries whose English term appears in the file.
  tm <file.po> [translation-memory.csv]
      Translation memory rows that exactly match a msgid in the file.
  compare <reference.po> <candidate.po>
      Compare two corrected/translated files by msgctxt+msgid.
  review-po <original.po> <decisions.jsonl> <out.po>
      Every entry for the human reviewer (Poedit), proposals applied as fuzzy
      with the verdict, reason and original translation as comments.
  finalize <original.po> <decisions.jsonl> <human.po> <corrected.po> [--report out.md]
      corrected.po with the entries the human changed, and a learning report.
"""
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import po_tool  # noqa: E402
from po_tool import *  # noqa: E402,F401,F403
from po_tool import _capture  # noqa: E402,F401
from glotpress import RES, read_csv, read_glossary  # noqa: E402,F401
RANGE = None


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
    if r and c:
        print(f'found {len(same) + len(diff)}/{len(r)} of the reference ({(len(same) + len(diff)) / len(r):.0%}), '
              f'{len(same)} with the same wording · extra {len(only_c)}/{len(c)} of the candidate '
              f'({len(only_c) / len(c):.0%})')
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


def cmd_glossary(args):
    """Glossary entries whose English term appears in the file's msgids."""
    po, gl = args[0], (args[1] if len(args) > 1 else RES + 'glossary.csv')
    entries = parse_sel(po)
    text = '\n'.join(e['msgid'] + '\n' + (e['msgid_plural'] or '') for e in entries)
    text = TAG.sub(' ', text).lower()
    hits = {}
    for row in read_glossary(gl):
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


def cmd_glossary_update(args):
    """Download the locale's official glossary from translate.wordpress.org."""
    import urllib.request
    locale = args[args.index('--locale') + 1] if '--locale' in args else 'es'
    url = f'https://translate.wordpress.org/locale/{locale}/default/glossary/-export/'
    req = urllib.request.Request(url, headers={'User-Agent': 'wordpress-translator skill'})
    data = urllib.request.urlopen(req, timeout=60).read().decode('utf-8')
    if not data.startswith('en,'):
        sys.exit('Unexpected glossary export; keeping the bundled copy.')
    open(RES + 'glossary.csv', 'w', encoding='utf-8', newline='').write(data)
    print(f'{RES}glossary.csv: {len(read_csv(RES + "glossary.csv"))} rows from {url}')


COMMANDS = {'compare': cmd_compare, 'review-po': cmd_review_po, 'finalize': cmd_finalize,
            'glossary': cmd_glossary, 'tm': cmd_tm, 'glossary-update': cmd_glossary_update}


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
