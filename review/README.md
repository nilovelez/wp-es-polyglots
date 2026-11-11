# Review of waiting strings

Goal: clear the es_ES *waiting* queue fast, and learn from every round.

## Who does what

- **The reviewer** picks the project, reviews **every** string in Poedit (starting from the model's proposals), imports `corrected.po` in GlotPress and approves the rest. Only the reviewer uploads or approves.
- **Translator session** ("Traductor - Haiku" since round 06; "Traductor - Sonnet" before) reviews the strings using only the installable skill `wordpress-translator-es/`, as a user would (see "Training sessions"). It writes only in the round folder, temporary files included.
- **Maintainer session** (Opus) downloads the round, sends it to the translator, prepares the review file, builds `corrected.po` from the reviewer's saved file, and turns the differences into improvements of `resources/`, `skill/scripts/po_tool.py` and `wordpress-translator-es/SKILL.md`.

## Training sessions: real use of the skill

The translator session must work exactly as a user of the installable skill would, with the same model a user would pick. Its prompt says only what a user would say:

```
Use the skill in <repo>/wordpress-translator-es (read its SKILL.md and follow it).
Review rounds/NN-<project>/original.po [entries A to B], work folder rounds/NN-<project>/work/,
decisions in work/dec_<slice>.jsonl.
```

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
4. Doubts that the guide, glossary or quick reference do not settle: the string stays as it was (no change) and goes to a list for the reviewer.
5. `python3 review/audit_decisions.py <round> [--edits edits.jsonl] <n>=<reason> …` writes `audited.jsonl` (the model's decisions minus the dropped ones, with Opus's rewordings from `edits.jsonl`) and `audit.md`; `decisions.jsonl` stays as the model wrote it. `build original.po audited.jsonl corrected.po` gives `corrected.po` (only the strings to change), The reviewer imports it and approves the rest.

There is no human reference, so the round is logged in `skill/benchmark-log.md` as "sin revisión humana" and is not counted in the measurements. Whatever the reviewer notices later while approving becomes a candidate or a rule as usual.

## Large rounds

Before any model review of a large round (more than ~400 strings), give the reviewer the cheap numbers first (`lint` count, strings identical to English, untranslated) so they can look at the originals and decide whether the batch deserves a review at all.

Files that do deserve it are reviewed in slices with `--range A-B` (`extract`, `glossary`, `lint`). Do **not** fan out to many parallel subagents on the same model: a 3053-string round reviewed by ten parallel Sonnet subagents burned most of a day's usage quota. Process the slices one after another in the translator session, or delegate slices to a cheaper model.

Measured with Haiku (rounds 11–13): up to ~900 UI strings fit in one pass with no drop in quality at the end. Larger files (rounds 31–33): one Haiku session per slice of ~600–700 entries, one after another, each told only its entry range, with decisions in `work/dec_<slice>.jsonl`; the maintainer audits each slice before starting the next one and joins them into `decisions.jsonl`. Before building `review.po`, check the final translations for terms that ended up inconsistent across slices and get the reviewer's decision on them (round 13: «autenticación» vs «identificación»), so they do not review the same strings twice.

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
  work/                per-slice decisions and the skill's own working files
```

Rounds 01 and 02 predate this flow: they have `repaired.po` (output of the `polyglots` tool), `corrected.po` and a one-off `make-corrected.py`.
