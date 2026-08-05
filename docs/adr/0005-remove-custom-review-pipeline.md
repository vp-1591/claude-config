# 0005 — Replace custom review pipeline with Claude Code built-in review

## Context

This repo previously maintained a custom multi-step PR review pipeline: a
`review` skill that orchestrated four subagents (`review-bug-scanner`,
`review-security`, `review-consistency`, `review-issue-scorer`) with helper
scripts (`review-context`, `review-filter`, `review-find-claude`,
`review-link`, `review-post`) and their tests. The pipeline was built to give
deterministic boundaries (scripted pre-filtering and link building), model
selection per step, parallel bug/security scanning, and evidence-flag scoring.

Maintaining this pipeline cost ongoing effort: scripts, tests, ADRs, and
incremental fixes (e.g. ADR 0001, a Windows UTF-8 fix for `review-context`).
Claude Code ships built-in review skills — `/review` for GitHub pull requests
and `/code-review` for the working diff — that cover the same ground with
upstream support and continuous improvement. The decision was made to stop
maintaining a custom pipeline and rely on the built-in skill instead.

## Decision

Remove the custom review agents (`agents/review-*.md`), the `review` skill
(`skills/review/`), and all review helper scripts and their tests. Use Claude
Code's built-in review (`/review` for GitHub PRs, `/code-review` for the
working diff) for PR review going forward. No custom review agents or skills
will be maintained to replace them.

The roadmap-lifecycle conventions introduced by ADR 0004 remain unchanged
(originally decided in ADR 0004, §Decision): the three roadmap statuses
(`active`, `completed`, `abandoned`), the requirement in
`shared/adr-workflow.md` that all decision points be covered by ADRs before a
roadmap is deleted, the lifecycle hints in the roadmap template, and the
`edit-roadmap` skill's flagging of completed-but-active roadmaps. These live
in the roadmap skills and `shared/adr-workflow.md`, which are independent of
the review pipeline.

## Constraints

- The roadmap lifecycle conventions (statuses, delete-gate, template hints,
  `edit-roadmap` flagging) must remain in force — they do not depend on the
  review pipeline.
- No new review agents or skills may be added to replace the removed ones.
- `README.md` must not reference the removed agents, skill, or scripts.
- ADR 0001 (UTF-8 encoding for `review-context`) is superseded: the script it
  described no longer exists, and nothing carries forward.

## Consequences

- **Positive:** No ongoing maintenance burden for scripts, tests, and ADR
  fixes in the review pipeline. Built-in review improves upstream and is
  already wired into Claude Code.
- **Negative:** The custom consistency checks are lost: `review-consistency`
  automatically flagged roadmap decisions without ADRs and stale
  `active` roadmaps from PR diffs. Those checks now rely on the instructions
  in `shared/adr-workflow.md` and the `edit-roadmap` skill rather than an
  automated reviewer. Deterministic noise pre-filtering, per-step model
  selection, and evidence-flag scoring are also gone — the built-in review
  covers the same ground but not with the same pipeline characteristics.
- **Neutral:** `agents/` and `skills/review/` are removed from the repo and
  from `~/.claude` junctions.

## Validation

- `git ls-files | grep -E "agents/review-|skills/review"` returns nothing.
- `grep -riE "review-context|review-consistency|review-issue-scorer|review-bug-scanner|review-security" .` returns nothing outside `docs/adr/` historical records.
- `README.md` no longer lists the `review` skill or the review agents.
- `/review` on a GitHub PR (or `/code-review` on the working diff) invokes Claude Code's built-in review.
- `docs/adr/README.md` marks 0001 and 0004 as superseded by this ADR.
