---
name: translate-glotpress-project
description: Translate the untranslated strings of a translate.wordpress.org (GlotPress) project into Spanish (Spain, es_ES), end to end - download, translate with the es_ES glossary and style guide, and hand back the .po to import. Use it when someone gives a translate.wordpress.org URL (plugin, theme, core, Meta) and asks to translate it into Spanish.
---

# Translate a GlotPress project (es_ES)

For anyone who translates a project of translate.wordpress.org into Spanish (Spain). This skill runs the workflow; the translation itself is done by the `translate` skill of this package, with its rules. You never upload or approve anything: the user does. Paths below are relative to this skill's folder (`<skill>`).

## 1. Download

```
python3 <skill>/scripts/po_tool.py fetch <url> <work> --untranslated
```

Any form of the project URL works (with filters, with or without `es/default`). It writes the untranslated strings to `<work>/original.po`. `<work>` is a temporary work folder, unless the user says where.

If there is nothing to translate, say so and stop. If there are more than about 1500 strings, tell the user the size and ask before starting (they may want a part only).

WordPress core, Meta (wordpress.org itself) and very popular plugins are read by millions of people: be especially careful with consistency, and mark as a doubt anything the glossary and the guide do not settle.

## 2. Translate

Use the `translate` skill of this package (`<skill>/../translate/SKILL.md` when installed as a package) on `<work>/original.po`, with `<work>` as its work folder, and follow it fully. For large files, its block procedure applies.

## 3. Hand back

1. The translated `.po`.
2. Where to import it: `https://translate.wordpress.org/projects/<path>/es/default/import-translations/` (the project path from the URL). Imported by an editor of the project (PTE/GTE), the strings can be added as approved or as waiting; imported by anyone else, they arrive as suggestions waiting for the es_ES team's approval.
3. How many strings were translated, and the doubts, as the `translate` skill says. When the user answers, update the decisions and build again.
