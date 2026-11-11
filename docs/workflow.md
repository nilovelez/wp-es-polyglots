# How we work

## Principles

- **Work by milestones.** At the end of each milestone, summarize and stop until the next one is approved.
- **Every review round is training data.** The strings we review are real; each correction is a chance to improve the rules, the style guide, the glossary notes or the translation memory, so the next round costs less.
- **Cheap first, expensive last.** Exact matches (common strings, translation memory) → rule-based checks → local model (Ollama) → frontier model → human. Each step should remove work from the next one, not add re-checking.
- **Lighter models later.** Development and organization run on Opus; day-to-day translation and review must end up working with Sonnet or Haiku. Write instructions and resources so that a smaller model does not have to infer anything.
- **Generic rules only.** Nothing specific to one plugin goes into the rules or the guide.

## How the subprojects feed each other

```
              common strings (.po)
                     │ exact matches, applied first
                     ▼
 review rounds ──► resources/ (guide, glossary notes, translation memory)
      │                 │
      │                 ├──► skill/      (translation skill)
      ▼                 │
 calibration log ──► polyglots/rules ──► polyglots + Ollama (pre-translation, first review)
```

- A mistake seen **once** is a *candidate* (calibration log). It becomes a rule when it repeats, or when the guide or glossary already state it.
- Decisions that set a general criterion go to `resources/` (style guide, moderation guide or translation memory), in Spanish.
- Open questions go to `docs/status.md` until the team or the reviewer decides them.

## Review round

See [review/README.md](../review/README.md).

## Where things go

| What | Where | Language |
|---|---|---|
| Project docs, code, file names, commit messages | `docs/`, scripts | English |
| Style guide, glossary, translation memory, moderation criteria | `resources/` | Spanish |
| Per-round notes and tool calibration | `skill/benchmark-log.md`, `polyglots/calibration-log.md` | Spanish |
| Rounds and temporary files (downloads, experiments) | Outside the repository: `ROUNDS_DIR`, see `CLAUDE.local.md` | — |
