# Translation skills

Development of the two installable plugins. `SKILL.md` files are written by hand in the plugin folders; `package.py` regenerates the rest from `resources/` and `scripts/`. Run it after every change and commit the result. The skills must work with cheap models (Haiku), not only Opus.

## Architecture

| Layer | Where | What |
|---|---|---|
| Base skills | `wordpress-translator-es/` (`translate`, `review`) | A `.po` in, a `.po` out. Each skill folder is self-contained (the same folder for Claude Code and claude.ai) and carries the whole style guide, the whole glossary (official glossary with the team's overrides merged in, as `glossary.md`) and `po_tool.py`. The model reads the guide and the glossary whole and decides; the script only handles the file. No other rules, no downloads, no workflow. |
| Workflow | `wordpress-polyglots-es/` (`review-glotpress-waiting`, `translate-glotpress-project`) | For es_ES moderators, on top of the base skills: download from translate.wordpress.org, precheck (batches to reject whole), split files too large for one session, import URL. Then it hands the `.po` to a base skill. |
| Repository | `resources/`, `skill/`, `review/` | Sources (guide, glossary export, overrides), packaging, training rounds and their tools. Never installed. |

Training rounds improve the guide and the glossary, so the base skills need nothing else.

## Scripts (`scripts/`, Python stdlib)

**`po_tool.py`**: base skills (copied into each one's `references/`).

| Command | What it does |
|---|---|
| `start` | Work folder and entries file (cut into parts only when over one Read); prints the exact steps: read the whole guide, the whole glossary and the entries at once, write the decisions, `finish` |
| `finish` | Builds the final `.po` next to where `start` ran, checks it and says what to fix or that it is done |
| `extract` | `.po` → numbered JSON lines (used by `start`) |
| `check` | Placeholders, HTML, entities, URLs, newlines, edge spaces, final punctuation, length, quotes |
| `build` | Decisions → `corrected.po` (only changed strings) or full `.po` (`--full`), plus a Markdown report |

**`glotpress.py`**: workflow (copied into each workflow skill's `scripts/`, with `po_tool.py` and the merged `glossary.csv`).

| Command | What it does |
|---|---|
| `prepare` | Download, precheck and STOP on a batch to reject whole (review), split into `<name>-partK.po` if it does not fit in one session; says which base skill to use on which file, and the import URL |
| `fetch` | Download waiting or untranslated strings of a translate.wordpress.org project |
| `precheck` | Cheap numbers on a waiting batch (see `review/README.md`, "Batches to reject whole") |
| `size` | Worst-case peak context of one session; entry ranges if it does not fit |
| `lint` | Hints on current translations, counted by the precheck |

**`dev_tools.py`**: repository only.

| Command | What it does |
|---|---|
| `glossary-update` | Refresh `resources/glossary.csv` from translate.wordpress.org when the reviewer says the official glossary has changed; then run `package.py` |
| `glossary` / `tm` | Glossary entries / translation memory rows (memory off for now) that apply to a file |
| `review-po` | All strings for the human reviewer in Poedit, proposals applied and fuzzy, with reason and original as comments |
| `finalize` | Human's saved file → `corrected.po` (only changed strings) and a learning report (kept, edited, reverted, missed) |
| `compare` | Compare two `.po` files by msgid (benchmark against human output) |

## How it is developed

A cheap model session (Haiku) does the translation and review work using only the base plugin, given a `.po` file as a real user would (see `review/README.md`, "Training sessions"). The Opus session that maintains the project plays the workflow (downloads, prechecks, gives the file), audits the output against the resources and fixes `resources/` and the skills. The translator session never edits them.

Benchmark: rounds 01 and 02 (in `rounds/`, not committed) have human-approved `corrected.po` files. Run the skill blind on copies of their `original.po` (outside the repo, so the answers are not visible) and compare with `dev_tools.py compare`.
