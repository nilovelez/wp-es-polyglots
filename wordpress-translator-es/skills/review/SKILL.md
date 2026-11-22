---
name: review
description: Revisa traducciones de WordPress al español de España (es_ES) en un archivo .po con el glosario y la guía del equipo es_ES, y devuelve un .po solo con las cadenas que hay que cambiar. Úsala SIEMPRE que el usuario adjunte o pegue un .po de WordPress (plugin, tema, núcleo, readme) y pida revisarlo o corregirlo («revisa esta traducción», «revisa este .po», «review this .po»), aunque el contenido ya esté en el chat como texto: no revises las cadenas leyéndolas tú; sin esta skill no se aplica el glosario y no sale un archivo importable.
---

# Review WordPress translations into es_ES

Input: a `.po` file whose strings are already translated, or a translate.wordpress.org project URL (its waiting strings). Output: a `.po` with **only the strings that must change**; uploading it over the original replaces what is wrong. You never upload or approve anything: the user does.

## 1. Start

If the user pasted the `.po` as text, first save it exactly as it is to `<name>.po` in the current folder with the Write tool. Then run, with `<skill>` this skill's folder:

```
python3 <skill>/../../references/po_tool.py start <file.po or URL>
```

- Add `--work <folder>` only if the user or the project's instructions (its CLAUDE.md or similar) say where to work.
- Add `--window 500000` if you are Haiku 5.5 in Claude Cowork, `--window 200000` if you are not Claude Opus, Sonnet or Haiku 5.5.

It prints the exact steps: read the whole style guide, the whole glossary and the entries file at once, write the decisions file, run `finish`. Do exactly those steps and nothing else: no other commands, no looking for files, no checks of your own. Use the Read and Write tools for files. If it prints `STOP`, do what it says.

The glossary and the style guide are the only reference. Priority on conflict: the user's instructions → glossary → style guide. If a rule looks wrong for the text, apply it anyway and say so at the end.

## 2. Review

Read **every** entry against its source, for meaning and not only terms: prepositions, who does the action, words added or lost. Decide (section 6 of the style guide):

| Verdict | When |
|---|---|
| approve (not written down) | Correct, or only a matter of style |
| `fix` | Minor errors: accent, comma after «Por favor», non-Spanish quotes, extra capital |
| `reject` | Breaks the glossary, uses «usted», changes the meaning, breaks placeholders/HTML, leaves a glossary term in English, clearly unnatural |
| `doubt` | Probably wrong, but not enough context, and the guide and glossary do not settle it: give your best proposal and the question |

- **Change only what is wrong.** If the translation is good enough, approve it, even when you know a slightly better option. When you change a string, keep the translator's wording except for the error.
- Translators often use one synonym systematically instead of the glossary term. Apply the glossary term in every entry where it appears, also in small verbs, and fix gender and agreement.
- Same source string or term → same translation across the file. Approved strings in the project are not a reference: approved does not mean correct.
- Decide on your own whenever the guide or the glossary settle the case; doubts are only for real questions.
- The generic masculine is not a reason to reject.

## 3. Decisions

One line per entry you change or doubt, in the decisions file:

```
{"n": 12, "verdict": "reject", "msgstr": "Mapa del sitio"}
{"n": 30, "verdict": "fix", "msgstr": "Por favor, inténtalo de nuevo."}
{"n": 41, "verdict": "doubt", "msgstr": "<your best proposal>", "comment": "Concrete question for the user."}
```

- `msgstr` is the full final text, plain (JSON escapes quotes and newlines). Plurals: `"msgstr_plural": ["singular", "plural"]`.
- No `comment` on `fix` and `reject`. Only when the user asks for the reasons, add to each change a `comment` in Spanish, short, in *tú*, addressed to the translator: the concrete reason (glossary term, rule).
- If the translator's text is as likely to be right as anything you can propose, it is not a doubt: approve it.

`finish` builds the file and checks placeholders, HTML, entities, URLs, newlines, edge spaces, final punctuation and quotes. If it lists problems, fix those entries and run the same `finish` command again. A doubt goes into the file with your proposal, because the user approves everything else after importing.

## 4. Answer

Do the whole job without asking (except when `start` says STOP) or explaining the process, then answer in the user's language with exactly this:

1. The corrected file `finish` printed, and nothing else to download. In a chat app (claude.ai, the desktop or mobile app) attach it as a download; on the user's own computer (Claude Code), give its path.
2. A summary in two or three lines: how many strings change and the main kinds of change. If `finish` printed an import URL, add it.
3. The doubts, if any: each with the source text (not an entry number), your proposal (already in the file) and a concrete question. When the user answers, update the decisions and run `finish` again.

Nothing more: no report, no list of every change, no reasons, no paths of the work folder. If a glossary or guide rule looked wrong for this text, say so in one line at the end.
