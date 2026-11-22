---
name: review-glotpress-waiting
description: Review the translations waiting for approval in a translate.wordpress.org (GlotPress) project for the es_ES locale, end to end - download, check whether the batch deserves a review, review it with the es_ES glossary and style guide, and hand back the .po to import. Use it when an es_ES editor (PTE/GTE) gives a translate.wordpress.org URL and asks to review its waiting strings.
---

# Review the waiting strings of a GlotPress project (es_ES)

The user gives a translate.wordpress.org project URL and wants you to review its waiting strings. Use the `review` skill of this package (`<skill>/../review/SKILL.md`, with `<skill>` this skill's folder) and follow it fully, passing the URL to `start`:

```
python3 <skill>/../../references/po_tool.py start <url>
```

Any form of the project URL works (with filters, with or without `es/default`). `start` downloads the strings and, if the batch looks like one to reject whole or does not fit in one session, prints STOP and what to tell the user. `finish` prints the import URL: add it to the answer. You never upload or approve anything: the user does.
