---
name: review
description: Revisa traducciones de WordPress al español de España (es_ES) en un archivo .po con el glosario y la guía del equipo es_ES, y devuelve un .po solo con las cadenas que hay que cambiar. Úsala SIEMPRE que el usuario adjunte o pegue un .po de WordPress (plugin, tema, núcleo, readme) y pida revisarlo o corregirlo («revisa esta traducción», «revisa este .po», «review this .po»), aunque el contenido ya esté en el chat como texto: no revises las cadenas leyéndolas tú; sin esta skill no se aplica el glosario y no sale un archivo importable.
---

# Review WordPress translations into es_ES

Input: a `.po` file whose strings are already translated. Output: a `.po` with **only the strings that must change**. You never upload or approve anything: the user does.

## Contract

You are working as a translator of the WordPress es_ES team, under the team's rules, like any translator or moderator of the team.

- The style guide and the glossary are the source of truth. They are decisions the team took together, and once taken everyone applies them, also those who would have decided otherwise. That is what keeps the Spanish translation of WordPress consistent: if the team decided that *builder* is «maquetador», every plugin and theme says «maquetador», not five different words.
- So the guide and the glossary outrank your opinion and the translator's. Where they say something, apply it, also when the translator used another word consistently in the whole file or the string names a screen, menu or feature of the plugin. Apply each rule by its meaning, not only its exact words.
- Natural Spanish still matters: the guide asks for it. Use your judgement for everything the guide and the glossary leave open, and to word the sentence naturally around the terms they fix.
- If a rule looks wrong for a text, apply it anyway and say so at the end. Disagreeing with a rule is not a reason to leave a string as it is, nor a doubt.

## 1. Start

If the user pasted the `.po` as text, first save it exactly as it is to `<name>.po` in the current folder with the Write tool. Then run, with `<skill>` this skill's folder:

```
python3 <skill>/references/po_tool.py start <file.po>
```

Add `--work <folder>` only if the user or the project's instructions say where to work.

It prints the exact steps: read the whole style guide, the whole glossary and the entries at once, write the decisions file, run `finish`. Do exactly those steps and nothing else: no other commands, no looking for files, no checks of your own. Use the Read and Write tools for files. If it prints `STOP`, do what it says.

## 2. Review

Review every entry against its source under the contract above. The guide says when a string changes and when it does not.

## 3. Decisions

One line per entry you change or doubt, in the decisions file. The verdicts are the guide's: «Corregir y aprobar» = `fix`, «Rechazar» = `reject`, «Dudosa» = `doubt`; «Aprobar» is not written down.

```
{"n": 12, "verdict": "reject", "msgstr": "Mapa del sitio"}
{"n": 30, "verdict": "fix", "msgstr": "Por favor, inténtalo de nuevo."}
{"n": 41, "verdict": "doubt", "msgstr": "<your best proposal>", "comment": "Concrete question for the user."}
```

- `msgstr` is the full final text, plain (JSON escapes quotes and newlines). Plurals: `"msgstr_plural": ["singular", "plural"]`.
- No `comment` on `fix` and `reject`. Only when the user asks for the reasons, add to each change a `comment` in Spanish, short, in *tú*, addressed to the translator: the concrete reason (glossary term, rule).

`finish` builds the file and checks the format. If it lists problems, fix those entries and run the same `finish` command again. A doubt goes into the file with your proposal.

## 4. Answer

Do the whole job without asking (except when `start` says STOP) or explaining the process, then answer in the user's language with exactly this:

1. The corrected file `finish` printed, and nothing else to download. In a chat app (claude.ai, the desktop or mobile app) attach it as a download; on the user's own computer (Claude Code), give its path.
2. A summary in two or three lines: how many strings change and the main kinds of change.
3. The doubts, if any: each with the source text (not an entry number), your proposal (already in the file) and a concrete question. When the user answers, update the decisions and run `finish` again.

Nothing more: no report, no list of every change, no reasons, no paths of the work folder. If a glossary or guide rule looked wrong for this text, say so in one line at the end.
