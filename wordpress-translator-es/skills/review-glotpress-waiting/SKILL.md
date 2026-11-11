---
name: review-glotpress-waiting
description: Review the translations waiting for approval in a translate.wordpress.org (GlotPress) project for the es_ES locale, end to end - download, check whether the batch deserves a review, review it with the es_ES glossary and style guide, and hand back the .po to import. Use it when an es_ES editor (PTE/GTE) gives a translate.wordpress.org URL and asks to review its waiting strings.
---

# Review the waiting strings of a GlotPress project (es_ES)

For editors of the es_ES locale (PTE or GTE) who clear the waiting queue of a project in translate.wordpress.org. This skill runs the workflow; the review itself is done by the `review` skill of this package, with its rules. You never upload or approve anything: the user does. Paths below are relative to this skill's folder (`<skill>`).

## 1. Download

```
python3 <skill>/scripts/po_tool.py fetch <url> <work>
```

Any form of the project URL works (with filters, with or without `es/default`). It writes the waiting strings to `<work>/original.po`. `<work>` is a temporary work folder, unless the user says where.

If there are no waiting strings, say so and stop.

## 2. Is the batch worth a review?

```
python3 <skill>/scripts/po_tool.py precheck <work>/original.po
```

Some batches must be rejected whole instead of reviewed string by string:

- Machine translation without care: many strings identical to the English source, glossary ignored everywhere, inconsistent terms, meaning errors in the sample.
- Formal register («usted» forms in many strings) or Latin American Spanish throughout.
- The source strings are not in English (e.g. the plugin was written in Spanish and the source was copied as the translation): the plugin cannot be translated until its source is in US English.

If the numbers point to one of these, or the batch has more than about 400 strings, give the user the numbers and the sample and ask whether to review it or reject it whole. Otherwise go on.

## 3. Review

Use the `review` skill of this package (`<skill>/../review/SKILL.md` when installed as a package) on `<work>/original.po`, with `<work>` as its work folder, and follow it fully. For large batches, its block procedure applies.

## 4. Hand back

1. `<work>/corrected.po`: only the strings to change.
2. Where to import it: `https://translate.wordpress.org/projects/<path>/es/default/import-translations/` (the project path from the URL). Imported by an editor of the project, the strings replace the waiting ones; the rest of the waiting strings can then be approved.
3. The counts, the main kinds of changes and the doubts, as the `review` skill says. When the user answers the doubts, update the decisions and build again.
4. The reasons for the changes are in `<work>/report.md`, to pass on to the translator if wanted.
