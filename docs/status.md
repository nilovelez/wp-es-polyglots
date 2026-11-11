# Status

Last updated: 2026-11-11.

## Current milestone

**M2 – Skill-driven review rounds.** A cheaper model session translates and reviews using only the installable skill ("Traductor - Sonnet" for rounds 03–04, "Traductor - Haiku" from round 06 on, measured round by round in `skill/benchmark-log.md`); the Opus session audits and improves the skill. Steps:

1. Write the skill and `skill/scripts/po_tool.py`. Done.
2. Blind benchmark on rounds 01 and 02 against the human-approved `corrected.po`. Done: 9/26 with skill v1, 39/50 with v2; v3 adds `lint` (see `skill/benchmark-log.md`).
3. Real rounds from the waiting queue with the reviewer's feedback, following `review/README.md`. In progress.
4. Installable skill `wordpress-translator-es/` (2026-11-11): the core component, translate or review with the glossary and the style guide, nothing else. `skill/package.py` regenerates it from `resources/` and `po_tool.py`; run it and commit after every change. The reviewer tests it in separate sessions with cheap models and compares it with other moderators' skills; what they learned is merged into it. Since round 34 the training rounds use only this skill, prompted as a real user would (no term lists or exceptions in the prompt); the development `skill/SKILL.md` was removed.

M1 (reorganize the repository and document the current state) is done.

## Plan: shared sources for every tool

Goal: every tool (a translation skill, a review skill for moderators, an AI agent that pre-reviews incoming translations) uses the same sources: the official translator guide and the official glossary. The skill keeps only the file tools (`po_tool.py`) and the workflows (translate, review), never its own translation rules.

What a skill or workflow may carry is fine-tuning for its scenario: how strict to be depending on what is being translated or reviewed. For example, changelogs allow more tolerance; a plugin's main file needs more care; WordPress core needs much more care. The "Cuándo cambiar una cadena" section of `resources/quick-reference.md` is this kind of rule and belongs in the review workflow, not in the guide. These are examples, to be adapted: the tuning is what the rounds teach us. It also covers how to run the work, such as the size from which slices or subagents make sense and the size that is too big for one pass (`review/README.md`, "Large rounds"). It depends on the agent: Claude with a small or a large model, or a local model with Ollama, will each need different tuning.

**Translator guide**

1. The reviewer reviews by hand the guide published in the es handbook and `resources/style-guide.md` (inherited: based on the official guide, more complete, with more cases). They report inconsistencies; Claude fixes them in the Markdown.
2. Two versions with the same rules, more complete and better explained than the published one:
   - **Human guide** (HTML): replaces the current page in the es handbook; the reviewer publishes it. Claude creates it when the reviewer asks. It links to the agent guide.
   - **Agent guide** (Markdown): the same rules plus the information for agents; it goes to the WordPress España community's GitHub account.
3. The skill then references the published agent guide instead of carrying rules.
4. From then on, new criteria from the rounds are reviewed one by one as changes to that base.

**Glossary**

- The glossary is the GlotPress glossary that moderators edit; `resources/glossary.csv` is its CSV export. Do not edit it by hand.
- Exceptions found in the rounds live in `resources/glossary-overrides.csv`, and every exception and every change to propose is recorded in `resources/proposals.md`. The reviewer proposes them in GlotPress; once published, the export is refreshed and the local exception removed.
- The more the guide and the glossary hold, the fewer local exceptions: the end state is no exceptions at all.

**Later: central Polyglots repository**

A central WordPress Polyglots repository (not the es one) with the general instructions on how agents must work and the agent guide of each locale. Any skill or tool of any locale then uses the general Polyglots guide plus its locale's agent guide, instead of each one interpreting the rules its own way. This repository must stay clonable by other locales for that reason.

## Subprojects

### review (top priority)

- 33 rounds so far (log in `skill/benchmark-log.md`): training rounds with the reviewer's review in Poedit, and direct rounds audited by Opus to clear the queue. Round folders live in the ignored `rounds/` folder and are never committed.
- Some batches are rejected whole (round 05, torlann: unchecked machine translation; others logged in the benchmark log).

### Future requirement: detect batches to reject whole

When a contributor uploads a batch like torlann (machine translation without consistency, hallucinations, glossary and style guide ignored, many strings copied in English), the tools must flag it and recommend rejecting it **before** spending a model review. Candidate signals, all cheap scripts: share of strings identical to the source, `lint` hints per string, formal register («usted»), inconsistent translations of the same source term, length ratios. Not for the current stage.

### polyglots

- Rules: `polyglots/rules/es_ES.yaml`, 44 mistakes and 33 patterns, guidance at 1444 / 1500 characters. Tests pass (21 cases).
- Calibration log covers rounds 1 and 2.
- Local models: Ollama quality is not good enough yet for unsupervised translation; usable for pre-translation. Comparison material in `polyglots/local-models/` (empty Visualizer `.po` and a Haiku reference translation **not approved by a human**). Better: export one or two approved es projects, empty them and measure against them (glossary, informal register, placeholders, exact match).
- `polyglots` and Ollama may run on a different machine from this repository (a GPU is needed for local models).

### skill

- One skill: `wordpress-translator-es/` (installable), developed from `skill/` and `resources/` with `skill/package.py`. It refreshes the official glossary at the start (`glossary-update`) and applies the team's overrides on top.
- Not yet tested on claude.ai (network access to translate.wordpress.org from its sandbox) or on Windows.
- `po_tool.py` still has es-specific checks (locale code, Spanish quotes, «ej.»); they must move to locale data before another locale can use it.
- Translation memory is off in the skill until decided.

### common strings (separate repository)

- Not started here. The reviewer has an older project (MySQL, themes only) with database dumps and a list of the most common strings. Plan: redo it for core, plugins and themes, drop strings whose translation depends on context (e.g. *Red* → «rojo» / «roja»), and produce a `.po` of common strings to be applied before any translation. Only that `.po` will come to this repository.

## Open questions (locale)

- «Escritorio» with a capital letter mid-sentence: confirm the es_ES core convention.
- *Dashboard* of an external service: «escritorio» per the glossary, or a different wording? Round 10: the reviewer accepted «escritorio del vendedor» for ifthenpay's merchant dashboard (one case, not yet a rule).
- *authentication salt* (AUTH_SALT): how does core translate it?
- *Deselect All*: the glossary gives «anular selección»; «Anular toda la selección»?
- Plugin name with a subtitle (WGRank Translate – …): leave untranslated?
- Official glossary entries the team overrides (`resources/glossary-overrides.csv`, used by `po_tool.py`): *meta title* / *meta description* («meta título» / «meta descripción»). The reviewer may want to change them in the official glossary.
- Glossary typos (QuickPress, *deprecate*, *expire*, *expanse*, *troubleshooting*, duplicated *endpoint* and *page*): the reviewer will review them.
- Translation memory: `resources/translation-memory.csv` has 21 entries from WGRank, but the previous instructions said to keep it empty because it will be approached differently. Waiting for a decision.
