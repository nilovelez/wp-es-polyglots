---
name: review-glotpress-waiting
description: Review the translations waiting for approval in a translate.wordpress.org (GlotPress) project for the es_ES locale, end to end - download, check whether the batch deserves a review, review it with the review skill of wordpress-translator-es, and hand back the .po to import. Use it when an es_ES editor (PTE/GTE) gives a translate.wordpress.org URL and asks to review its waiting strings.
---

# Review the waiting strings of a GlotPress project (es_ES)

Needs the `wordpress-translator-es` plugin. You never upload or approve anything: the user does.

1. Run, with `<skill>` this skill's folder:

   ```
   python3 <skill>/scripts/glotpress.py prepare <url>
   ```

   Any form of the project URL works (with filters, with or without `es/default`). If it prints `STOP`, do what it says.
2. If it names one file, use the `review` skill of `wordpress-translator-es` on it and follow that skill fully.
3. If it names several parts, do exactly what it prints: one subagent per part, one after another, never in parallel, each using the `review` skill on its part; then `merge`. A part is never done in this conversation, so that each one starts with a clean context. The user asking for this review is already the request for these subagents: start them without asking for permission.
4. Answer as the `review` skill says (the merged file and the doubts of all the parts), and add the import URL that `prepare` printed.
