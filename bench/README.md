# Test bench

Reference cases to measure the base skills `review` and `translate` (`wordpress-translator-es/skills/`) and to compare them with other translation skills on the same input. Every case has a human reference: a reviewer of the locale checked every string. The strings come from translate.wordpress.org (GPL).

Old rounds are not used: the bench starts from rounds reviewed by a human after 2026-11-11.

## Cases

```
cases/NN-<slug>-<sub-project>/
  original.po    input exactly as downloaded (waiting strings, or strings to translate)
  reference.po   the reviewer's result
  case.md        mode, project and URL, date, size, what the case covers
```

- **Review cases:** `reference.po` holds only the strings the reviewer changed, the way they would import it. Strings not in it were approved as they were.
- **Translation cases:** `reference.po` is the full translation after the reviewer's review.

Aim for a mix: batches with typical errors (glossary synonyms, «usted», wrong meaning, capitals, placeholders), good batches where the right answer is to change almost nothing (they measure over-correction), translations of official projects (core, Meta, popular plugins), and different sizes.

A case is never edited after it is added. If a reference turns out to be wrong, fix it in a new case version (`NN-…-v2`) and say why in its `case.md`.

## Running the bench

For each case, in a fresh session with the model under test, prompt exactly as a user would:

```
Use the skill in wordpress-translator-es/skills/review (read its SKILL.md and follow it).
Review bench/cases/<case>/original.po. Work folder: <tmp>/<case>/. Write the result to <tmp>/<case>/corrected.po.
```

(For translation cases: the `translate` skill, "Translate …" and `translated.po`.) Do not add hints, term lists or exceptions: the bench measures the skill as people get it. Then:

```
python3 skill/scripts/po_tool.py compare bench/cases/<case>/reference.po <tmp>/<case>/corrected.po
```

- **found**: strings the reviewer changed that the skill changed too (and how many with the same wording).
- **only in reference**: changes the skill missed.
- **only in candidate** / **extra**: changes the skill made that the reviewer did not (over-correction, or a reviewer miss worth a look).

Log every run in `results.md`: date, skill commit, model, and the numbers per case. Run the whole bench after a batch of skill changes, not after every change.
