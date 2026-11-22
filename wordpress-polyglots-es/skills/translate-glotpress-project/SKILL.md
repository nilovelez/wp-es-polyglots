---
name: translate-glotpress-project
description: Translate the untranslated strings of a translate.wordpress.org (GlotPress) project into Spanish (Spain, es_ES), end to end - download, translate with the translate skill of wordpress-translator-es, and hand back the .po to import. Use it when someone gives a translate.wordpress.org URL (plugin, theme, core, Meta) and asks to translate it into Spanish.
---

# Translate a GlotPress project (es_ES)

Needs the `wordpress-translator-es` plugin. You never upload or approve anything: the user does.

1. Run, with `<skill>` this skill's folder:

   ```
   python3 <skill>/scripts/glotpress.py prepare <url> --translate
   ```

   Any form of the project URL works (with filters, with or without `es/default`). If it prints `STOP`, do what it says.
2. It names the file to translate: use the `translate` skill of `wordpress-translator-es` on it and follow that skill fully.
3. Answer as the `translate` skill says, and add the import URL that `prepare` printed.
