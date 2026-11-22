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
2. It names the file to review: use the `review` skill of `wordpress-translator-es` on it and follow that skill fully.
3. Answer as the `review` skill says, and add the import URL that `prepare` printed.
