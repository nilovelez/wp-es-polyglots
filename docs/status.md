# Status

Last updated: 2026-11-05.

## Current milestone

**M2 – Skill-driven review rounds.** A Sonnet session ("Traductor - Sonnet") translates and reviews using only `skill/`; the Opus session audits and improves the skill. Steps:

1. Write `skill/SKILL.md` and `skill/scripts/po_tool.py`. Done.
2. Blind benchmark on rounds 01 and 02 against the human-approved `corrected.po`. Done: 9/26 with skill v1, 39/50 with v2; v3 adds `lint` (see `skill/benchmark-log.md`).
3. Real rounds from the waiting queue with Nilo's feedback, following `review/README.md`. In progress.

M1 (reorganize the repository and document the current state) is done.

## Subprojects

### review (top priority)

- Two rounds done: `01-mailbridgeapi` (readme, 72 strings) and `02-wgrank` (readme, 161 strings).
- Each round keeps `original.po`, `repaired.po` (tool output), `corrected.po` (only the strings to change) and the script that built it.
- The `corrected.po` was built with a one-off Python script per round. A reusable script is a candidate for M2.

### polyglots

- Rules: `polyglots/rules/es_ES.yaml`, 44 mistakes and 33 patterns, guidance at 1444 / 1500 characters. Tests pass (21 cases).
- Calibration log covers rounds 1 and 2.
- Local models: Ollama quality is not good enough yet for unsupervised translation; usable for pre-translation. Comparison material in `polyglots/local-models/` (empty Visualizer `.po` and a Haiku reference translation **not approved by a human**). Better: export one or two approved es projects, empty them and measure against them (glossary, informal register, placeholders, exact match).
- `polyglots` and Ollama run on Marcianito; this repository lives on Bender, where they are not installed.

### skill

- First version of `skill/SKILL.md` (review and translation modes) and `skill/scripts/po_tool.py`. Scripts verified: rebuilding both rounds' `corrected.po` from decisions gives identical files.
- Translation memory is off in the skill until decided.

### common strings (separate repository)

- Not started here. Nilo has an older project (MySQL, themes only) with database dumps and a list of the most common strings. Plan: redo it for core, plugins and themes, drop strings whose translation depends on context (e.g. *Red* → «rojo» / «roja»), and produce a `.po` of common strings to be applied before any translation. Only that `.po` will come to this repository.

## Open questions (locale)

- «Escritorio» with a capital letter mid-sentence: confirm the es_ES core convention.
- *Dashboard* of an external service: «escritorio» per the glossary, or a different wording?
- *authentication salt* (AUTH_SALT): how does core translate it?
- *Deselect All*: the glossary gives «anular selección»; «Anular toda la selección»?
- Plugin name with a subtitle (WGRank Translate – …): leave untranslated?
- Glossary typos (QuickPress, *deprecate*, *expire*, *expanse*, *troubleshooting*, duplicated *endpoint* and *page*): Nilo will review them.
- Translation memory: `resources/translation-memory.csv` has 21 entries from WGRank, but the previous instructions said to keep it empty because it will be approached differently. Waiting for a decision.
