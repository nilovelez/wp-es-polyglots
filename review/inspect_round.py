"""Inspect a training round: tool calls and errors, precheck head, decisions.
Usage: python3 review/inspect_round.py <round folder> [all | sample N]"""
import glob
import json
import os
import random
import sys

R = sys.argv[1].rstrip('/')
mode = sys.argv[2:] or ['sample', '30']
for line in open(R + '/run.jsonl'):
    if not line.startswith('{'):
        continue
    e = json.loads(line)
    if e.get('type') == 'assistant':
        for c in e['message'].get('content', []):
            if c.get('type') == 'tool_use':
                i = c['input']
                print('CALL', c['name'], str(i.get('command') or i.get('file_path') or i.get('skill') or i.get('pattern'))[-70:])
    if e.get('type') == 'user' and isinstance(e['message'].get('content'), list):
        for c in e['message']['content']:
            if c.get('type') == 'tool_result' and c.get('is_error'):
                print('   ERROR', str(c.get('content'))[:160])
work = glob.glob(R + '/*-work')
if not work:
    sys.exit('no work folder')
w = work[0]
if os.path.exists(w + '/precheck.txt'):
    print(''.join(open(w + '/precheck.txt').readlines()[:9]))
po = {}
for f in sorted(glob.glob(w + '/entries*.md')):
    for l in open(f):
        if l.startswith('{"n"'):
            x = json.loads(l)
            po[x['n']] = x
if not os.path.exists(w + '/decisions.jsonl'):
    sys.exit('no decisions.jsonl')
ds = [json.loads(l) for l in open(w + '/decisions.jsonl') if l.strip()]
print(len(ds), 'decisions')
if mode[0] == 'sample':
    random.seed(len(ds))
    ds = random.sample(ds, min(int(mode[1]), len(ds)))
    ds.sort(key=lambda d: d['n'])
for d in ds:
    x = po[d['n']]
    old = x.get('msgstr', x.get('msgstr_plural'))
    new = d.get('msgstr', d.get('msgstr_plural'))
    print(d['n'], d['verdict'], '|', x['msgid'][:90], '|', str(old)[:110], '=>', str(new)[:130],
          ('| ' + d['comment']) if d.get('comment') else '')
