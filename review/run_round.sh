#!/bin/zsh
# One training round: the isolated translator session in its sandbox, then the whole sandbox
# copied into rounds/<NN-slug>/ and the sandbox emptied.
# Usage: review/run_round.sh <sandbox-dir> <NN-slug> "<what the user would say>" [file]
#   [file]  the .po to review or translate (usually the one glotpress.py prepare wrote in
#           rounds/<NN-slug>/); it is copied into the empty sandbox.
# MODEL=sonnet (or another) instead of haiku. WORKFLOW=1 and KEEP_SESSION=1 are passed on to run_translator.sh.
set -e
REPO=${0:A:h:h}
SB=${1:A}
R=$REPO/rounds/$2
mkdir -p $R
$REPO/review/run_translator.sh $SB "$3" $R/run.jsonl ${MODEL:-haiku} ${4:+"$4"} < /dev/null
cp -R $SB/. $R/
rm -rf ${SB:?}/*(N)
python3 $REPO/review/run_summary.py $R/run.jsonl | sed -n '/^Duration/,$p'
