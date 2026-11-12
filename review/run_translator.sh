#!/bin/zsh
# Translator session for a round, run as a real user of the skill would run it:
# a separate headless Claude Code session with only the packaged plugin (dist/ zip),
# in an empty folder outside the repository, so it sees no CLAUDE.md of this project,
# no resources/ and no other rounds. No transcript is saved and auto-memory is off, so
# nothing carries over from one round to the next.
#
# Usage: review/run_translator.sh <sandbox-dir> "<what the user would say>" <log.jsonl> [model] [file]
#   <sandbox-dir>  a folder outside the repository; it is emptied first. Always use the same
#                  one, so Claude Code keeps at most one project entry for it.
#   <log.jsonl>    stream-json log: every tool call, the final answer, usage and duration.
#                  Summarize it with: python3 review/run_summary.py <log.jsonl>
#   [file]         a .po/.pot to review or translate; it is copied into the empty sandbox.
# Run python3 skill/package.py first, so the zip is current.
set -e
REPO=${0:A:h:h}
SANDBOX=${1:A}
case "$SANDBOX/" in
  "$REPO"/*) echo "The sandbox must be outside the repository." >&2; exit 1 ;;
esac
PLUGIN="$SANDBOX.plugin"
rm -rf "$SANDBOX" "$PLUGIN"
mkdir -p "$SANDBOX" "$PLUGIN"
unzip -q "$REPO/dist/wordpress-translator-es.zip" -d "$PLUGIN"
[ -n "$5" ] && cp "${5:A}" "$SANDBOX/"
LOG=${3:A}
cd "$SANDBOX"
claude -p "$2" --model "${4:-haiku}" \
  --plugin-dir "$PLUGIN/wordpress-translator-es" \
  --no-session-persistence \
  --settings '{"autoMemoryEnabled": false}' \
  --allowedTools Read Write Edit Glob Grep Skill "Bash(python3 *)" "Bash(mkdir *)" "Bash(ls *)" \
    "Bash(msgfmt *)" "Bash(cp *)" "Bash(mv *)" "Bash(wc *)" "Bash(head *)" \
  --output-format stream-json --verbose > "$LOG" 2>&1
