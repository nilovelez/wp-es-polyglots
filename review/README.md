# Review of waiting strings

Goal: clear the es_ES *waiting* queue fast, and learn from every round.

## Who does what

- **Nilo** picks the project, reviews **every** string in Poedit (starting from the model's proposals), imports `corrected.po` in GlotPress and approves the rest. Only Nilo uploads or approves.
- **Translator session** ("Traductor - Haiku" since round 06; "Traductor - Sonnet" before) reviews the strings using only `skill/SKILL.md` and `resources/`. It writes only in the round folder, temporary files included.
- **Maintainer session** (Opus) downloads the round, sends it to the translator, prepares the review file, builds `corrected.po` from Nilo's saved file, and turns the differences into improvements of `resources/` and `skill/`.

## Exchange folder

`/Volumes/Datos/scratch/wp-es-polyglots/` on Bender, mounted on Nilo's machines through Tailscale. Each round gets a subfolder `NN-<project>/` there with the files Nilo opens and saves. The canonical copy of every round lives in `review/rounds/NN-<project>/` in this repository.

## Round

1. Nilo picks a project in GlotPress, opens its waiting strings and passes the URL (any form works, filters included).
2. Maintainer downloads the waiting strings:
   ```
   python3 review/fetch_round.py <url>
   ```
   This creates `rounds/NN-<slug>-<subproject>/original.po`. Approved strings are not used as a reference (approved does not mean correct, and large projects have thousands); `--current` downloads them only for occasional analysis.
3. Translator runs the skill in review mode on the round folder → `decisions.jsonl`.
4. Maintainer builds the file for Nilo and copies it to the exchange folder:
   ```
   python3 skill/scripts/po_tool.py review-po original.po decisions.jsonl review.po
   ```
   `review.po` has **all** waiting strings. Those with a proposal have it applied, are marked *fuzzy*, and carry translator comments: `[Corrección|Rechazo|DUDA] reason` and `Original: <translator's version>`.
5. Nilo reviews every string in Poedit: accepts a proposal (clears *fuzzy*), restores the original text when the proposal is not needed, edits anything else, saves `review.po` in place and says it is done. No *fuzzy* may remain.
6. Maintainer copies the saved file to the repository as `reviewed.po` and runs:
   ```
   python3 skill/scripts/po_tool.py finalize original.po decisions.jsonl reviewed.po corrected.po --report learning.md
   ```
   `corrected.po` holds only the strings Nilo changed against the original; it goes back to the exchange folder.
7. Nilo imports `corrected.po` at the same GlotPress URL (as PTE it replaces the waiting strings; he chooses approved or waiting) and approves the rest.
8. Maintainer reads `learning.md` and improves the skill:
   - **kept**: the model was right.
   - **reverted**: the model changed something that should have been approved → the "change only real errors" criteria.
   - **edited**: right idea, different wording.
   - **missed**: Nilo changed something the model did not → a missing criterion, glossary note or lint check.
   Asks Nilo only when the reason for a change is not obvious. One case is a candidate; it becomes a rule when it repeats or when the guide or glossary say it. Logs the round in `skill/benchmark-log.md`.

The `polyglots` tool and Ollama are not part of this loop for now.

## Large rounds

Before any model review of a large round (more than ~400 strings), give Nilo the cheap numbers first (`lint` count, strings identical to English, untranslated) so he can look at the originals and decide whether the batch deserves a review at all.

Files that do deserve it are reviewed in slices with `--range A-B` (`extract`, `glossary`, `lint`). Do **not** fan out to many parallel subagents on the same model: a 3053-string round reviewed by ten parallel Sonnet subagents burned most of a day's usage quota. Process the slices one after another in the translator session, or delegate slices to a cheaper model.

## Batches to reject whole

Some batches must be rejected entirely instead of reviewed: machine translations without consistency, with hallucinations, ignoring the glossary and the style guide, and many strings just copied in English. Reviewing them string by string is a waste (round 05, torlann, 3053 strings, was one; its files were deleted so they are never reused). Detecting them automatically, before any model runs, is a requirement for the future review tools (see `docs/status.md`).

## Round folder

```
rounds/NN-project/
  original.po          waiting strings as downloaded
  entries.jsonl        extracted entries (skill)
  decisions.jsonl      translator decisions
  review.po            file for Nilo (all strings, proposals fuzzy)
  reviewed.po          Nilo's saved review.po
  corrected.po         only the strings Nilo changed (what he imports)
  learning.md          model vs Nilo: kept, edited, reverted, missed
```

Rounds 01 and 02 predate this flow: they have `repaired.po` (output of the `polyglots` tool), `corrected.po` and a one-off `make-corrected.py`.
