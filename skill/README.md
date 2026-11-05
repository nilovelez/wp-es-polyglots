# Translation skill (planned)

A skill that takes "translate this into Spanish" (a `.po`, a list of strings or plain text) and produces the best possible es_ES translation using:

- `resources/glossary.csv` (its notes are mandatory),
- `resources/style-guide.md`,
- exact matches from the common strings `.po` and, if we decide so, `resources/translation-memory.csv`.

It must work with Sonnet or Haiku, not only Opus. Not started; see `docs/status.md`.
