# Review of waiting strings

Goal: clear the es_ES *waiting* queue fast, and learn from every round.

## Who does what

- **The reviewer** picks the project, reviews **every** string in Poedit (starting from the model's proposals), imports `corrected.po` in GlotPress and approves the rest. Only the reviewer uploads or approves.
- **Translator session** ("Traductor - Haiku" since round 06; "Traductor - Sonnet" before) reviews the strings using only the installable skill `wordpress-translator-es/`, as a user would (see "Training sessions"). It runs outside the repository and sees only the packaged plugin.
- **Maintainer session** (Opus) downloads the round, sends it to the translator, prepares the review file, builds `corrected.po` from the reviewer's saved file, and turns the differences into improvements of `resources/`, `skill/scripts/po_tool.py` and the skills' `SKILL.md` files.

## Training sessions: real use of the skill

The translator session must work exactly as a user of the installable skill would, with the same model a user would pick. It is not a subagent of the maintainer session: a subagent works inside the repository, gets this project's `CLAUDE.md` (which points to `resources/`) and can read `resources/` and other rounds, so it is not testing the skill (round 45, first try). Run it with `review/run_translator.sh`: a separate headless Claude Code session, in an empty sandbox folder outside the repository, with only the packaged plugin from `dist/`, no saved transcript and no auto-memory.

```
python3 skill/package.py
review/run_translator.sh <sandbox> "<what the user would say>" <log.jsonl>
python3 review/run_summary.py <log.jsonl>
```

Always use the same sandbox folder (the script empties it). The message is only what a user would say, in their words, without naming the skill or where it is, so the run also tests that the skill triggers:

- **Direct round**: "Revisa las cadenas en espera de <URL>".
- **Translation of an official project** the reviewer picks: "Traduce las cadenas sin traducir de este proyecto: <URL>".
- **Review of a file** (training round reviewed in Poedit, bench cases): pass the file as the fifth argument; the script copies it into the empty sandbox. "Revisa esta traducción: original.po".

Check the summary's tool list: the session must read only its skill and its work files. Then copy its work folder into `rounds/NN-<project>/` for the audit.

No lists of terms, exceptions or reminders in the prompt: if the session needs one to do the job right, it is missing from the skill or from `resources/`, and that is the finding of the round. The maintainer fixes it there (then `python3 skill/package.py`), not in the next prompt. The audit, the slicing into separate sessions for very large files and any `terms.md` the maintainer keeps are training machinery, not part of the skill.

## Round folders

Each round gets a folder `rounds/NN-<project>/` in the repository root, ignored by git: rounds are working material and are never committed. The reviewer opens and saves the round files there. What a round teaches goes into `skill/benchmark-log.md` and, when it is a rule, into `resources/`.

## Round

1. The reviewer picks a project in GlotPress, opens its waiting strings and passes the URL (any form works, filters included).
2. Maintainer downloads the waiting strings:
   ```
   python3 review/fetch_round.py <url>
   ```
   This creates `rounds/NN-<slug>-<subproject>/original.po`. Approved strings are not used as a reference (approved does not mean correct, and large projects have thousands); `--current` downloads them only for occasional analysis.
3. Translator runs the skill in review mode on the round folder → `decisions.jsonl`.
4. Maintainer builds the file for the reviewer in the round folder:
   ```
   python3 skill/scripts/po_tool.py review-po original.po decisions.jsonl review.po
   ```
   `review.po` has **all** waiting strings. Those with a proposal have it applied, are marked *fuzzy*, and carry translator comments: `[Corrección|Rechazo|DUDA] reason` and `Original: <translator's version>`.
5. The reviewer reviews every string in Poedit: accepts a proposal (clears *fuzzy*), restores the original text when the proposal is not needed, edits anything else, saves `review.po` in place and says it is done. No *fuzzy* may remain.
6. Maintainer copies the saved file to the round folder as `reviewed.po` and runs:
   ```
   python3 skill/scripts/po_tool.py finalize original.po decisions.jsonl reviewed.po corrected.po --report learning.md
   ```
   `corrected.po` holds only the strings the reviewer changed against the original.
7. The reviewer imports `corrected.po` at the same GlotPress URL (as PTE it replaces the waiting strings; he chooses approved or waiting) and approves the rest.
8. Maintainer reads `learning.md` and improves the skill:
   - **kept**: the model was right.
   - **reverted**: the model changed something that should have been approved → the "change only real errors" criteria.
   - **edited**: right idea, different wording.
   - **missed**: The reviewer changed something the model did not → a missing criterion, glossary note or lint check.
   Copies the round to the test bench as a new case (`bench/cases/`, see `bench/README.md`): `original.po`, `corrected.po` as `reference.po`, and a `case.md`.
   Asks the reviewer only when the reason for a change is not obvious. One case is a candidate; it becomes a rule when it repeats or when the guide or glossary say it. Logs the round in `skill/benchmark-log.md`.

The `polyglots` tool and Ollama are not part of this loop for now.

## Direct rounds (no Poedit review)

To clear the waiting queue, training rounds (above, with the reviewer's review in Poedit) alternate with direct rounds:

1. Fetch and cheap numbers; stop and ask the reviewer if it looks like a batch to reject whole.
2. The translator session reviews it as usual.
3. Opus audits the decisions instead of the reviewer: doubtful changes checked against the glossary, `glossary-overrides.csv` and the quick reference; term consistency across the whole file; `lint` hints left unanswered.
4. Doubts that the guide, glossary or quick reference do not settle: they go into `corrected.po` with the best proposal (the model's or Opus's), and to a list for the reviewer, by source text. Nothing is left out, because the reviewer approves everything else after importing.
5. `python3 review/audit_decisions.py <round> [--edits edits.jsonl] <n>=<reason> …` writes `audited.jsonl` (the model's decisions minus the dropped ones, with Opus's rewordings from `edits.jsonl`) and `audit.md`; `decisions.jsonl` stays as the model wrote it. `build original.po audited.jsonl corrected.po` gives `corrected.po` (only the strings to change), The reviewer imports it and approves the rest.

There is no human reference, so the round is logged in `skill/benchmark-log.md` as "sin revisión humana" and is not counted in the measurements. Whatever the reviewer notices later while approving becomes a candidate or a rule as usual.

## Large rounds

The skill stops before reviewing only when the precheck numbers point to a batch to reject whole, or when it has more than 7000 strings. Anything below that is reviewed straight away, in one session, and the precheck numbers go in the summary.

**One session, up to 7000 strings.** Measured with Haiku (rounds 38–46): the cache tokens read grow about in proportion to the size (2,000–3,500 per string, from 109 to 2505 strings), so a bigger batch does not cost more per string in any way that matters. The context peaked at 309,000 tokens with 2505 strings, about 40,000 plus 110 per string, so Haiku's 1,000,000-token window holds about 8000; the skills stop at 7000 for margin. Splitting into several sessions costs more, not less: every session reloads the skill and the guide (round 31, eight sessions of 600–700 strings: about 13 million cache tokens for about 3000 strings; round 43, one session: 7.4 million for 2505). Above 7000, split into as few sessions as possible, one after another, never in parallel: ten parallel Sonnet subagents on a 3053-string round burned most of a day's usage quota. Keep measuring: `review/run_summary.py` gives the peak, the tokens and the cost of each run.

## Batches to reject whole

Some batches must be rejected entirely instead of reviewed: machine translations without consistency, with hallucinations, ignoring the glossary and the style guide, and many strings just copied in English. Reviewing them string by string is a waste (round 05, torlann, 3053 strings, was one; its files were deleted so they are never reused).

Another case: the source strings are not in US English (Arcadys Municipal Core, a plugin written in Latin American Spanish, with the source copied as the es_ES translation). The plugin cannot be translated as it is: the whole batch is rejected and the person who submitted it is told that the original must be in US English. Detecting them automatically, before any model runs, is a requirement for the future review tools (see `docs/status.md`).

## Round folder

```
rounds/NN-project/
  original.po          waiting strings as downloaded
  entries.jsonl        extracted entries (skill)
  decisions.jsonl      translator decisions
  review.po            file for the reviewer (all strings, proposals fuzzy)
  reviewed.po          the reviewer's saved review.po
  corrected.po         only the strings the reviewer changed (what they import)
  learning.md          model vs the reviewer: kept, edited, reverted, missed
  audited.jsonl        direct rounds: decisions after the maintainer's audit
  edits.jsonl, audit.md  the audit's rewordings and the reasons for dropped decisions
  work/                the skill's own working files
```

Rounds 01 and 02 predate this flow: they have `repaired.po` (output of the `polyglots` tool), `corrected.po` and a one-off `make-corrected.py`.
