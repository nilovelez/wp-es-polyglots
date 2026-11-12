---
name: translate
description: Traduce al español de España (es_ES) un archivo .pot o .po de WordPress (plugin, tema, núcleo, readme) con el glosario y la guía del equipo es_ES, y devuelve el .po traducido. Úsala SIEMPRE que el usuario adjunte o pegue un .pot o .po de WordPress y pida traducirlo («traduce este .pot», «traduce este archivo», «translate this into Spanish»), aunque el contenido ya esté en el chat como texto, o cuando dé un proyecto de translate.wordpress.org con cadenas sin traducir: no traduzcas las cadenas a mano en el chat; sin esta skill no se aplica el glosario y no sale un archivo importable.
---

# Translate WordPress strings into es_ES

Input: a `.pot` or `.po` file with strings to translate. Output: the same file translated into Spanish (Spain). Nothing else: you never upload or approve anything. `<skill>` is this skill's folder; `<refs>` is the package's shared folder, `<skill>/../../references` (glossary, style guide and `po_tool.py`, used by all the skills of the package). The scripts need only Python 3 (if `python3` does not exist, use `python` or `py -3`).

Always do the translation with this workflow and `po_tool.py`, never by reading the strings and answering in the chat: without it the glossary is not applied and the result cannot be imported.

## Read first, every time

The glossary and the guide in `<refs>` are the only reference: do not use other glossaries, guides or translations you may find on disk.

1. `<refs>/style-guide.md`, sections 1–5, once, with the Read tool (not `cat` too: reading it twice only fills the context). Follow it literally; it is the team's consensus.
2. The glossary entries that apply to the file. Do not read the whole glossary:
   ```
   python3 <refs>/po_tool.py glossary <file.po>
   ```
   Each line is `term (part of speech) → translation — notes [#entries]`. The notes are mandatory («No usar…», «No se traduce»).

Priority on conflict: the user's instructions → glossary → style guide. If a rule looks wrong for the text in front of you, apply it anyway and say so at the end.

## 1. Get the file

- The user's `.pot` or `.po`. In a plugin or theme folder without one, if WP-CLI is installed: `wp i18n make-pot . <work>/<text-domain>.pot`.
- A translate.wordpress.org project URL: `python3 <refs>/po_tool.py fetch <url> <work> --untranslated` writes its untranslated strings to `<work>/original.po`.
- The `.po` pasted into the chat (some apps turn an uploaded file into pasted text): save it exactly as it is to `<work>/original.po` and use that file.

`<work>` is a temporary work folder outside the user's project, unless the user says where. Then:

```
python3 <refs>/po_tool.py extract <file.po> <work>/entries.jsonl
```

One JSON object per entry: `n` (entry number), `ctx`, `note` (comment for translators), `msgid`, `msgstr` (or `msgid_plural` / `msgstr_plural`). Work by `n`. Never edit the `.po` by hand.

**Large files** (more than about 400 entries): work in blocks of about 300 entries with `--range A-B` on `extract` and `glossary`, appending to the same decisions file. Keep the term choices you settle in `<work>/terms.md` and re-read it before each block. Before starting, check that the whole file fits in this session: `python3 <refs>/po_tool.py size <file.po> --translate --window N`. Your context window, for `--window`: 1000000 for Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 (Haiku 5.5 in Claude Cowork: 500000); 200000 for any other model, or if you do not know which model you are. If it fits, do it all in this session, in blocks: never split it into several sessions or conversations, which reload the skill and the guide and cost more, not less. If it does not fit, tell the user the size and the parts it gives (entry ranges), translate the first part now and offer the rest, one part per new conversation. If the user asks for entries A to B only, do exactly that range.

## 2. Translate

Translate every empty or fuzzy entry. Do not change entries that are already translated unless asked. Translate everything without stopping; when unsure, use your best translation and mark it as a doubt.

- Plurals: always fill both forms.
- Keep placeholders (`%s`, `%1$d`, `{name}`), HTML, entities, URLs, `\n` and edge spaces exactly as in the source.
- Product, plugin and theme names are not translated.
- Same source string or term → same translation across the file.

## 3. Write decisions

`<work>/decisions.jsonl`, one line per translated entry:

```
{"n": 12, "verdict": "fix", "msgstr": "Mapa del sitio"}
{"n": 13, "verdict": "fix", "msgstr_plural": ["%d elemento", "%d elementos"]}
{"n": 41, "verdict": "doubt", "msgstr": "…", "comment": "Concrete question for the user."}
```

`msgstr` is the full text, plain (JSON escapes quotes and newlines). Use `doubt` (with your translation) only for real doubts.

## 4. Build and check

```
python3 <refs>/po_tool.py build <file.po> <work>/decisions.jsonl <out>/<name>-es_ES.po --full --report <work>/report.md
```

`<name>` is the name of the user's file without `.pot`/`.po` and without a locale suffix (`foo.pot` → `foo-es_ES.po`); for a project downloaded from its URL, the project and subproject (`foo-stable-es_ES.po`). Never a fixed name: the user may translate many files.

The output is the whole file, translated, with an es_ES header; doubts go in with your translation. The build checks placeholders, HTML, entities, URLs, newlines, edge spaces, final punctuation (GlotPress warns when it differs from the source: do not add or drop a final period) and quotes. Fix every reported problem in the decisions and build again until it reports 0 problems; if one is a false positive, say which and why.

## 5. Answer

Do the whole job without asking (except the size check above) or explaining the process, then answer in the user's language with exactly this:

1. the `translated .po` file, and nothing else to download. In a chat app (claude.ai, the desktop or mobile app) attach it to the answer as a download, never a path from your sandbox; on the user's own computer (Claude Code), give its path.
2. A summary in one or two lines: how many strings you translated.
3. The doubts, if any: each with the source text (not an entry number), your translation (already in the file) and a concrete question. When the user answers, update the decisions and build again.

Nothing more: no report, no list of every string, no paths of your work folder. If a glossary or guide rule looked wrong for this text, say so in one line at the end.
