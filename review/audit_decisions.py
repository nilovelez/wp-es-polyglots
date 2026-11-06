"""Opus audit for direct rounds: drop decisions that should not be applied.

Usage: python3 review/audit_decisions.py <round-folder> <n>=<reason> [<n>=<reason> ...]

Keeps the translator's decisions.jsonl untouched (it is the model's output, used for
measurement) and writes audited.jsonl without the dropped entries, plus audit.md with
the reasons. Build corrected.po from audited.jsonl.
"""
import json
import os
import sys

folder = sys.argv[1]
drops = {}
for arg in sys.argv[2:]:
    n, _, reason = arg.partition('=')
    drops[int(n)] = reason
rows = [json.loads(l) for l in open(os.path.join(folder, 'decisions.jsonl'), encoding='utf-8') if l.strip()]
kept = [r for r in rows if r['n'] not in drops]
with open(os.path.join(folder, 'audited.jsonl'), 'w', encoding='utf-8') as f:
    for r in kept:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(os.path.join(folder, 'audit.md'), 'w', encoding='utf-8') as f:
    f.write('# Audit (direct round, no human review)\n\n')
    f.write(f'Model decisions: {len(rows)} · applied: {len(kept)} · dropped: {len(rows) - len(kept)}\n\n')
    for r in rows:
        if r['n'] in drops:
            f.write(f'- #{r["n"]} dropped: {drops[r["n"]]}\n  - model: {r.get("msgstr", r.get("msgstr_plural"))}\n')
print(f'{len(rows)} decisions, {len(kept)} applied, {len(rows) - len(kept)} dropped')
