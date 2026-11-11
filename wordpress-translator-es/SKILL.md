---
name: wordpress-translator-es
description: Translate WordPress plugins and themes into Spanish (Spain, es_ES), or review translations waiting in translate.wordpress.org, following the es_ES team's glossary and style guide. Use it for "translate my plugin into Spanish", a .pot or .po file to translate, or a translate.wordpress.org URL to translate or review.
---

# WordPress translator (es_ES)

You translate WordPress strings into Spanish (Spain) or review translations that are waiting for approval, the way the es_ES team of WordPress Polyglots does. Paths below are relative to this skill's folder (`<skill>`). The scripts need only Python 3 (if `python3` does not exist, use `python` or `py -3`).

## Read first, every time

1. Refresh the glossary (once per session; if it fails, the bundled copy is used):
   ```
   python3 <skill>/scripts/po_tool.py glossary-update
   ```
2. `<skill>/style-guide.md`: the quick reference at the top (the criteria most often broken, and when a string should **not** be changed) and the full guide. Follow it literally; it is the team's consensus.
3. The glossary entries that apply to the file. Do not read the whole glossary:
   ```
   python3 <skill>/scripts/po_tool.py glossary <file.po>
   ```
   Each line is `term (part of speech) → translation — notes [#entries]`. The notes are mandatory («No usar…», «No se traduce»).

Priority on conflict: the user's instructions → glossary → style guide. If a rule looks wrong for the text in front of you, apply it anyway and say so at the end.

## 1. Get the file

Pick the mode from what the user gives you:

| The user gives you | Mode | Get the file |
|---|---|---|
| A `.pot` or a `.po` with empty strings, or asks to translate their plugin | translate | Use their file. In a plugin folder, look for `languages/*.pot`; if there is none and WP-CLI is installed, `wp i18n make-pot . languages/<text-domain>.pot` |
| A translate.wordpress.org URL and asks to translate | translate | `python3 <skill>/scripts/po_tool.py fetch <url> <work> --untranslated` |
| A translate.wordpress.org URL and asks to review (or the URL shows `status=waiting`) | review | `python3 <skill>/scripts/po_tool.py fetch <url> <work>` |
| A `.po` file and asks to review it | review | Use their file |

`<work>` is a work folder outside the user's project (a temporary folder) unless the user says where. `fetch` prints the number of strings and the import URL.

Then:

```
python3 <skill>/scripts/po_tool.py extract <file.po> <work>/entries.jsonl
```

One JSON object per entry: `n` (entry number), `ctx`, `note` (comment for translators, e.g. where the string comes from), `msgid`, `msgstr` (or `msgid_plural` / `msgstr_plural`). Work by `n`. Never edit the `.po` by hand.

**Large files** (more than about 400 entries): work in blocks of about 300 entries with `--range A-B` on `extract`, `glossary` and `lint`, appending to the same decisions file. Keep a list of the term choices you settle in `<work>/terms.md` and re-read it before each new block, so the whole file stays consistent. If the file has more than 1500 entries, tell the user the size and ask before starting. If the user asks you to work only on entries A to B, do exactly that range.

## 2a. Translate

Translate every empty or fuzzy entry (section 6 of the style guide). Do not change entries that are already translated unless asked. Translate everything without stopping; when unsure, use your best translation and mark it as a doubt.

- Plurals: always fill both forms (`msgstr_plural`: singular, plural).
- Keep placeholders (`%s`, `%1$d`, `{name}`), HTML, entities, URLs, `\n` and edge spaces exactly as in the source.
- Product, plugin and theme names are not translated.

## 2b. Review

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

`<work>/decisions.jsonl`, one line per entry you translate, change or doubt:

```
{"n": 12, "verdict": "reject", "msgstr": "Mapa del sitio", "comment": "Según el glosario, «sitemap» se traduce como «mapa del sitio»."}
{"n": 30, "verdict": "fix", "msgstr": "Por favor, inténtalo de nuevo.", "comment": "Coma tras «Por favor»."}
{"n": 41, "verdict": "doubt", "msgstr": "…", "comment": "Concrete question for the user."}
```

- `msgstr` is the full final text, plain (JSON escapes quotes and newlines). Plurals: `"msgstr_plural": ["singular", "plural"]`.
- Translate mode: `"verdict": "fix"` for every translated entry, and `doubt` (with your translation) only for real doubts.
- Review mode: `comment` is in Spanish, short, in *tú*: the concrete reason (glossary term, rule) and nothing else. For a `doubt`, keep the translator's text as `msgstr` and ask the question in the comment.

## 4. Build and check

Translate mode (whole file, doubts included with your translation):

```
python3 <skill>/scripts/po_tool.py build <file.po> <work>/decisions.jsonl <out>/<name>-es_ES.po --full --report <work>/report.md
```

Review mode (only the strings that change; doubts are left out):

```
python3 <skill>/scripts/po_tool.py build <file.po> <work>/decisions.jsonl <out>/corrected.po --report <work>/report.md
```

The build checks placeholders, HTML, entities, URLs, newlines, edge spaces and quotes. Fix every reported problem in the decisions and build again until it reports 0 problems; if one is a false positive, say which and why.

Where the result goes:

- **Plugins and themes hosted on WordPress.org** load their translations from translate.wordpress.org, not from the plugin's own files. Give the user the import URL (`https://translate.wordpress.org/projects/<type>/<slug>/<sub-project>/es/default/import-translations/`, printed by `fetch`). If they are not an editor (PTE/GTE) of that project, the imported strings arrive as suggestions waiting for the es_ES team's approval.
- **Plugins and themes not hosted on WordPress.org:** `languages/<text-domain>-es_ES.po`; if WP-CLI is installed, also `wp i18n make-mo` and `wp i18n make-php` on it so WordPress can load it.

## 5. Answer

Short, in the user's language:

1. Where the file is, and the import URL when it applies. The user imports it; never upload or approve anything yourself.
2. Counts: translated, or approved / fixed / rejected.
3. The main kinds of changes, with counts.
4. The doubts, each with the source, your proposal and a concrete question. When the user answers, update the decisions and build again.
5. Review mode: GlotPress does not carry comments when a file is imported. The reasons for each change are in `<work>/report.md`; say so, so the user can pass them on to the translator.
6. Glossary or guide rules that looked wrong or unclear for this text, if any.
