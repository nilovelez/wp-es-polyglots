# polyglots tool tuning

The [`polyglots`](https://ada.tools) tool downloads waiting strings and reviews them with rules and, optionally, an AI model (frontier or local through Ollama). It **never uploads or approves anything**.

It runs on Marcianito (Windows 11, 32 GB RAM, RTX 2060 12 GB; working folder `Z:\polyglots`). Candidate local models: `gemma4:12b`, `gemma4:e4b-it-qat`, `translategemma:12b`; context ≥ 8192; check 100 % GPU with `ollama ps`.

## Commands

- `polyglots fetch <url> --get waiting [--out-dir <folder>] [--no-ai]`: download and review. Without `--get` it also downloads untranslated strings.
- `polyglots review <file>.po --locale es_ES [--no-ai]`, `polyglots translate`, `polyglots rules check --file <yaml>`, `polyglots config`, `polyglots doctor`.
- Local drafts: `--draft-engine local --local-model <model>`. Local review is experimental (do not enable `reviewProvider local`).
- Check `polyglots <command> --help` when in doubt: part of this list comes from public docs and may be outdated.

## Rules file

`rules/es_ES.yaml` is **generated**; do not edit it by hand.

```
python3 polyglots/rules/build_rules.py
```

It combines `rules/es_ES.base.yaml` (export from the tool's rules generator) with the `M` (mistakes) and `P` (patterns) lists in the script, and checks the limits: `guidance` ≤ 1500 characters, `capitalization` ≤ 2500, `register` ≤ 500.

Tests:

```
node polyglots/rules/tests/newtest.js polyglots/rules/es_ES.yaml
node polyglots/rules/tests/evalrules.js polyglots/rules/es_ES.yaml review/rounds/02-wgrank/original.po
```

`newtest.js` runs hit and false-positive cases; `evalrules.js` counts hits per rule on a real `.po`. Validate with `polyglots rules check --file es_ES.yaml` on Marcianito before delivering.

## Calibration

`calibration-log.md` (Spanish): one entry per round with what the tool caught, missed and got wrong. Used to tune the rules and to compare local models.

`local-models/`: material to compare local models.
