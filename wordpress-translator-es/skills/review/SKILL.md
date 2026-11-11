---
name: review
description: Review WordPress translations into Spanish (Spain, es_ES) in a .po file (typically strings waiting for approval in translate.wordpress.org) against the es_ES team's glossary and style guide, and return a .po with only the strings that must change. Use it for "review this .po" or "check these Spanish translations".
---

# Review WordPress translations into es_ES

Input: a `.po` file whose strings are already translated. Output: a `.po` with **only the strings that must change**, with the corrected translation; uploading it over the original replaces what is wrong, and everything else stays as it was. Nothing else: you never upload or approve anything. Paths below are relative to this skill's folder (`<skill>`). The scripts need only Python 3 (if `python3` does not exist, use `python` or `py -3`).

## Read first, every time

1. Refresh the glossary (once per session; if it fails, the bundled copy is used):
   ```
   python3 <skill>/scripts/po_tool.py glossary-update
   ```
2. `<skill>/style-guide.md`: the quick reference at the top (the criteria most often broken, and when a string should **not** be changed) and the full guide (sections 1–5 and 7). Follow it literally; it is the team's consensus.
3. The glossary entries that apply to the file. Do not read the whole glossary:
   ```
   python3 <skill>/scripts/po_tool.py glossary <file.po>
   ```
   Each line is `term (part of speech) → translation — notes [#entries]`. The notes are mandatory («No usar…», «No se traduce»).

Priority on conflict: the user's instructions → glossary → style guide. If a rule looks wrong for the text in front of you, apply it anyway and say so at the end.

## 1. Get the file

- The user's `.po`.
- A translate.wordpress.org project URL: `python3 <skill>/scripts/po_tool.py fetch <url> <work>` writes its waiting strings to `<work>/original.po`.

`<work>` is a temporary work folder outside the user's project, unless the user says where. Then:

```
python3 <skill>/scripts/po_tool.py extract <file.po> <work>/entries.jsonl
```

One JSON object per entry: `n` (entry number), `ctx`, `note` (comment for translators, e.g. where the string comes from), `msgid`, `msgstr` (or `msgid_plural` / `msgstr_plural`). Work by `n`. Never edit the `.po` by hand.

**Large files** (more than about 400 entries): work in blocks of about 300 entries with `--range A-B` on `extract`, `glossary` and `lint`, appending to the same decisions file. Keep the term choices you settle in `<work>/terms.md` and re-read it before each block, so the whole file stays consistent. If the file has more than 1500 entries, tell the user the size and ask before starting. If the user asks for entries A to B only, do exactly that range.

## 2. Review

First the automatic hints:

```
python3 <skill>/scripts/po_tool.py lint <file.po>
```

They flag glossary terms missing or left in English (with the glossary note), capitals mid-sentence and typography. Look at every hinted entry: most hints are real errors, some are not (the term is there in another form, or the string is fine as it is). Then read **every** entry against its source, for meaning and not only terms: prepositions, who does the action, words added or lost. Decide (section 7 of the style guide):

| Verdict | When |
|---|---|
| approve (not written down) | Correct, or only a matter of style |
| `fix` | Minor errors: accent, comma after «Por favor», non-Spanish quotes, extra capital |
| `reject` | Breaks the glossary, uses «usted», changes the meaning, breaks placeholders/HTML, leaves a glossary term in English, clearly unnatural |
| `doubt` | Not enough context, and the guide and glossary do not settle it |

- **Change only what is wrong.** If the translation is good enough, approve it, even when you know a slightly better option (the quick reference lists cases). When you change a string, keep the translator's wording except for the error.
- Translators often use one synonym systematically instead of the glossary term. Apply the glossary term in every entry where it appears, also in small verbs, and fix gender and agreement.
- Same source string or term → same translation across the file. Do not use the project's already approved strings as a reference: approved does not mean correct.
- Decide on your own whenever the guide or the glossary settle the case; doubts are only for real questions.
- The generic masculine is not a reason to reject.

## 3. Write decisions

`<work>/decisions.jsonl`, one line per entry you change or doubt:

```
{"n": 12, "verdict": "reject", "msgstr": "Mapa del sitio", "comment": "Según el glosario, «sitemap» se traduce como «mapa del sitio»."}
{"n": 30, "verdict": "fix", "msgstr": "Por favor, inténtalo de nuevo.", "comment": "Coma tras «Por favor»."}
{"n": 41, "verdict": "doubt", "msgstr": "<the translator's text, unchanged>", "comment": "Concrete question for the user."}
```

- `msgstr` is the full final text, plain (JSON escapes quotes and newlines). Plurals: `"msgstr_plural": ["singular", "plural"]`.
- `comment` is in Spanish, short, in *tú*, addressed to the translator: the concrete reason (glossary term, rule) and nothing else.
- For a `doubt`, keep the translator's text as `msgstr` and ask the question in the comment.

## 4. Build and check

```
python3 <skill>/scripts/po_tool.py build <file.po> <work>/decisions.jsonl <out>/corrected.po --report <work>/report.md
```

`corrected.po` keeps the original header and only the `fix` and `reject` entries; doubts are left out until the user answers. The build checks placeholders, HTML, entities, URLs, newlines, edge spaces and quotes. Fix every reported problem in the decisions and build again until it reports 0 problems; if one is a false positive, say which and why.

## 5. Answer

Short, in the user's language:

1. Where `corrected.po` is.
2. Counts: approved, fixed, rejected, doubts.
3. The main kinds of changes, with counts.
4. The doubts, each with the source, the translation, your proposal and a concrete question. When the user answers, update the decisions and build again.
5. The reasons for each change are in `<work>/report.md`: importing a `.po` does not carry comments, so the user can pass them on to the translator.
6. Glossary or guide rules that looked wrong or unclear for this text, if any.
