# Review of waiting strings

Goal: clear the es_ES *waiting* queue fast, and learn from every round.

## Round

1. Nilo runs, on Marcianito, `polyglots fetch <project url> --get waiting` (without `--no-ai` it also does a first review) and hands over the original `.po` and the `-repaired.po`.
2. Claude creates `rounds/NN-project/` with `original.po` and `repaired.po`, and builds `corrected.po` with **only the strings that must change compared with the original**:
   - header from the original; keep its `#.` and `#,` comments; drop `# polyglots:` comments;
   - if a tool fix is wrong, the string goes back to its original state (it does not appear in `corrected.po`);
   - check that HTML tags, entities, URLs, placeholders (`%s`, `{id}`…) and `\n` match the original.
3. Nilo reviews it, gives feedback and uploads it. As PTE, the upload replaces the waiting strings and can mark them approved or waiting; then he approves the rest.
4. Claude updates the rules (`polyglots/rules/`), logs the round in `polyglots/calibration-log.md`, and moves general criteria to `resources/`. Deliver the new YAML with a short summary.
5. Nilo applies the YAML on Marcianito and moves on to the next project.

Reference for verdicts and upload permissions: `resources/moderation-guide.md` and section 7 of `resources/style-guide.md`.

## Round folder

```
rounds/NN-project/
  original.po          waiting strings as downloaded
  repaired.po          tool output
  corrected.po         only the strings to change (what Nilo uploads)
  make-corrected.py    script that built corrected.po (optional)
  *.md                 round notes (Spanish)
```
