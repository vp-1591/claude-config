---
name: edit-roadmap
description: Surgically edit an existing roadmap document
allowed-tools: Read(${CLAUDE_PLUGIN_ROOT}/skills/create-roadmap/roadmap-template.md)
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

1. Ask the user which roadmap to edit (number, topic name, or file path).
2. Read the existing roadmap file from `docs/roadmaps/<NNNN>-<topic>.md`. If not found,
   suggest using `/create-roadmap` to create one first, then stop.
3. Read the roadmap template: `roadmap-template.md` in the `create-roadmap`
   skill directory. If not found, look for `docs/roadmap-template.md` in the
   project root.
4. Read `docs/adr/README.md` (the ADR index) if it exists, otherwise
   relevant ADRs directly, plus the project's `CLAUDE.md` for context.

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

### Step 3 — Resolve ambiguities

If the user's requested changes introduce or modify scope, success criteria, or
any section where ambiguity could hide, scan the change description for
ambiguity signals. Do not assume vague terms are precise. Name each ambiguity
and ask the user to resolve it.

**Ambiguity signals to look for:**

| Signal | Example | Resolution pattern |
|--------|---------|--------------------|
| "or" / "and/or" in scope | "Add CI or deployment pipeline" | Name the fork, present as choices, ask which |
| Vague quantifiers | "various", "some", "etc." | Ask for the specific complete list |
| Conjoined independent goals | "Improve testing and add monitoring" | Split-or-keep decision |
| Fuzzy adjectives | "better UX", "more reliable" | Ask for a specific, testable definition |
| Overloaded terms | "user" meaning buyer, payer, or end-user | Name the ambiguity, ask for a precise choice |

For each ambiguity found, name it clearly and present choices when the options
are clear. Record resolutions in the roadmap's Decision points section (add
rows to the existing table). Do not proceed until every ambiguity is resolved
or explicitly deferred.

If no ambiguities are found, say so briefly and move to Step 4.

### Step 4 — Confirm understanding

Before making edits, reflect back what you understood needs to change and what
the result should look like — in your own words, naturally, without labels like
"Summarizing:" or "To confirm:".

Ask: "Is that right? Anything I'm missing?"

- If confirmed, proceed to Step 5.
- If corrected, adjust and reflect back again. Do not proceed until confirmed.

### Step 5 — Edit surgically

Rewrite only the affected sections. Preserve all unchanged sections verbatim —
do not rephrase, reformat, or "improve" sections the user didn't ask to change.

For each edit:
- Ensure the change directly addresses the user's stated problem.
- Keep the section's structure consistent with the template.
- If required information is still unknown after clarification, insert
  `<!-- TODO: ... -->` rather than guessing.

### Step 6 — Self-review

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
8. **Ambiguities resolved**: No unresolved "or", vague quantifiers, or fuzzy
   adjectives remain in the changed sections. Any deferred decisions are
   recorded in the Decision points section with what's still open.

Report any sections that fail the checklist. The user can accept the draft
as-is or ask for revisions.

### Step 7 — Write and summarize

Write the updated roadmap to the same file path it was loaded from.

If `docs/roadmaps/README.md` exists, update this roadmap's row:
- Refresh the Title column if the title changed.
- Update the Status column only if the user explicitly asked to change
  the roadmap's status (e.g. marking it completed or superseded) — don't
  infer status changes from phase edits on your own.
- Add a short note in the Notes column only if the edit is significant
  enough that a future reader scanning the index should know about it
  (e.g. "scope narrowed", "phase 2 added"). Leave it as `—` for minor
  edits.
- Leave the Created date and number untouched.
- If the index file doesn't exist, don't create it here — that's
  `/create-roadmap`'s responsibility.

Do not modify any other files or index rows. Do not create ADRs. Do not
modify code.

After writing, provide a change summary listing each section that changed
and what changed in it. Example:

```
Changed sections:
- Goal: tightened language from "improve reliability" to "p99 latency < 200ms"
- Phase 2 scope: added "database migration script" to deliverables
- Success criteria: replaced "works correctly" with "all integration tests pass"
- Index: updated Status to "completed"
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