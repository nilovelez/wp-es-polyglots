---
name: translate
description: Traduce al español de España (es_ES) un archivo .pot o .po de WordPress (plugin, tema, núcleo, readme) con el glosario y la guía del equipo es_ES, y devuelve el .po traducido. Úsala SIEMPRE que el usuario adjunte o pegue un .pot o .po de WordPress y pida traducirlo («traduce este .pot», «traduce este archivo», «translate this into Spanish»), aunque el contenido ya esté en el chat como texto: no traduzcas las cadenas a mano en el chat; sin esta skill no se aplica el glosario y no sale un archivo importable.
---

# Translate WordPress strings into es_ES

Input: a `.pot` or `.po` file with strings to translate. Output: the same file translated into Spanish (Spain). You never upload or approve anything: the user does.

## Contract

You are working as a translator of the WordPress es_ES team, under the team's rules, like any translator or moderator of the team.

- The style guide and the glossary are the source of truth. They are decisions the team took together, and once taken everyone applies them, also those who would have decided otherwise. That is what keeps the Spanish translation of WordPress consistent: if the team decided that *builder* is «maquetador», every plugin and theme says «maquetador», not five different words.
- So the guide and the glossary outrank your opinion and the translator's. Where they say something, apply it, also when the translator used another word consistently in the whole file or the string names a screen, menu or feature of the plugin. Apply each rule by its meaning, not only its exact words.
- Natural Spanish still matters: the guide asks for it. Use your judgement for everything the guide and the glossary leave open, and to word the sentence naturally around the terms they fix.
- If a rule looks wrong for a text, apply it anyway and say so at the end. Disagreeing with a rule is not a reason to leave a string as it is, nor a doubt.

## 1. Start

If the user pasted the file as text, first save it exactly as it is to `<name>.po` in the current folder with the Write tool. Then run, with `<skill>` this skill's folder:

```
python3 <skill>/references/po_tool.py start <file> --translate
```

Add `--work <folder>` only if the user or the project's instructions say where to work.

It prints the exact steps: read the whole style guide, the whole glossary and the entries at once, write the decisions file, run `finish`. Do exactly those steps and nothing else: no other commands, no looking for files, no checks of your own. Use the Read and Write tools for files. If it prints `STOP`, do what it says.

## 2. Translate

Translate every entry under the contract above. Translate everything without stopping; when unsure, use your best translation and mark it as a doubt.

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
2. A summary in one or two lines: how many strings you translated.
3. The doubts, if any: each with the source text (not an entry number), your translation (already in the file) and a concrete question. When the user answers, update the decisions and run `finish` again.

Nothing more: no report, no list of every string, no paths of the work folder. If a glossary or guide rule looked wrong for this text, say so in one line at the end.
