---
name: create-roadmap
description: Create a roadmap document with clarify-first workflow
allowed-tools: Read(${CLAUDE_PLUGIN_ROOT}/skills/create-roadmap/roadmap-template.md)
model: sonnet
---

Create a roadmap document for this project. Roadmaps live in
`docs/roadmaps/<NNNN>-<topic>.md` (four-digit zero-padded number prefix,
e.g. `0001-ci-pipeline.md`) and use the template defined in
`roadmap-template.md` (in this skill directory, or fallback at
`docs/roadmap-template.md` in the project root).

If the user wants to edit an existing roadmap, suggest using
`/edit-roadmap` instead.

## Overview

This skill follows a clarify-before-draft process: it first gathers context,
then invites the user to share their thinking before asking targeted questions,
and only then writes the document. This reduces iteration cycles by resolving
vagueness up front.

## Process

### Step 1 — Load context

Read these files in order:

1. Relevant ADRs (per the ADR workflow).
2. `docs/roadmaps/README.md` if it exists (the roadmap index — for context
   on what already exists); otherwise all existing roadmaps in
   `docs/roadmaps/*.md`. Do not use prior roadmaps as a starting point for
   this new one.
3. The roadmap template: `roadmap-template.md` in this skill directory. If
   not found, look for `docs/roadmap-template.md` in the project root.
4. The project's `CLAUDE.md` for constraints and environment details.

### Step 2 — Open floor

Before any structured questions, invite the user to share everything they have
in mind: the goal, context, constraints, half-formed ideas, and anything that
feels relevant. Adapt the invitation to what they already told you. Then ask
one soft "anything else?" to surface what they almost forgot.

This dump replaces most downstream questioning — mine it for details before
asking anything structured.

### Step 3 — Clarify gaps

After the open floor, identify remaining gaps by checking each section of the
roadmap template against what the user provided. For each gap, ask a targeted
question. Use the categories below as a checklist:

**Goal:**
- What specific outcome does this roadmap deliver?
- Who is the primary audience (hiring managers, stakeholders, future you)?

**Current state:**
- What already exists? What works, what's missing, what's painful?

**Success criteria:**
- How will you know this roadmap is complete? Each criterion must be
  verifiable: a test, a manual check, or an observable behavior.
- Can you run a command, visit a URL, or inspect a file to confirm each one?

**Alternatives considered:**
- What approaches were evaluated and rejected? One-line reason per rejection.
- If none exist yet, record "None considered yet."

**Phase scope:**
- What are the phases? What does each phase deliver?
- For each phase, what is explicitly out of scope?

Ask 3–5 questions maximum. Group related questions. Skip questions the open
floor already answered. Do not proceed to Step 4 until the user has answered
or confirmed they want to skip a question.

### Step 4 — Resolve ambiguities

Scan everything the user has said so far (open floor, clarification answers)
for ambiguity signals. Do not assume vague terms are precise. Name each
ambiguity and ask the user to resolve it before continuing.

**Ambiguity signals to look for:**

| Signal | Example | Resolution pattern |
|--------|---------|--------------------|
| "or" / "and/or" in scope | "Add CI or deployment pipeline" | Name the fork, present as choices, ask which |
| Vague quantifiers | "various", "some", "etc." | Ask for the specific complete list |
| Conjoined independent goals | "Improve testing and add monitoring" | Split-or-keep decision |
| Fuzzy adjectives | "better UX", "more reliable" | Ask for a specific, testable definition |
| Overloaded terms | "user" meaning buyer, payer, or end-user | Name the ambiguity, ask for a precise choice |

**For each ambiguity found:**

1. Name it clearly: "I see an 'or' here — does this mean X, or Y?"
2. When the options are clear, present them as choices rather than leaving it
   open-ended.
3. Record the resolution in the roadmap's Decision points section.
4. Do not proceed to Step 5 until every ambiguity is resolved or the user
   explicitly defers it (recorded as "deferred" with what's still open).

**If no ambiguities are found**, say so briefly and move to Step 5.

### Step 5 — Confirm understanding

Before writing anything, synthesize what you understood into 2–3 sentences
covering: the goal, what's in scope, and what success looks like.

Present it naturally — do not prefix with "Acknowledging:", "Summarizing:", or
"To confirm:". Use your own words, like a colleague who's really listening.

Then ask: "Is that right? Am I missing anything?"

- If the user confirms, proceed to Step 6.
- If the user corrects or adds something, adjust your understanding and
  reflect back again. Do not proceed until confirmed.

### Step 6 — Draft the roadmap

Draft the roadmap using the template exactly.
Do not invent missing details. If required information is still unknown,
insert `<!-- TODO: ... -->` rather than guessing.

### Step 7 — Self-review

After drafting, review the roadmap against this checklist:

1. **Goal is testable**: Can you verify the roadmap is done without asking
   the author?
2. **Success criteria are specific**: No vague criteria like "works" or
   "is reliable". Each one names what to check and how. See the specificity
   guide below.
3. **Scope is bounded**: Every phase has an "Out of scope" section.
4. **Alternatives are documented**: At least one rejected approach is listed,
   or the section explicitly says none were considered yet.
5. **ADRs are linked**: Relevant decisions reference ADR numbers.
6. **Mission test**: Could a generic assistant write this goal? If yes, it's
   too vague — push for domain-specific language.
7. **Ambiguities resolved**: No unresolved "or", vague quantifiers, or fuzzy
   adjectives remain in the draft. Any deferred decisions are recorded in
   the Decision points section with what's still open.

Report any sections that fail the checklist. The user can accept the draft
as-is or ask for revisions.

### Step 8 — Write the file

Determine the next available number by scanning existing roadmaps in
`docs/roadmaps/`. If `0001-*.md` through `0003-*.md` exist, the next number
is `0004`. If the directory is empty, start at `0001`.

Write the final roadmap to `docs/roadmaps/<NNNN>-<slug>.md` where `<NNNN>`
is the zero-padded number and `<slug>` is a short kebab-case topic name
derived from the goal.

Then update the roadmap index at `docs/roadmaps/README.md`:
- If the index file doesn't exist yet, create it with an `## Index`
  header and table:
  ```markdown
  ## Index

  | # | Title | Date | Status | Notes |
  |---|-------|------|--------|-------|
  ```
- Append one row: `| <NNNN> | <Title> | YYYY-MM-DD | active | — |` using
  the roadmap's number, today's date, and the roadmap's title.

Do not modify any other rows. Do not create ADRs. Do not modify code.

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

- This skill produces a roadmap document only. It does not create ADRs,
  stories, or implementation plans.
- The roadmap feeds into the project workflow: `roadmap → plan mode →
  implement → ADR → review PR`.
- If the user asks to create a roadmap and an ADR for the same topic,
  suggest creating the roadmap first, then using plan mode to implement,
  then creating the ADR for decisions made during implementation.
- To edit an existing roadmap, use `/edit-roadmap`.