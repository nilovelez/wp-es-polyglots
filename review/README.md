# Review of waiting strings

Goal: clear the es_ES *waiting* queue fast, and learn from every round.

## Who does what

- **The reviewer** picks the project, reviews **every** string in Poedit (starting from the model's proposals), imports `corrected.po` in GlotPress and approves the rest. Only the reviewer uploads or approves.
- **Translator session** ("Traductor - Haiku" since round 06; "Traductor - Sonnet" before) reviews the strings using only the base plugin `wordpress-translator-es/`, as a user would (see "Training sessions"). It runs outside the repository and sees only the packaged plugin.
- **Maintainer session** (Opus) plays the workflow (downloads the round with `glotpress.py prepare`, stops on a batch to reject whole), sends the `.po` to the translator, prepares the review file, builds `corrected.po` from the reviewer's saved file, and turns the differences into improvements of `resources/`, `skill/scripts/po_tool.py` and the skills' `SKILL.md` files.

## Training sessions: real use of the skill

The translator session must work exactly as a user of the installable skill would, with the same model a user would pick. It is not a subagent of the maintainer session: a subagent works inside the repository, gets this project's `CLAUDE.md` (which points to `resources/`) and can read `resources/` and other rounds, so it is not testing the skill (round 45, first try). Run it with `review/run_translator.sh`: a separate headless Claude Code session, in an empty sandbox folder outside the repository, with only the packaged plugin from `dist/`, no saved transcript and no auto-memory.

```
python3 skill/package.py
review/run_translator.sh <sandbox> "<what the user would say>" <log.jsonl>
python3 review/run_summary.py <log.jsonl>
```

Always use the same sandbox folder (the script empties it). The message is only what a user would say, in their words, without naming the skill or where it is, so the run also tests that the skill triggers:

- **Review**: "Revisa esta traducción: <name>.po", with the file `glotpress.py prepare` wrote as the fifth argument (the script copies it into the empty sandbox).
- **Translation of an official project** the reviewer picks: `glotpress.py prepare <url> --translate`, then "Traduce este archivo: <name>.po".
- **Workflow test** (now and then, not every round): `WORKFLOW=1` also loads `wordpress-polyglots-es`, and the message is the URL as a moderator would give it ("Revisa las cadenas en espera de <URL>").

`review/run_round.sh <sandbox> <NN-slug> "<message>" [file]` runs the session, copies the sandbox into `rounds/NN-slug/` and prints the summary; `python3 review/inspect_round.py rounds/NN-slug` lists its tool calls, errors and decisions.

Check the summary's tool list: the session must read only its skill and its work files. Then copy its work folder into `rounds/NN-<project>/` for the audit.

No lists of terms, exceptions or reminders in the prompt: if the session needs one to do the job right, it is missing from the skill or from `resources/`, and that is the finding of the round. The maintainer fixes it there (then `python3 skill/package.py`), not in the next prompt. The audit, the slicing into separate sessions for very large files and any `terms.md` the maintainer keeps are training machinery, not part of the skill.

## Round folders

Each round gets a folder `rounds/NN-<project>/` in the repository root, ignored by git: rounds are working material and are never committed. The reviewer opens and saves the round files there. What a round teaches goes into `skill/benchmark-log.md` and, when it is a rule, into `resources/`.

## Round

1. The reviewer picks a project in GlotPress, opens its waiting strings and passes the URL (any form works, filters included).
2. Maintainer downloads the waiting strings in a new round folder, as the workflow does:
   ```
   mkdir rounds/NN-<project> && cd rounds/NN-<project>
   python3 ../../skill/scripts/glotpress.py prepare <url>
   ```
   This writes `<name>.po` and `<name>-precheck.txt`, or STOPs on a batch to reject whole. Approved strings are never downloaded (approved does not mean correct).
3. Translator runs the `review` skill on `<name>.po` → `decisions.jsonl` in its work folder.
4. Maintainer builds the file for the reviewer in the round folder:
   ```
   python3 skill/scripts/dev_tools.py review-po original.po decisions.jsonl review.po
   ```
   `review.po` has **all** waiting strings. Those with a proposal have it applied, are marked *fuzzy*, and carry translator comments: `[Corrección|Rechazo|DUDA] reason` and `Original: <translator's version>`.
5. The reviewer reviews every string in Poedit: accepts a proposal (clears *fuzzy*), restores the original text when the proposal is not needed, edits anything else, saves `review.po` in place and says it is done. No *fuzzy* may remain.
6. Maintainer copies the saved file to the round folder as `reviewed.po` and runs:
   ```
   python3 skill/scripts/dev_tools.py finalize original.po decisions.jsonl reviewed.po corrected.po --report learning.md
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
3. Opus audits the decisions instead of the reviewer: doubtful changes checked against the glossary, `glossary-overrides.csv` and the style guide; term consistency across the whole file. The resources are the only yardstick: every dropped or reworded decision must cite the rule that justifies it (a glossary entry, an override, a section of the guide, or an explicit decision of the reviewer). With no rule to cite, the model's decision stands; at most it goes to the reviewer as a doubt. The auditor's own taste is never a reason: an original that "sounds fine" is not a valid alternative if the resources say otherwise (rounds 114, 128 and 129 dropped correct «Lo siento» changes on a rule that did not exist). Judging what the resources do not cover belongs to training rounds.
4. Doubts that the guide, its exceptions or the glossary do not settle: they go into `corrected.po` with the best proposal (the model's or Opus's), and to a list for the reviewer, by source text. Nothing is left out, because the reviewer approves everything else after importing.
5. `python3 review/audit_decisions.py <round> [--edits edits.jsonl] <n>=<reason> …` (each reason names its source, such as `glossary: sorry = lo siento` or `guide: 3.2`) writes `audited.jsonl` (the model's decisions minus the dropped ones, with Opus's rewordings from `edits.jsonl`) and `audit.md`; `decisions.jsonl` stays as the model wrote it. `build original.po audited.jsonl corrected.po` gives `corrected.po` (only the strings to change), The reviewer imports it and approves the rest.

There is no human reference, so the round is logged in `skill/benchmark-log.md` as "sin revisión humana" and is not counted in the measurements. Whatever the reviewer notices later while approving becomes a candidate or a rule as usual.

## Large rounds

The workflow (`glotpress.py prepare`) stops before reviewing only when the precheck numbers point to a batch to reject whole, and splits the file when it does not fit in one session. Anything else is reviewed straight away, in one session, and the precheck numbers go in the summary.

**One session whenever it fits.** `glotpress.py size` (also the last line of `precheck`) estimates the worst-case peak context of the whole job and gives the entry ranges to split it into when it does not fit in 85% of the context window. The estimate is measured on Haiku sessions (rounds 38–48, peak context per turn): about 55,000 tokens of base (what an isolated session holds before the first block: system, skill, guide, glossary) plus 0.46 tokens per byte of `entries.jsonl` read plus 1.07 per byte of decisions written. The decisions are not known before starting, so a review assumes a bad batch (decisions of 60% of the entries' bytes, the worst measured, round 39) and a translation 120% (110% measured in round 48). Measured against it: round 46 (review, 1635 strings), estimate 378,000, real 300,000; round 48 (translation, 1018 strings), estimate 291,000, real 181,000; round 47 (review, 90 strings), estimate 76,000, real 73,000. The gap is the unknown decisions, not the per-byte numbers: with its real decisions, round 46 would be estimated at 226,000, short of the real 300,000, so they are not lowered. With a 1,000,000-token window that is several thousand UI strings; long strings (readmes) fill it sooner. Context windows by model and surface: Claude Help Center, "How large is the context window on paid Claude plans?".

Splitting a job that fits costs more, not less: every session reloads the skill and the guide (round 31, eight sessions of 600–700 strings: about 13 million cache tokens for about 3000 strings; round 43, one session: 7.4 million for 2505). When it does not fit, use as few sessions as `size` gives, one after another, never in parallel: ten parallel Sonnet subagents on a 3053-string round burned most of a day's usage quota. Keep measuring: `review/run_summary.py` prints the peak context of each run; compare it with the estimate and adjust the numbers in `size_estimate` when they drift.

## Training rounds and production rounds

Every round is one of two kinds; if it is not clear which, ask before the audit.

- **Training round**: the point is to improve the skill (a change in how it decides, calibrating `size`, a new kind of file), so every detail counts. The message to the session asks for the reasons, as a user would («…y explícame el motivo de cada cambio»), so each change carries one and the audit can check that the rules are applied right. The maintainer may spend on the audit: all the decisions on a small round, a sample on a large one (about 30 at random plus everything `check` flags, and the model's doubts), reading the plugin's code when a doubt depends on it.
- **Production round** (a direct review to clear the backlog): fast, cheap and reliable. The message asks only for the review, so changes carry no reasons; the session asks about the doubts, and the doubts are what may need adding to the glossary or the guide. Haiku in an isolated session, the automatic checks and a small sample. The whole file is read only when the sample finds several real errors. Report the error rate of the sample with the file.

## Batches to reject whole

Some batches must be rejected entirely instead of reviewed: machine translations without consistency, with hallucinations, ignoring the glossary and the style guide, and many strings just copied in English. Reviewing them string by string is a waste (round 05, torlann, 3053 strings, was one; its files were deleted so they are never reused).

Another case: the source strings are not in US English (Arcadys Municipal Core, a plugin written in Latin American Spanish, with the source copied as the es_ES translation). The plugin cannot be translated as it is: the whole batch is rejected and the person who submitted it is told that the original must be in US English. Detecting them automatically, before any model runs, is a requirement for the future review tools (see `docs/status.md`).

## Round folder

```
rounds/NN-project/
  <name>.po            waiting strings as downloaded (glotpress.py prepare)
  <name>-precheck.txt  precheck numbers
  run.jsonl            translator session log
  <name>-work/         the skill's working files: original.po, entries*.md, decisions.jsonl
  <name>-corrected.po  the skill's output
  review.po            file for the reviewer (all strings, proposals fuzzy)
  reviewed.po          the reviewer's saved review.po
  corrected.po         only the strings the reviewer changed (what they import)
  learning.md          model vs the reviewer: kept, edited, reverted, missed
  audited.jsonl        direct rounds: decisions after the maintainer's audit
  edits.jsonl, audit.md  the audit's rewordings and the reasons for dropped decisions
```

Rounds 01 and 02 predate this flow: they have `repaired.po` (output of the `polyglots` tool), `corrected.po` and a one-off `make-corrected.py`.
