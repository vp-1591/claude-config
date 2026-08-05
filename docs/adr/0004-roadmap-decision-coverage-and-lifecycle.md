# 0004 — Roadmap decision coverage and lifecycle tracking

> **Superseded by [ADR 0005](./0005-remove-custom-review-pipeline.md)** — the `review-consistency` agent it extended was removed; roadmap lifecycle decisions carry forward unchanged, see 0005 §Decision.

## Context

Roadmaps contain Decision points and Alternatives considered that represent
architectural choices. These decisions should eventually be recorded as ADRs,
but nothing checks whether they have been. Completed roadmaps also have no
defined terminal status — they stay `active` indefinitely, and there is no
guidance on when to mark them `completed` or delete them.

When a roadmap is deleted, the review-consistency agent loses visibility into
its decisions because the file is gone from the working tree. The only
checkpoint is the PR that deletes it, where the roadmap content is still
visible in the diff.

## Decision

1. Extend the review-consistency agent (Step 0 and Step 4) to detect deleted
   roadmaps from the PR diff and check that their decision points have
   corresponding ADRs. Also flag active roadmaps whose success criteria are
   all met.

2. Define three roadmap statuses: `active`, `completed`, `abandoned`.

3. Add a roadmap lifecycle section to the ADR workflow (`shared/adr-workflow.md`)
   requiring that before deleting a roadmap, all its decision points and
   alternatives must be covered by ADRs.

4. Add lifecycle hints to the roadmap template (status blockquote, HTML
   comment on success criteria, phase status variants) and the edit-roadmap
   skill (flag completed-but-active roadmaps).

5. Flag rather than auto-change — the review agent and edit-roadmap skill
   report gaps; the user decides what to do.

## Constraints

- No new agents or review steps. The checks extend existing Step 0 and Step 4
  in review-consistency.
- Preserve the existing JSON output format (`reason: "adr_roadmap_consistency"`).
- Deleted roadmaps must be recoverable from the PR diff, not just from the
  working tree.

## Consequences

- **Positive:** Two new categories of documentation gaps surfaced during review
  (uncovered roadmap decisions, stale active roadmaps). Roadmap lifecycle is
  explicit rather than implicit. Deleting a roadmap is safe because ADRs
  preserve the decisions.
- **Negative:** Minor initial noise on the first few reviews until existing
  roadmaps get their decisions promoted to ADRs. The review-consistency agent
  is slightly longer.

## Validation

- Create a roadmap with decision points, run a PR that touches the roadmap's
  code area, verify the review-consistency agent flags decisions without ADRs.
- Mark all success criteria checked on an active roadmap, verify the
  edit-roadmap skill flags the status mismatch.
- Delete a roadmap in a PR where not all decisions have ADRs, verify the
  review-consistency agent flags the uncovered decisions from the diff.