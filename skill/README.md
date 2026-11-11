# Translation skill

`SKILL.md` is the skill: translate or review WordPress strings into es_ES using `resources/` (glossary, style guide, quick reference). It must work with Sonnet (and later Haiku), not only Opus.

`scripts/po_tool.py` (Python stdlib) does the deterministic work so the model only decides translations:

| Command | What it does |
|---|---|
| `extract` | `.po` → numbered JSON lines |
| `glossary` / `tm` | Glossary entries / translation memory rows that apply to a file |
| `lint` | Review hints on the current translations: glossary terms missing or left in English, Title Case, «ej.», straight quotes |
| `check` | Placeholders, HTML, entities, URLs, newlines, edge spaces, quotes |
| `build` | Decisions → `corrected.po` (only changed strings) or full `.po` (`--full`), plus a Markdown report |
| `review-po` | All strings for the human reviewer in Poedit, proposals applied and fuzzy, with reason and original as comments |
| `finalize` | Human's saved file → `corrected.po` (only changed strings) and a learning report (kept, edited, reverted, missed) |
| `compare` | Compare two `.po` files by msgid (benchmark against human output) |

## How it is developed

A cheaper model session (Sonnet) does the translation and review work using only this skill. The Opus session that maintains the project audits its output against Nilo's feedback and updates the skill and `resources/`. The translator session never edits them; it reports what was unclear.

Benchmark: rounds 01 and 02 (in `/Volumes/Datos/scratch/wp-es-polyglots/rounds/`) have human-approved `corrected.po` files. Run the skill blind on copies of their `original.po` (outside the repo, so the answers are not visible) and compare with `po_tool.py compare`.
