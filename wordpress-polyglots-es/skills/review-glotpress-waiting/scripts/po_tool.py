#!/usr/bin/env python3
"""File plumbing of the translate and review skills (stdlib only). No translation
rules here: the model applies the style guide and the glossary next to this script.

Commands:
  start <file.po|.pot> [--translate] [--work DIR]
      Work folder (<name>-work/ in the current folder unless --work) and the
      entries file (parts only if over one Read). Prints the exact steps: read
      the style guide, the glossary and the entries, write the decisions, finish.
  finish <work folder>
      Build <name>-corrected.po (review: only the strings to change) or
      <name>-es_ES.po (translate: the whole file) in the folder where start
      ran, and check it (also with msgfmt --check when it is installed).
  extract <file.po> [out.jsonl]
      One JSON object per entry: n, ctx, comments, flags, msgid, msgid_plural,
      msgstr (or msgstr_plural). Strings are unescaped (real newlines/quotes).
  check <original.po> <decisions.jsonl>
      Check every proposed translation against its msgid: placeholders, HTML
      tags, entities, URLs, newlines, edge spaces, final punctuation, length,
      Spanish quotes.
  build <original.po> <decisions.jsonl> <out.po> [--full] [--report out.md]
      Review (default): the original header plus only the entries whose
      verdict is "fix" or "reject" (and doubts that change the text).
      --full (translate): every entry, with an es_ES header.
      --report: a Markdown table of all decisions.
  --range A-B (extract): only entries A to B.

decisions.jsonl: one JSON object per changed or doubtful entry:
  {"n": 12, "verdict": "fix|reject|doubt", "msgstr": "...",
   "msgstr_plural": ["...", "..."], "comment": "..."}
Entries not listed are approved as they are.
"""
import json
import os
import re
import shutil
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


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


PH = re.compile(r'%(?:\d+\$)?[-+ #0]*\d*(?:\.\d+)?[sdifuxXoceEgGb%]|\{[A-Za-z0-9_.-]+\}|\[[a-z_]+\]')


TAG = re.compile(r'</?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>')


ENT = re.compile(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);')


URL = re.compile(r'https?://[^\s"<>)]+')


def bag(rx, s, group=0):
    return sorted(m.group(group) for m in rx.finditer(s))


ABBR_END = re.compile(r'\b(?:mín|máx|etc|ej|aprox|núm|pág|desc)\.$', re.I)


def end_punct(s):
    s = s.rstrip().replace('...', '…').rstrip('"\'»”’)]')
    if ABBR_END.search(s):  # «Distancia mín.» ends with an abbreviation, not a period
        return ''
    return s[-1:] if s[-1:] in ('.', ':', '!', '?', '…', ';') else ''


def length_off(src, tr):
    """GlotPress's length warning: the translation is 5 times the source or longer,
    or 0.2 times or shorter ("Lengths of source and translation differ too much").
    Returns the ratio when it fires, else None."""
    if not src or not tr:
        return None
    ratio = len(tr) / len(src)
    return None if 0.2 < ratio < 5 else ratio


def strip_json(text):
    """Drop JSON-like code ({"key": ...}, nested too): its straight quotes are code, not text."""
    while True:
        new = re.sub(r'\{[^{}]*\}', lambda m: '' if re.search(r'"\s*:', m.group(0)) else m.group(0), text)
        if new == text:
            return text
        text = new


