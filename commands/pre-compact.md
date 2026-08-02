---
name: pre-compact
description: >-
  Write plan, plan status, problems, modified files, verification, blockers and next steps to tmp/PROGRESS.md before compacting
disable-model-invocation: true
---
Before we compact context, write our current progress to `tmp/PROGRESS.md`
in the project root (read and overwrite it if it exists, create if it doesn't).

Include, in this structure:

## Plan
Link or path to the plan being implemented, plus a one-line restatement 
of the overall goal.

## Plan status
Go through the plan step by step: which steps are done, in progress, 
not started, or skipped/changed. If any step was implemented 
differently than planned, say what changed and why.

## Problems encountered
For each nontrivial problem hit during implementation:
- what broke / what the symptom was (include the actual error output, 
  not a paraphrase)
- root cause, if known
- how it was resolved, or its current status if unresolved
- any workaround or deviation from the plan this forced

Skip trivial fixes (typos, obvious syntax errors). Include anything that 
took more than a couple tries, anything where the fix isn't obvious from 
the diff, and anything where the root cause isn't fully understood yet.

## Modified/created files
List every file touched this session and what changed in it, one line each.

## Verification
Exact commands to run to check things still work (tests, lint, build, 
manual repro steps) — and their last known result.

## Open blockers / unresolved questions
Anything still stuck, with relevant error output or reasoning, so I don't 
have to re-debug from scratch.

## Next steps
The immediate next 1-3 actions, in order, tied back to the plan.

Keep it dense and skimmable — this is a working document for you to 
re-read after compaction, not a report for a human. Don't include 
anything regenerable by reading the current code/git diff or the plan 
file itself; only include what would otherwise be lost.

After writing the file, confirm it's saved, then proceed with /compact.