# Translation skill

Development of the installable skill in `wordpress-translator-es/`. Its `SKILL.md` is written by hand there; `package.py` regenerates the rest (glossary, overrides, style guide, `po_tool.py`) from `resources/` and `scripts/`. Run it after every change and commit the result. The skill must work with cheap models (Haiku), not only Opus.

`scripts/po_tool.py` (Python stdlib) does the deterministic work so the model only decides translations:

| Command | What it does |
|---|---|
| `extract` | `.po` → numbered JSON lines |
| `fetch` | Download waiting or untranslated strings of a translate.wordpress.org project |
| `glossary-update` | Refresh the official glossary from translate.wordpress.org |
| `glossary` / `tm` | Glossary entries / translation memory rows (memory off for now) that apply to a file |
| `lint` | Review hints on the current translations: glossary terms missing or left in English, Title Case, «ej.», straight quotes |
| `check` | Placeholders, HTML, entities, URLs, newlines, edge spaces, quotes |
| `build` | Decisions → `corrected.po` (only changed strings) or full `.po` (`--full`), plus a Markdown report |
| `review-po` (training only) | All strings for the human reviewer in Poedit, proposals applied and fuzzy, with reason and original as comments |
| `finalize` (training only) | Human's saved file → `corrected.po` (only changed strings) and a learning report (kept, edited, reverted, missed) |
| `compare` (training only) | Compare two `.po` files by msgid (benchmark against human output) |

## How it is developed

A cheap model session (Haiku) does the translation and review work using only the installable skill, prompted as a real user would prompt it (see `review/README.md`, "Training sessions"). The Opus session that maintains the project audits its output against the reviewer's feedback and fixes the skill and `resources/`. The translator session never edits them; it reports what was unclear.

Benchmark: rounds 01 and 02 (in `rounds/`, not committed) have human-approved `corrected.po` files. Run the skill blind on copies of their `original.po` (outside the repo, so the answers are not visible) and compare with `po_tool.py compare`.
