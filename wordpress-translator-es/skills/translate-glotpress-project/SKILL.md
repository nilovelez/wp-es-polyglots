---
name: translate-glotpress-project
description: Translate the untranslated strings of a translate.wordpress.org (GlotPress) project into Spanish (Spain, es_ES), end to end - download, translate with the es_ES glossary and style guide, and hand back the .po to import. Use it when someone gives a translate.wordpress.org URL (plugin, theme, core, Meta) and asks to translate it into Spanish.
---

# Translate a GlotPress project (es_ES)

The user gives a translate.wordpress.org project URL and wants you to translate its untranslated strings. Use the `translate` skill of this package (`<skill>/../translate/SKILL.md`, with `<skill>` this skill's folder) and follow it fully, passing the URL to `start`:

```
python3 <skill>/../../references/po_tool.py start <url> --translate
```

Any form of the project URL works (with filters, with or without `es/default`). `start` downloads the strings and, if the batch looks like one to reject whole or does not fit in one session, prints STOP and what to tell the user. `finish` prints the import URL: add it to the answer. You never upload or approve anything: the user does.
