---
name: review
description: Revisa traducciones de WordPress al español de España (es_ES) en un archivo .po con el glosario y la guía del equipo es_ES, y devuelve un .po solo con las cadenas que hay que cambiar. Úsala SIEMPRE que el usuario adjunte o pegue un .po de WordPress (plugin, tema, núcleo, readme) y pida revisarlo o corregirlo («revisa esta traducción», «revisa este .po», «review this .po»), aunque el contenido ya esté en el chat como texto: no revises las cadenas leyéndolas tú; sin esta skill no se aplica el glosario y no sale un archivo importable.
---

# Review WordPress translations into es_ES

Input: a `.po` file whose strings are already translated. Output: a `.po` with **only the strings that must change**. You never upload or approve anything: the user does.

## Contract

You are doing a job for the WordPress translation team of the target locale, under their rules.

- The style guide and the glossary are the team's decisions, agreed by consensus. They outrank your opinion, the translator's choices and what sounds more natural to you.
- The user's explicit instructions outrank the glossary and the guide.
- Where the glossary or the guide says something, apply it. It does not matter that another word reads better, that the translator used another one consistently in the whole file, or that the string names a screen, menu or feature of the plugin.
- Apply each rule by its meaning, not only its exact words.
- Your own judgement only decides what the glossary and the guide do not cover.
- If a rule looks wrong for a text, apply it anyway and say so at the end. A rule you disagree with is not a reason to leave a string as it is, nor a doubt.

## 1. Start

If the user pasted the `.po` as text, first save it exactly as it is to `<name>.po` in the current folder with the Write tool. Then run, with `<skill>` this skill's folder:

```
python3 <skill>/references/po_tool.py start <file.po>
```

Add `--work <folder>` only if the user or the project's instructions say where to work.

It prints the exact steps: for each block of entries, read the whole style guide, the whole glossary and that block, then write that block's decisions before reading the next block; at the end, run `finish`. Do exactly those steps and nothing else: no other commands, no looking for files, no checks of your own. Use the Read and Write tools for files. If it prints `STOP`, do what it says.

## 2. Review

Review every entry against its source under the contract above. For each entry:

- If it is right, leave it as it is.
- If it has an error, replace it with the corrected translation.
- If there is not enough context to decide, it is a doubt: give your proposal and a concrete question.

When deciding:

- An entry has an error if it breaks the glossary or the guide, says something different from the source, is badly written, or does not read naturally: it reads like a literal or machine translation, not like a text written directly in the target language. If it follows the glossary and the guide and reads naturally, leave it, even if you would say it another way. An entry that reads naturally but breaks the glossary or the guide is an error.
- When you change an entry, keep the translator's wording and fix only the error.
- The glossary is never a preference: apply it in every entry. Only the guide's preferred forms (appendix A.3) are applied when you already change the entry for another reason.
- If the translator always uses another word instead of a glossary term, fix it in every entry where it appears, and adjust the rest of the sentence to it.
- Check the meaning, not only the terms: who does the action, the relation between words, words added or missing.
- In changelogs, be more tolerant.

## 3. Decisions

One line per entry you change or doubt, in the block's decisions file. `fix` for an entry you replace, `doubt` for a doubt.

```
{"n": 12, "verdict": "fix", "msgstr": "Mapa del sitio"}
{"n": 30, "verdict": "fix", "msgstr": "Por favor, inténtalo de nuevo."}
{"n": 41, "verdict": "doubt", "msgstr": "<your best proposal>", "comment": "Concrete question for the user."}
```

- `msgstr` is the full final text, plain (JSON escapes quotes and newlines). Plurals: `"msgstr_plural": ["singular", "plural"]`.
- No `comment` on `fix`. Only when the user asks for the reasons, add to each change a `comment` in Spanish, short, in *tú*, addressed to the translator: the concrete reason (glossary term, rule).

`finish` builds the file and checks the format. If it lists problems, fix those entries and run the same `finish` command again. A doubt goes into the file with your proposal.

## 4. Answer

Do the whole job without asking (except when `start` says STOP) or explaining the process, then answer in the user's language with exactly this:

1. The corrected file `finish` printed, and nothing else to download. In a chat app (claude.ai, the desktop or mobile app) attach it as a download; on the user's own computer (Claude Code), give its path.
2. A summary in two or three lines: how many strings change and the main kinds of change.
3. The doubts, if any: each with the source text (not an entry number), your proposal (already in the file) and a concrete question. When the user answers, update the decisions and run `finish` again.

Nothing more: no report, no list of every change, no reasons, no paths of the work folder. If a glossary or guide rule looked wrong for this text, say so in one line at the end.
