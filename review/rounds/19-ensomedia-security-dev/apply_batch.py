"""Turn a batch of edits into decisions.jsonl lines (one line per entry).

Usage: apply_batch.py <entries.jsonl> <batch.json> <decisions.jsonl>

batch.json: list of objects
  {"n": 12, "verdict": "fix|reject|doubt",
   "comment": "...",                       # Spanish, for the translator
   "replace": [["old", "new"], ...],       # applied to the current text
   "msgstr": "..."}                        # or a full replacement (optional)
The current text is the msgstr of the existing decision for that entry, if any,
otherwise the original msgstr. Every "old" must occur in the current text, or
nothing is written. An existing decision for the same entry is replaced.
"""
import json
import sys

entries_path, batch_path, out_path = sys.argv[1:4]

with open(entries_path, encoding="utf-8") as f:
    entries = {e["n"]: e for e in (json.loads(line) for line in f)}
with open(batch_path, encoding="utf-8") as f:
    batch = json.load(f)

decisions = {}
try:
    with open(out_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                decisions[d["n"]] = d
except FileNotFoundError:
    pass

errors = []
for item in batch:
    n = item["n"]
    e = entries[n]
    prev = decisions.get(n)
    base = prev if prev else e
    if "msgstr_plural" in e:
        texts = list(base.get("msgstr_plural", e["msgstr_plural"]))
    else:
        texts = [base.get("msgstr", e.get("msgstr", ""))]
    if "msgstr" in item:
        new = item["msgstr"]
        texts = new if isinstance(new, list) else [new]
    else:
        for old, rep in item.get("replace", []):
            hit = False
            for i in range(len(texts)):
                if old in texts[i]:
                    texts[i] = texts[i].replace(old, rep)
                    hit = True
            if not hit:
                errors.append(f"#{n}: '{old}' not found in current msgstr")
    out = {"n": n, "verdict": item["verdict"]}
    if "msgstr_plural" in e:
        out["msgstr_plural"] = texts
    else:
        out["msgstr"] = texts[0]
    out["comment"] = item["comment"] if not prev else (prev["comment"] + " " + item["comment"] if item["comment"] not in prev["comment"] else prev["comment"])
    if prev and prev.get("verdict") == "reject" and item["verdict"] == "fix":
        out["verdict"] = "reject"
    decisions[n] = out

if errors:
    print("\n".join(errors))
    sys.exit(1)

with open(out_path, "w", encoding="utf-8") as f:
    for n in sorted(decisions):
        f.write(json.dumps(decisions[n], ensure_ascii=False) + "\n")
print(f"{len(batch)} items applied; decisions file now has {len(decisions)} entries")
