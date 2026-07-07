---
name: create-roadmap
description: Create or update a roadmap document with clarify-first workflow
model: sonnet
---

Create or update a roadmap document for this project. Roadmaps live in
`docs/roadmap-<topic>.md` and use the template defined in
`docs/roadmap-template.md`.

## Overview

This skill follows a clarify-before-draft process: it first gathers context,
then probes for ambiguities before writing anything. This reduces iteration
cycles by resolving vagueness up front.

## Process

### Step 1 — Load context

Read these files in order:

1. Relevant ADRs (per the ADR workflow).
2. All existing roadmaps in `docs/roadmap-*.md`.
3. The roadmap template: `docs/roadmap-template.md`.
4. The project's `CLAUDE.md` for constraints and environment details.

If the user specified a topic that already has a roadmap, this is an **update**
operation — the existing roadmap is the starting point, not a blank template.

### Step 2 — Clarify ambiguities

Before writing, identify gaps in the user's request by checking each section
of the roadmap template against what the user provided. For each gap, ask a
targeted question. Use the categories below as a checklist:

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

Ask 3–5 questions maximum. Group related questions. Do not proceed to
Step 3 until the user has answered or confirmed they want to skip a question.

### Step 3 — Draft the roadmap

Draft the roadmap using the template exactly.
Do not invent missing details. If required information is still unknown,
insert `<!-- TODO: ... -->` rather than guessing.

### Step 4 — Self-review

After drafting, review the roadmap against this checklist:

1. **Goal is testable**: Can you verify the roadmap is done without asking
   the author?
2. **Success criteria are specific**: No vague criteria like "works" or
   "is reliable". Each one names what to check and how.
3. **Scope is bounded**: Every phase has an "Out of scope" section.
4. **Alternatives are documented**: At least one rejected approach is listed,
   or the section explicitly says none were considered yet.
5. **ADRs are linked**: Relevant decisions reference ADR numbers.

Report any sections that fail the checklist. The user can accept the draft
as-is or ask for revisions.

### Step 5 — Write the file

Write the final roadmap to `docs/roadmap-<slug>.md` where `<slug>` is a
short kebab-case topic name derived from the goal.

If this is an update to an existing roadmap, write the updated content to the
existing file path.

Do not modify any other files. Do not create ADRs. Do not modify code.

## Notes

- This skill produces a roadmap document only. It does not create ADRs,
  stories, or implementation plans.
- The roadmap feeds into the project workflow: `roadmap → plan mode →
  implement → ADR → review PR`.
- If the user asks to create a roadmap and an ADR for the same topic,
  suggest creating the roadmap first, then using plan mode to implement,
  then creating the ADR for decisions made during implementation.