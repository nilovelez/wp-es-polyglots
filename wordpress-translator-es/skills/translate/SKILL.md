---
name: translate
description: Traduce al español de España (es_ES) un archivo .pot o .po de WordPress (plugin, tema, núcleo, readme) con el glosario y la guía del equipo es_ES, y devuelve el .po traducido. Úsala SIEMPRE que el usuario adjunte o pegue un .pot o .po de WordPress y pida traducirlo («traduce este .pot», «traduce este archivo», «translate this into Spanish»), aunque el contenido ya esté en el chat como texto, o cuando dé un proyecto de translate.wordpress.org con cadenas sin traducir: no traduzcas las cadenas a mano en el chat; sin esta skill no se aplica el glosario y no sale un archivo importable.
---

# Translate WordPress strings into es_ES

Input: a `.pot` or `.po` file with strings to translate, or a translate.wordpress.org project URL (its untranslated strings). Output: the same file translated into Spanish (Spain). You never upload or approve anything: the user does.

## 1. Start

If the user pasted the file as text, first save it exactly as it is to `<name>.po` in the current folder with the Write tool. In a plugin or theme folder without a `.pot`, if WP-CLI is installed: `wp i18n make-pot . <text-domain>.pot`. Then run, with `<skill>` this skill's folder:

```
python3 <skill>/../../references/po_tool.py start <file or URL> --translate
```

- Add `--work <folder>` only if the user or the project's instructions (its CLAUDE.md or similar) say where to work.
- Add `--window 500000` if you are Haiku 5.5 in Claude Cowork, `--window 200000` if you are not Claude Opus, Sonnet or Haiku 5.5.

It prints the exact steps: read the whole style guide, the whole glossary and the entries file at once, write the decisions file, run `finish`. Do exactly those steps and nothing else: no other commands, no looking for files, no checks of your own. Use the Read and Write tools for files. If it prints `STOP`, do what it says.

The glossary and the style guide are the only reference. Priority on conflict: the user's instructions → glossary → style guide. If a rule looks wrong for the text, apply it anyway and say so at the end.

## 2. Translate

Translate every entry in the entries file. Translate everything without stopping; when unsure, use your best translation and mark it as a doubt.

- Plurals: always fill both forms.
- Keep placeholders (`%s`, `%1$d`, `{name}`), HTML, entities, URLs, `\n` and edge spaces exactly as in the source. Do not add or drop a final period.
- Product, plugin and theme names are not translated.
- Same source string or term → same translation across the file.

## 3. Decisions

One line per entry, in the decisions file:

```
{"n": 12, "verdict": "fix", "msgstr": "Mapa del sitio"}
{"n": 13, "verdict": "fix", "msgstr_plural": ["%d elemento", "%d elementos"]}
{"n": 41, "verdict": "doubt", "msgstr": "…", "comment": "Concrete question for the user."}
```

`msgstr` is the full text, plain (JSON escapes quotes and newlines). Use `doubt` (with your translation) only for real doubts.

`finish` builds the whole file with an es_ES header and checks it. If it lists problems or entries not translated, fix those and run the same `finish` command again.

## 4. Answer

Do the whole job without asking (except when `start` says STOP) or explaining the process, then answer in the user's language with exactly this:

1. The translated file `finish` printed, and nothing else to download. In a chat app (claude.ai, the desktop or mobile app) attach it as a download; on the user's own computer (Claude Code), give its path.
2. A summary in one or two lines: how many strings you translated. If `finish` printed an import URL, add it.
3. The doubts, if any: each with the source text (not an entry number), your translation (already in the file) and a concrete question. When the user answers, update the decisions and run `finish` again.

Nothing more: no report, no list of every string, no paths of the work folder. If a glossary or guide rule looked wrong for this text, say so in one line at the end.
