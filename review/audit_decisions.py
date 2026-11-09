"""Opus audit for direct rounds: drop or edit decisions before applying them.

Usage: python3 review/audit_decisions.py <round-folder> [--edits edits.jsonl] [<n>=<reason> ...]

<n>=<reason> drops decision n (the string stays as the translator left it).
--edits: a JSONL file in the round folder, one {"n", "msgstr" | "msgstr_plural", "reason"}
per line, replacing the model's proposal for that entry (or adding one).

Keeps the translator's decisions.jsonl untouched (it is the model's output, used for
measurement) and writes audited.jsonl, plus audit.md with the reasons. Build
corrected.po from audited.jsonl.
"""
import json
import os
import sys

folder = sys.argv[1]
args = sys.argv[2:]
edits = {}
if '--edits' in args:
    i = args.index('--edits')
    path = os.path.join(folder, args[i + 1])
    for line in open(path, encoding='utf-8'):
        if line.strip():
            e = json.loads(line)
            edits[e['n']] = e
    del args[i:i + 2]
drops = {}
for arg in args:
    n, _, reason = arg.partition('=')
    drops[int(n)] = reason
rows = [json.loads(l) for l in open(os.path.join(folder, 'decisions.jsonl'), encoding='utf-8') if l.strip()]
by_n = {r['n']: r for r in rows}
out = []
for r in rows:
    if r['n'] in drops:
        continue
    if r['n'] in edits:
        r = dict(r)
        for k in ('msgstr', 'msgstr_plural'):
            r.pop(k, None)
            if k in edits[r['n']]:
                r[k] = edits[r['n']][k]
        if r.get('verdict') == 'doubt':  # an edited doubt is settled: it becomes a change
            r['verdict'] = 'reject'
            r['comment'] = edits[r['n']].get('reason', r.get('comment', ''))
    out.append(r)
for n, e in edits.items():
    if n not in by_n:
        out.append({'n': n, 'verdict': 'reject', 'reason': e.get('reason', ''),
                    **{k: e[k] for k in ('msgstr', 'msgstr_plural') if k in e}})
out.sort(key=lambda r: r['n'])
with open(os.path.join(folder, 'audited.jsonl'), 'w', encoding='utf-8') as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(os.path.join(folder, 'audit.md'), 'w', encoding='utf-8') as f:
    f.write('# Audit (direct round, no human review)\n\n')
    f.write(f'Model decisions: {len(rows)} · dropped: {len(drops)} · edited or added: {len(edits)} · applied: {len(out)}\n\n')
    for r in rows:
        if r['n'] in drops:
            f.write(f'- #{r["n"]} dropped: {drops[r["n"]]}\n  - model: {r.get("msgstr", r.get("msgstr_plural"))}\n')
    for n, e in sorted(edits.items()):
        old = by_n.get(n, {})
        f.write(f'- #{n} edited: {e.get("reason", "")}\n  - model: {old.get("msgstr", old.get("msgstr_plural"))}\n'
                f'  - audit: {e.get("msgstr", e.get("msgstr_plural"))}\n')
print(f'{len(rows)} decisions, {len(drops)} dropped, {len(edits)} edited or added, {len(out)} applied')
