import json
import sys

path, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
with open(path, encoding="utf-8") as f:
    entries = [json.loads(line) for line in f]
for e in entries:
    if first <= e["n"] <= last:
        if "msgid_plural" in e:
            print(f"{e['n']} | {e['msgid']} / {e['msgid_plural']}")
            for i, s in enumerate(e.get("msgstr_plural", [])):
                print(f"   [{i}] => {s}")
        else:
            print(f"{e['n']} | {e['msgid']}")
            print(f"   => {e.get('msgstr', '')}")
