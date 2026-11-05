# Review of waiting strings

Goal: clear the es_ES *waiting* queue fast, and learn from every round.

## Who does what

- **Nilo** picks the project, gives feedback on the proposed changes, uploads `corrected.po` and approves the rest. Only Nilo uploads or approves.
- **Translator session** ("Traductor - Sonnet") reviews the strings using only `skill/SKILL.md` and `resources/`. It writes only in the round folder.
- **Maintainer session** (Opus) downloads the round, sends it to the translator, pre-checks its output, turns Nilo's feedback into changes in `resources/` and `skill/`, and logs the round.

## Round

1. Nilo gives the project URL, e.g. `https://translate.wordpress.org/projects/wp-plugins/<slug>/stable-readme/es/default/`.
2. Maintainer downloads it (no login needed):
   ```
   python3 review/fetch_round.py <project url>
   ```
   This creates `rounds/NN-<slug>-<subproject>/` with `original.po` (waiting) and `current.po` (approved, for consistency).
3. Translator runs the skill in review mode with the round folder as work folder: `decisions.jsonl`, `corrected.po` (only the strings to change) and `review.md` (table of decisions).
4. Maintainer pre-checks the decisions and gives Nilo a short list: proposed changes, doubts, anything suspicious.
5. Nilo gives feedback. The translator (or the maintainer) updates `decisions.jsonl` and rebuilds `corrected.po`.
6. Nilo uploads `corrected.po` (as PTE it replaces the waiting strings; he chooses approved or waiting) and approves the rest.
7. Maintainer turns the feedback into criteria (`resources/quick-reference.md`, style guide, glossary notes), skill changes or lint changes, and logs the round in `skill/benchmark-log.md`. Feedback on a single case is a candidate; it becomes a rule when it repeats or when the guide or glossary already say it.

The `polyglots` tool and Ollama are not part of this loop for now.

## Round folder

```
rounds/NN-project/
  original.po          waiting strings as downloaded
  current.po           approved strings of the project
  entries.jsonl        extracted entries (skill)
  decisions.jsonl      translator decisions, updated with Nilo's feedback
  corrected.po         only the strings to change (what Nilo uploads)
  review.md            table of decisions
  notes.md             round notes and Nilo's feedback (Spanish, optional)
```

Rounds 01 and 02 predate this flow: they also have `repaired.po` (output of the `polyglots` tool) and a one-off `make-corrected.py`.
