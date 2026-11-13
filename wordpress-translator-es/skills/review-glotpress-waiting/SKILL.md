---
name: review-glotpress-waiting
description: Review the translations waiting for approval in a translate.wordpress.org (GlotPress) project for the es_ES locale, end to end - download, check whether the batch deserves a review, review it with the es_ES glossary and style guide, and hand back the .po to import. Use it when an es_ES editor (PTE/GTE) gives a translate.wordpress.org URL and asks to review its waiting strings.
---

# Review the waiting strings of a GlotPress project (es_ES)

For editors of the es_ES locale (PTE or GTE) who clear the waiting queue of a project in translate.wordpress.org. This skill runs the workflow; the review itself is done by the `review` skill of this package, with its rules. You never upload or approve anything: the user does. `<skill>` is this skill's folder; `<refs>` is the package's shared folder, `<skill>/../../references` (glossary, style guide and `po_tool.py`, used by all the skills of the package).

## 1. Download

```
python3 <refs>/po_tool.py fetch <url> <work>
```

Any form of the project URL works (with filters, with or without `es/default`). It writes the waiting strings to `<work>/original.po`. `<work>` is a temporary work folder, unless the user says where.

If there are no waiting strings, say so and stop.

## 2. Is the batch worth a review?

```
python3 <refs>/po_tool.py precheck <work>/original.po --window N
```

Your context window, for `--window`: 1000000 for Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 (Haiku 5.5 in Claude Cowork: 500000); 200000 for any other model, or if you do not know which model you are. The last line says whether the batch fits in one session.

Some batches must be rejected whole instead of reviewed string by string:

- Machine translation without care: many strings identical to the English source, glossary ignored everywhere, inconsistent terms, meaning errors in the sample. The mark `SEARCH AND REPLACE WITHOUT CARE` (glossary alternatives such as «obligatorio / requerido / necesario» pasted whole into a translation) is enough, even for a single string.
- Formal register («usted» forms in many strings) or Latin American Spanish throughout. The mark `FORMAL REGISTER THROUGHOUT` on the address line is enough: the «usted» count misses most imperatives, so trust the su/tu numbers over it.
- The source strings are not in English (e.g. the plugin was written in Spanish and the source was copied as the translation): the plugin cannot be translated until its source is in US English.

If the numbers point to one of these, give the user the numbers and the sample and ask whether to review it or reject it whole. If it does not fit in one session, tell the user the size and the parts it gives (entry ranges), review the first part now and offer the rest, one part per new conversation. Otherwise go on without asking, and put the precheck numbers in one line of the summary.

## 3. Review

Use the `review` skill of this package (`<skill>/../review/SKILL.md`) on `<work>/original.po`, with `<work>` as its work folder, and follow it fully. For large batches, its block procedure applies.

## 4. Hand back

The answer of the `review` skill (the file, a short summary and the doubts, nothing more), plus one line: where to import it, `https://translate.wordpress.org/projects/<path>/es/default/import-translations/` (the project path from the URL). Imported by an editor of the project, the strings replace the waiting ones; the rest can then be approved, and the doubts checked in GlotPress.
