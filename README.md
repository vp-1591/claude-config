# claude-config

Version control for my claude code files and lightweight Claude Code harness for structured AI-assisted development. Similar in spirit to [BMAD](https://github.com/BMAD-code-org/BMAD-METHOD) but optimized for smaller projects and lower token usage.

## Design philosophy

The key insight: **not every step in an AI workflow needs AI judgment**. This repo draws explicit boundaries between what a model should decide and what a script should enforce:

- **Deterministic boundaries** — steps like eligibility checks, issue filtering, and link building are scripted (`review-context`, `review-filter`, `review-link`). No tokens spent on decisions that have one right answer.
- **Model selection per step** — Sonnet for reasoning-heavy work like bug scanning and security review, no heavier model than the step needs. No step over-provisioned.
- **Parallel subagents** — bug scanning and security review run concurrently because they're independent. The pipeline waits only where steps depend on each other.
- **Evidence flags over confidence scores** — the issue scorer returns verifiable boolean flags ("does the diff actually contain this pattern?"), not subjective confidence percentages. A fixed decision table then filters — no LLM needed for the final call.

## What's included

### Skills

| Skill | Description |
|-------|-------------|
| `review` | Multi-step automated PR review: context gathering → obvious-noise pre-filter → parallel bug/security/consistency scan → batched scoring → deterministic filter → post |
| `create-roadmap` | Clarify-first roadmap drafting — asks targeted questions before writing to reduce iteration cycles |
| `edit-roadmap` | Surgically edit an existing roadmap, preserving structure and unchanged sections |
| `junction` | Windows junction linking for skill directories into `~/.claude/skills/` |

### Agents

| Agent | Description |
|-------|-------------|
| `review-bug-scanner` | Shallow-scan PR diffs for obvious bugs and CLAUDE.md compliance violations |
| `review-security` | Scan PR diffs for security concerns — injection, auth issues, leaked secrets |
| `review-consistency` | Check that a PR's code, ADRs, and roadmaps agree with each other and with pre-existing active scope |
| `review-issue-scorer` | Batch-score review issues using evidence flags (not confidence scores) |

### Shared

| Path | Description |
|------|-------------|
| `shared/adr-workflow.md` | Architecture Decision Record workflow guidelines |

> **Dependency note:** `review-consistency` assumes the target repo has opted
> into `shared/adr-workflow.md` (via `@~/.claude/shared/adr-workflow.md` in
> that repo's own `CLAUDE.md`, as this repo does for itself). This is a
> per-project opt-in, not a global default — without it, `docs/adr/` won't
> exist and the "missing ADR" check in `review-consistency` Step 4 will flag
> noise on every substantive PR.

### Docs

| Path | Description |
|------|-------------|
| `docs/adr/` | Project ADRs, indexed in `docs/adr/README.md` — read directly by `review-consistency` rather than discovered at runtime |

## Setup

Use the junction skill to link skill directories into `~/.claude/skills/`:

```
/junction
```

This creates Windows directory junctions (not file symlinks) so that scripts and other assets within skill folders are included.