"""Summarize a translator session log written by review/run_translator.sh.

Usage: python3 review/run_summary.py <log.jsonl>

Prints every tool call (with the path or command), the permission denials, the final
answer, and duration, turns, tokens, cost and peak context (it must stay well under the
model's context window). Use the tool list to check that the session
read only its skill and its work files.
"""
import json
import sys

result = None
peak = 0
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        m = json.loads(line)
    except ValueError:
        continue
    if m.get('type') == 'assistant':
        u = m['message'].get('usage') or {}
        peak = max(peak, u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0)
                   + u.get('cache_read_input_tokens', 0))
        for c in m['message'].get('content', []):
            if c.get('type') == 'tool_use':
                i = c.get('input', {})
                arg = i.get('file_path') or i.get('command') or i.get('pattern') or i.get('skill') or ''
                print(f"{c['name']}: {str(arg)[:160]}")
    elif m.get('type') == 'result':
        result = m

if result is None:
    sys.exit('No result in the log: the session did not finish.')
u = result.get('usage', {})
print('\nDenied:', [d.get('tool_input', {}).get('command') or d.get('tool_input', {}).get('file_path')
                    for d in result.get('permission_denials', [])])
print(f"Duration {result.get('duration_ms', 0) / 1000:.0f} s · turns {result.get('num_turns')} · "
      f"input {u.get('input_tokens', 0)} + cache write {u.get('cache_creation_input_tokens', 0)} + "
      f"cache read {u.get('cache_read_input_tokens', 0)} · output {u.get('output_tokens', 0)} · "
      f"cost ${result.get('total_cost_usd', 0):.3f} · peak context {peak}")
print('\n' + (result.get('result') or ''))