def check_pair(src, tr):
    problems = []
    r = length_off(src, tr)
    if r is not None:
        problems.append(f'length: translation {r:.1f} times the source; GlotPress flags it '
                        '(over 5 or under 0.2) and it may break the interface: make it concise')
    if bag(PH, src) != bag(PH, tr):
        problems.append(f'placeholders {bag(PH, src)} != {bag(PH, tr)}')
    if bag(TAG, src, 1) != bag(TAG, tr, 1):
        problems.append(f'HTML tags {bag(TAG, src, 1)} != {bag(TAG, tr, 1)}')
    # "&amp;" may legitimately become "y", and typographic quotes and apostrophes
    # ("group&#8217;s") often have no place in Spanish, so they are not required.
    TYPO = {'&amp;', '&#8216;', '&#8217;', '&#8220;', '&#8221;', '&lsquo;', '&rsquo;', '&ldquo;', '&rdquo;',
            '&#039;', '&#39;', '&apos;', '&quot;', '&#34;'}
    ents = lambda s: [x for x in bag(ENT, s) if x not in TYPO]
    if ents(src) != ents(tr):
        problems.append(f'entities {ents(src)} != {ents(tr)}')
    if bag(URL, src) != bag(URL, tr):
        problems.append('URLs differ')
    if src.count('\n') != tr.count('\n'):
        problems.append(f'newlines {src.count(chr(10))} != {tr.count(chr(10))}')
    if (src[:1].isspace(), src[-1:].isspace()) != (tr[:1].isspace(), tr[-1:].isspace()):
        problems.append('leading/trailing whitespace differs')
    # GlotPress warns when the final punctuation differs: keep the source's (a period
    # added or dropped at the end is the usual case). Closing quotes and brackets do not count.
    if end_punct(src) != end_punct(tr):
        problems.append(f'final punctuation differs: {end_punct(src) or "none"} != {end_punct(tr) or "none"}')
    visible = strip_json(TAG.sub('', tr))
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


def locale_header(header):
    """A .pot header turned into an es_ES one: Language and Plural-Forms set,
    the header's fuzzy flag removed. Other fields are kept."""
    lines = [l for l in header.split('\n') if l.strip() != '#, fuzzy']
    text = '\n'.join(lines)
    for field, value in (('Language', 'es_ES'), ('Plural-Forms', 'nplurals=2; plural=(n != 1);')):
        pat = re.compile(rf'^"{field}:.*\\n"$', re.M)
        line = f'"{field}: {value}\\n"'
        if pat.search(text):
            text = pat.sub(lambda m: line, text)
        else:
            text += '\n' + line
    return text


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
    if full and header:
        header = locale_header(header)
    blocks = [header] if header else []
    written = 0
    for e in entries:
        d = decisions.get(e['n'])
        change = d is not None and d['verdict'] in ('fix', 'reject')
        if d is not None and d['verdict'] == 'doubt':
            # A doubt carries the model's best proposal and goes in like a change, so nothing is left
            # undecided in a file the reviewer imports before approving the rest. A doubt that keeps
            # the current text (or an untranslated one in translation mode) is written only if needed.
            old = e.get('msgstr_plural') if e.get('msgid_plural') is not None else e['msgstr']
            new = d.get('msgstr_plural') if 'msgstr_plural' in d else d.get('msgstr')
            untranslated = not any(e.get('msgstr_plural') or [e['msgstr']])
            change = new != old or (full and untranslated)
        if full or change:
            blocks.append(write_entry(e, d if change else None))
            written += 1
    open(out_path, 'w', encoding='utf-8').write('\n\n'.join(blocks) + '\n')
    if report:
        write_report(report, entries, decisions)
    print(f'{out_path}: {written} entries written; {errors} check problem(s)')
    sys.exit(1 if errors else 0)


PART_BYTES = 50_000  # the Read tool returns about this much in one call; a part over it comes back cut


def _py():
    exe = os.path.basename(sys.executable or 'python3')
    return 'python3' if exe.startswith('python3') or not exe else exe


def _capture(fn, args, rng=None):
    import contextlib
    import io
    global RANGE
    old, RANGE = RANGE, rng
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            try:
                fn(args)
            except SystemExit:
                pass
    finally:
        RANGE = old
    return buf.getvalue()


