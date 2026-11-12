---
name: translate-glotpress-project
description: Translate the untranslated strings of a translate.wordpress.org (GlotPress) project into Spanish (Spain, es_ES), end to end - download, translate with the es_ES glossary and style guide, and hand back the .po to import. Use it when someone gives a translate.wordpress.org URL (plugin, theme, core, Meta) and asks to translate it into Spanish.
---

# Translate a GlotPress project (es_ES)

For anyone who translates a project of translate.wordpress.org into Spanish (Spain). This skill runs the workflow; the translation itself is done by the `translate` skill of this package, with its rules. You never upload or approve anything: the user does. `<skill>` is this skill's folder; `<refs>` is the package's shared folder, `<skill>/../../references` (glossary, style guide and `po_tool.py`, used by all the skills of the package).

## 1. Download

```
python3 <refs>/po_tool.py fetch <url> <work> --untranslated
```

Any form of the project URL works (with filters, with or without `es/default`). It writes the untranslated strings to `<work>/original.po`. `<work>` is a temporary work folder, unless the user says where.

If there is nothing to translate, say so and stop. If there are more than 7000 strings, they do not fit in one session: tell the user the size and offer to translate strings 1 to 7000 now and the rest in a new conversation.

WordPress core, Meta (wordpress.org itself) and very popular plugins are read by millions of people: be especially careful with consistency, and mark as a doubt anything the glossary and the guide do not settle.

## 2. Translate

Use the `translate` skill of this package (`<skill>/../translate/SKILL.md`) on `<work>/original.po`, with `<work>` as its work folder, and follow it fully. For large files, its block procedure applies.

## 3. Hand back

The answer of the `translate` skill (the file, a short summary and the doubts, nothing more), plus one line: where to import it, `https://translate.wordpress.org/projects/<path>/es/default/import-translations/` (the project path from the URL). Imported by an editor of the project (PTE/GTE), the strings can be added as approved or as waiting; imported by anyone else, they arrive as suggestions waiting for the es_ES team's approval.
