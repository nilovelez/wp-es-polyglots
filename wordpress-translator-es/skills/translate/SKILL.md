---
name: translate
description: Translate a WordPress .pot or .po file (plugin, theme, core, readme) into Spanish (Spain, es_ES) following the es_ES team's glossary and style guide, and return the translated .po. Use it for "translate this into Spanish" with a .pot/.po file, or a translate.wordpress.org project whose untranslated strings should be translated.
---

# Translate WordPress strings into es_ES

Input: a `.pot` or `.po` file with strings to translate. Output: the same file translated into Spanish (Spain). Nothing else: you never upload or approve anything. `<skill>` is this skill's folder; `<refs>` is the package's shared folder, `<skill>/../../references` (glossary, style guide and `po_tool.py`, used by all the skills of the package). The scripts need only Python 3 (if `python3` does not exist, use `python` or `py -3`).

Always do the translation with this workflow and `po_tool.py`, never by reading the strings and answering in the chat: without it the glossary is not applied and the result cannot be imported.

## Read first, every time

1. Refresh the glossary (once per session; if it fails, the bundled copy is used):
   ```
   python3 <refs>/po_tool.py glossary-update
   ```
2. `<refs>/style-guide.md`: the quick reference at the top and the full guide (sections 1–6). Follow it literally; it is the team's consensus.
3. The glossary entries that apply to the file. Do not read the whole glossary:
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

**Large files** (more than about 400 entries): work in blocks of about 300 entries with `--range A-B` on `extract` and `glossary`, appending to the same decisions file. Keep the term choices you settle in `<work>/terms.md` and re-read it before each block. If the file has more than 1500 entries, tell the user the size and ask before starting. If the user asks for entries A to B only, do exactly that range.

## 2. Translate

Translate every empty or fuzzy entry (section 6 of the style guide). Do not change entries that are already translated unless asked. Translate everything without stopping; when unsure, use your best translation and mark it as a doubt.

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

The output is the whole file, translated, with an es_ES header; doubts go in with your translation. The build checks placeholders, HTML, entities, URLs, newlines, edge spaces and quotes. Fix every reported problem in the decisions and build again until it reports 0 problems; if one is a false positive, say which and why.

## 5. Answer

Short, in the user's language. Identify strings by their source text, not by entry number (the user's editor numbers them differently):

1. Where the translated `.po` is.
2. How many entries you translated.
3. The doubts, each with the source, your translation and a concrete question. When the user answers, update the decisions and build again.
4. Glossary or guide rules that looked wrong or unclear for this text, if any.