def cmd_start(args):
    """start <file.po|.pot> [--translate] [--work DIR]"""
    import shutil
    translate = '--translate' in args
    work = args[args.index('--work') + 1] if '--work' in args else None
    src = [a for i, a in enumerate(args) if not a.startswith('--') and args[i - 1] != '--work'][0]
    cwd = os.getcwd()
    job = {'mode': 'translate' if translate else 'review'}
    if not os.path.exists(src):
        sys.exit(f'STOP: {src} does not exist. Ask the user for the file.')
    name = re.sub(r'\.(po|pot)$', '', os.path.basename(src))
    if translate:
        name = re.sub(r'[-_]es(_ES)?$', '', name)
    work = os.path.abspath(work or os.path.join(cwd, f'{name}-work'))
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    orig = os.path.join(work, 'original.po')
    shutil.copyfile(src, orig)
    _, entries = parse(orig)
    if translate:
        todo = [e for e in entries if 'fuzzy' in (e['flags'] or '') or not any(e['msgstr_plural'] or [e['msgstr']])]
    else:
        todo = entries
    if not todo:
        print(f'STOP: no strings to {job["mode"]} in {src}. Tell the user and stop.')
        return
    suffix = '-es_ES.po' if translate else '-corrected.po'
    job.update(name=name, out=os.path.join(cwd, name + suffix), todo=[e['n'] for e in todo])
    def render(part, k, total):
        rng = (part[0]['n'], part[-1]['n'])
        ns = {e['n'] for e in part}
        head = f'# Part {k} of {total}: entries {rng[0]}-{rng[1]}' if total > 1 else '# Entries to ' + job['mode']
        out = [head, '', '## Entries (one JSON object per line)', '',
                '\n'.join(l for l in _capture(cmd_extract, [orig], rng).splitlines() if json.loads(l)['n'] in ns)]
        return '\n'.join(out) + '\n'

    # One file if it fits in one Read; otherwise parts cut by size (equal bytes of entries),
    # never by a fixed number of strings. Add a part until every part fits.
    weight = [len(json.dumps(e, ensure_ascii=False)) for e in todo]
    n = -(-len(render(todo, 1, 1).encode('utf-8')) // PART_BYTES)
    while True:
        target, parts, cur, acc = sum(weight) / n, [], [], 0
        for e, w in zip(todo, weight):
            if cur and acc + w > target * 1.0001 and len(parts) < n - 1:
                parts.append(cur)
                cur, acc = [], 0
            cur.append(e)
            acc += w
        parts.append(cur)
        if all(len(render(p, 1, 1).encode('utf-8')) <= PART_BYTES for p in parts) or n >= len(todo):
            break
        n += 1
    files = []
    for k, part in enumerate(parts, 1):
        f = os.path.join(work, 'entries.md' if len(parts) == 1 else f'entries-{k}.md')
        open(f, 'w', encoding='utf-8').write(render(part, k, len(parts)))
        files.append(f)
    job['parts'] = len(files)
    json.dump(job, open(os.path.join(work, 'job.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # The whole guide and the whole glossary. Skill: next to this script.
    # Development repository: the packaged copies.
    refs = _HERE if os.path.exists(os.path.join(_HERE, 'style-guide.md')) \
        else os.path.join(_HERE, '..', '..', 'wordpress-translator-es', 'skills', 'review', 'references')
    guide, gloss = os.path.abspath(os.path.join(refs, 'style-guide.md')), os.path.abspath(os.path.join(refs, 'glossary.md'))
    verb = 'translate' if translate else 'review'
    finish = f'{_py()} {os.path.abspath(__file__)} finish {work}'
    if len(files) == 1:
        print(f'{len(todo)} strings to {verb}. Do exactly these three steps, nothing else:')
        print('1. In ONE response, call Read 3 times at once, one call per file:')
        for f in (guide, gloss, files[0]):
            print(f'   {f}')
        print(f'2. {verb.capitalize()} every entry. Then, in ONE response, write all your decisions with one Write call to:')
        print(f'   {os.path.join(work, "decisions.jsonl")}')
        print(f'3. In the next response, alone: {finish}')
        return
    # Block by block: the guide and the glossary are read again with each block, and each block's
    # decisions are written before the next block is read (round 42: 2437 strings read in 8 parts and
    # all decisions written at the end left about half of the glossary errors unfixed).
    print(f'{len(todo)} strings to {verb}, in {len(files)} blocks. Do the blocks one at a time, in order, '
          'nothing else. For each block:')
    print('a. In ONE response, call Read 3 times at once, one call per file: the style guide, the glossary and the block.')
    print(f'b. {verb.capitalize()} every entry of the block. Then, in ONE response, write the decisions of that block '
          'with one Write call to its decisions file (an empty file if nothing changes).')
    print('Do not read the next block before writing the decisions of this one.')
    print(f'Style guide: {guide}')
    print(f'Glossary:    {gloss}')
    for k, f in enumerate(files, 1):
        print(f'Block {k}: {f} → decisions: {os.path.join(work, f"decisions-{k}.jsonl")}')
    print(f'When all the blocks are done, in the next response, alone: {finish}')


def cmd_finish(args):
    """finish <work folder>: build the final .po from decisions.jsonl and check it."""
    work = os.path.abspath(args[0])
    job = json.load(open(os.path.join(work, 'job.json'), encoding='utf-8'))
    merged = os.path.join(work, 'decisions.jsonl')
    parts = job.get('parts', 1)
    if parts > 1:
        # Each block has its own decisions file; decisions.jsonl is rebuilt from them on every run.
        files = [os.path.join(work, f'decisions-{k}.jsonl') for k in range(1, parts + 1)]
        missing = [f for f in files if not os.path.exists(f)]
        if missing:
            sys.exit(f'Missing: {", ".join(missing)}. Do those blocks (an empty file if nothing changes) '
                     'and run this same command again.')
        with open(merged, 'w', encoding='utf-8') as out:
            for f in files:
                for i, line in enumerate(open(f, encoding='utf-8'), 1):
                    if line.strip():
                        try:
                            json.loads(line)
                        except json.JSONDecodeError as x:
                            sys.exit(f'{f}:{i}: invalid JSON: {x}')
                        out.write(line.strip() + '\n')
        where = 'the decisions file of their block'
    else:
        where = 'decisions.jsonl'
    if not os.path.exists(merged):
        sys.exit(f'Missing: {merged}. Write it (an empty file if nothing changes) and run this same command again.')
    decisions = load_decisions(merged)
    if job['mode'] == 'translate':
        left = [n for n in job['todo'] if n not in decisions]
        if left:
            sys.exit(f'Not translated yet: entries {", ".join(map(str, left[:40]))}{"…" if len(left) > 40 else ""}. '
                     f'Add them to {where} and run this same command again.')
    build = [os.path.join(work, 'original.po'), merged, job['out'], '--report', os.path.join(work, 'report.md')]
    if job['mode'] == 'translate':
        build.append('--full')
    text = _capture(cmd_build, build)
    problems = [l for l in text.splitlines() if l.startswith('#')]
    if problems:
        print('\n'.join(problems))
        sys.exit(f'{len(problems)} problem(s) above. The file is written: {job["out"]}. Fix the real problems in '
                 f'{where} and run this same command again. If only false positives are left, give the user '
                 'this file and say which ones they are.')
    msgfmt = shutil.which('msgfmt')
    if msgfmt:
        r = subprocess.run([msgfmt, '--check', '-o', os.devnull, job['out']], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr.strip())
            sys.exit(f'msgfmt found the problems above in the final file: fix those entries in {where} '
                     'and run this same command again.')
    changed = sum(1 for d in decisions.values() if d['verdict'] in ('fix', 'reject', 'doubt'))
    doubts = [n for n, d in decisions.items() if d['verdict'] == 'doubt']
    if not msgfmt:
        print('Tell the user: the file could not be checked with msgfmt because msgfmt is not installed.')
    print(f'OK: {job["out"]} · {changed} strings {"translated" if job["mode"] == "translate" else "to change"}'
          f' · {len(doubts)} doubt(s) · 0 problems.')
    print('Now answer the user as the skill says. Do not run anything else.')


COMMANDS = {'start': cmd_start, 'finish': cmd_finish, 'extract': cmd_extract, 'check': cmd_check, 'build': cmd_build}


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--range' in argv:
        k = argv.index('--range')
        a, b = argv[k + 1].split('-')
        RANGE = (int(a), int(b))
        del argv[k:k + 2]
    if not argv or argv[0] not in COMMANDS:
        sys.exit(__doc__)
    COMMANDS[argv[0]](argv[1:])
