---
name: review
description: Revisa traducciones de WordPress al español de España (es_ES) en un archivo .po con el glosario y la guía del equipo es_ES, y devuelve un .po solo con las cadenas que hay que cambiar. Úsala SIEMPRE que el usuario adjunte o pegue un .po de WordPress (plugin, tema, núcleo, readme) y pida revisarlo o corregirlo («revisa esta traducción», «revisa este .po», «review this .po»), aunque el contenido ya esté en el chat como texto: no revises las cadenas leyéndolas tú; sin esta skill no se aplica el glosario y no sale un archivo importable.
---

# Review WordPress translations into es_ES

Input: a `.po` file whose strings are already translated. Output: a `.po` with **only the strings that must change**, with the corrected translation; uploading it over the original replaces what is wrong, and everything else stays as it was. Nothing else: you never upload or approve anything. `<skill>` is this skill's folder; `<refs>` is the package's shared folder, `<skill>/../../references` (glossary, style guide and `po_tool.py`, used by all the skills of the package). The scripts need only Python 3 (if `python3` does not exist, use `python` or `py -3`).

Always do the review with this workflow and `po_tool.py`, never by reading the strings and answering in the chat: without it the glossary is not applied and the result cannot be imported.

## Read first, every time

The glossary and the guide in `<refs>` are the only reference: do not use other glossaries, guides or translations you may find on disk.

1. `<refs>/style-guide.md`, all of it: section 6 says when a string should **not** be changed. Follow it literally; it is the team's consensus.
2. The glossary entries that apply to the file. Do not read the whole glossary:
   ```
   python3 <refs>/po_tool.py glossary <file.po>
   ```
   Each line is `term (part of speech) → translation — notes [#entries]`. The notes are mandatory («No usar…», «No se traduce»).

Priority on conflict: the user's instructions → glossary → style guide. If a rule looks wrong for the text in front of you, apply it anyway and say so at the end.

## 1. Get the file

- The user's `.po`.
- A translate.wordpress.org project URL: `python3 <refs>/po_tool.py fetch <url> <work>` writes its waiting strings to `<work>/original.po`.
- The `.po` pasted into the chat (some apps turn an uploaded file into pasted text): save it exactly as it is to `<work>/original.po` and use that file.

`<work>` is a temporary work folder outside the user's project, unless the user says where. Then:

```
python3 <refs>/po_tool.py extract <file.po> <work>/entries.jsonl
```

One JSON object per entry: `n` (entry number), `ctx`, `note` (comment for translators, e.g. where the string comes from), `msgid`, `msgstr` (or `msgid_plural` / `msgstr_plural`). Work by `n`. Never edit the `.po` by hand.

**Large files** (more than about 400 entries): work in blocks of about 300 entries with `--range A-B` on `extract`, `glossary` and `lint`, appending to the same decisions file. Keep the term choices you settle in `<work>/terms.md` and re-read it before each block, so the whole file stays consistent. If the file has more than 1500 entries, tell the user the size and ask before starting. If the user asks for entries A to B only, do exactly that range.

## 2. Review

First the automatic hints:

```
python3 <refs>/po_tool.py lint <file.po>
```

They flag glossary terms missing or left in English (with the glossary note), capitals mid-sentence and typography. Look at every hinted entry: most hints are real errors, some are not (the term is there in another form, or the string is fine as it is). Then read **every** entry against its source, for meaning and not only terms: prepositions, who does the action, words added or lost. Decide (section 6 of the style guide):

| Verdict | When |
|---|---|
| approve (not written down) | Correct, or only a matter of style |
| `fix` | Minor errors: accent, comma after «Por favor», non-Spanish quotes, extra capital |
| `reject` | Breaks the glossary, uses «usted», changes the meaning, breaks placeholders/HTML, leaves a glossary term in English, clearly unnatural |
| `doubt` | Probably wrong, but not enough context, and the guide and glossary do not settle it: give your best proposal and the question |

- **Change only what is wrong.** If the translation is good enough, approve it, even when you know a slightly better option (section 6 of the guide lists cases). When you change a string, keep the translator's wording except for the error.
- Translators often use one synonym systematically instead of the glossary term. Apply the glossary term in every entry where it appears, also in small verbs, and fix gender and agreement.
- Same source string or term → same translation across the file. Do not use the project's already approved strings as a reference: approved does not mean correct.
- Decide on your own whenever the guide or the glossary settle the case; doubts are only for real questions.
- The generic masculine is not a reason to reject.

## 3. Write decisions

`<work>/decisions.jsonl`, one line per entry you change or doubt:

```
{"n": 12, "verdict": "reject", "msgstr": "Mapa del sitio", "comment": "Según el glosario, «sitemap» se traduce como «mapa del sitio»."}
{"n": 30, "verdict": "fix", "msgstr": "Por favor, inténtalo de nuevo.", "comment": "Coma tras «Por favor»."}
{"n": 41, "verdict": "doubt", "msgstr": "<your best proposal>", "comment": "Concrete question for the user."}
```

- `msgstr` is the full final text, plain (JSON escapes quotes and newlines). Plurals: `"msgstr_plural": ["singular", "plural"]`.
- `comment` is in Spanish, short, in *tú*, addressed to the translator: the concrete reason (glossary term, rule) and nothing else.
- For a `doubt`, put your best proposal as `msgstr` and ask the question in the comment. If the translator's text is as likely to be right as anything you can propose, it is not a doubt: approve it.

## 4. Build and check

```
python3 <refs>/po_tool.py build <file.po> <work>/decisions.jsonl <out>/<name>-corrected.po --report <work>/report.md
```

`<name>` is the name of the user's file without `.po` (`wp-plugins-foo-stable-es.po` → `wp-plugins-foo-stable-es-corrected.po`); for a project downloaded from its URL, the project and subproject (`foo-stable-corrected.po`). The user may review many files: a fixed name like `corrected.po` ends up as «corrected (7).po» in their downloads.

The corrected file keeps the original header and only the entries that change: `fix`, `reject` and `doubt` (with your proposal). Doubts go in because the user imports the file and then approves everything else: a doubt left out would be approved as it was. The build checks placeholders, HTML, entities, URLs, newlines, edge spaces and quotes. Fix every reported problem in the decisions and build again until it reports 0 problems; if one is a false positive, say which and why.

## 5. Answer

Do the whole job without asking (except the size check above) or explaining the process, then answer in the user's language with exactly this:

1. the `<name>-corrected.po` file, and nothing else to download. In a chat app (claude.ai, the desktop or mobile app) attach it to the answer as a download, never a path from your sandbox; on the user's own computer (Claude Code), give its path.
2. A summary in two or three lines: how many strings change and the main kinds of change.
3. The doubts, if any: each with the source text (not an entry number), your proposal (already in the file) and a concrete question. When the user answers, update the decisions and build again.

Nothing more: no report, no list of every change, no paths of your work folder. The reasons for each change stay in `<work>/report.md`; give them only if the user asks (importing a `.po` does not carry comments, so they may want to pass them on to the translator). If a glossary or guide rule looked wrong for this text, say so in one line at the end.
