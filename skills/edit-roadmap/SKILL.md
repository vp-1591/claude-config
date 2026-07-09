---
name: edit-roadmap
description: Surgically edit an existing roadmap document
model: sonnet
---

Surgically edit an existing roadmap document. This skill preserves the
structure and unchanged sections of an existing roadmap, making only targeted
updates based on what the user wants to change.

If no roadmap exists yet for the topic, suggest using `/create-roadmap` first.

## Overview

This skill is the edit counterpart to `/create-roadmap`. Where that skill builds
a new roadmap from scratch, this one takes an existing roadmap and makes focused,
surgical changes — rewriting only the sections that need to change and preserving
everything else verbatim.

The process follows BMAD's edit guidance: understand what's not working before
proposing changes, assess whether edits cascade across sections, and validate
after every change.

## Process

### Step 1 — Load the roadmap

1. Ask the user which roadmap to edit (topic name or file path).
2. Read the existing roadmap file from `docs/roadmap-<topic>.md`. If not found,
   suggest using `/create-roadmap` to create one first, then stop.
3. Read the roadmap template: `roadmap-template.md` in the `create-roadmap`
   skill directory. If not found, look for `docs/roadmap-template.md` in the
   project root.
4. Read relevant ADRs and the project's `CLAUDE.md` for context.

### Step 2 — Understand what needs to change

Ask the user what's not working the way they want. Let them describe the problem
in their own words first — do not jump to structured questions.

Then assess the cascade:
- **Local change**: affects one section (e.g., updating success criteria for
  one phase). Proceed with a surgical edit to that section only.
- **Cascading change**: ripples across multiple sections (e.g., changing the
  goal affects phases, success criteria, and alternatives). Ask which sections
  are affected before proceeding.

For each section being changed, ask targeted clarification questions — but
only for that section. Skip clarification for sections that are staying the
same.

Ask 3–5 questions maximum. Group related questions. Do not proceed to Step 3
until the user has answered or confirmed they want to skip a question.

### Step 3 — Edit surgically

Rewrite only the affected sections. Preserve all unchanged sections verbatim —
do not rephrase, reformat, or "improve" sections the user didn't ask to change.

For each edit:
- Ensure the change directly addresses the user's stated problem.
- Keep the section's structure consistent with the template.
- If required information is still unknown after clarification, insert
  `<!-- TODO: ... -->` rather than guessing.

### Step 4 — Self-review

After editing, review the updated roadmap against this checklist:

1. **Goal is testable**: Can you verify the roadmap is done without asking
   the author?
2. **Success criteria are specific**: No vague criteria like "works" or
   "is reliable". Each one names what to check and how. See the specificity
   guide below.
3. **Scope is bounded**: Every phase has an "Out of scope" section.
4. **Alternatives are documented**: At least one rejected approach is listed,
   or the section explicitly says none were considered yet.
5. **ADRs are linked**: Relevant decisions reference ADR numbers.
6. **Structure preserved**: All sections from the template are present. No
   sections were accidentally removed or reordered.
7. **Mission test**: Could a generic assistant write this goal? If yes, it's
   too vague — push for domain-specific language.

Report any sections that fail the checklist. The user can accept the draft
as-is or ask for revisions.

### Step 5 — Write and summarize

Write the updated roadmap to the same file path it was loaded from.
Do not modify any other files. Do not create ADRs. Do not modify code.

After writing, provide a change summary listing each section that changed
and what changed in it. Example:

```
Changed sections:
- Goal: tightened language from "improve reliability" to "p99 latency < 200ms"
- Phase 2 scope: added "database migration script" to deliverables
- Success criteria: replaced "works correctly" with "all integration tests pass"
```

## Specificity guide

Every success criterion must answer: **what failure does this prevent?**
If you can't name the failure, the criterion is too vague.

| Vague ❌ | Specific ✅ |
|----------|------------|
| "System works" | "All tests in `test/` pass, `make lint` is clean" |
| "Is reliable" | "Handles 1000 req/s with p99 < 200ms" |
| "Better UX" | "New user completes signup in < 2 minutes without help" |
| "Easy to maintain" | "A new team member can deploy a change in < 1 hour" |
| "Good performance" | "Page load time < 3s on 3G connection" |

## Notes

- This skill edits an existing roadmap only. To create a new one, use
  `/create-roadmap`.
- This skill preserves unchanged sections verbatim. It does not rephrase or
  reformat sections the user didn't ask to change.
- The roadmap feeds into the project workflow: `roadmap → plan mode →
  implement → ADR → review PR`.
- If the user's requested changes are so extensive that most sections need
  rewriting, suggest using `/create-roadmap` to draft a fresh roadmap instead.