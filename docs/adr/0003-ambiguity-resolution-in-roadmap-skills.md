# ADR 0003: Ambiguity resolution in roadmap skills

## Context

The roadmap skills (`create-roadmap` and `edit-roadmap`) relied entirely on the model's general language understanding to detect vague or ambiguous requirements during their clarify-first workflow. There was no explicit mechanism to:

- Detect "or" in scope bullet points (e.g., "Add CI or deployment pipeline")
- Catch other ambiguity signals like vague quantifiers ("various", "etc."), fuzzy adjectives ("better UX"), or overloaded terms ("user" meaning buyer vs payer)
- Force resolution before drafting — the model could silently pick one interpretation and proceed
- Record which choices were made and why, leaving future readers unable to understand the reasoning

This meant roadmaps could contain unresolved forks that the model resolved by assumption rather than by asking the user, leading to drafts that didn't match the user's intent and required extra iteration cycles.

The _bmad framework (v6.10.0) has battle-tested patterns for this problem:
- **Forge Idea** explicitly names overloaded terms and forces a precise choice before continuing
- **Clarify-and-Route** uses numbered questions that must ALL be answered before proceeding
- **Discovery Conversation Guide** uses a reflect-confirm-proceed loop: listen, reflect back in natural language, wait for confirmation
- **Multi-Goal Check** detects independent goals and forces a split-or-keep decision

## Decision

Add three mechanisms to the roadmap skills, each inspired by a _bmad pattern but stripped down for lighter token usage:

1. **Ambiguity scan step** (inspired by Forge Idea's term-precision rule and Clarify-and-Route's multi-goal check) — A new step between clarification and drafting that scans all user input for ambiguity signals ("or"/"and/or", vague quantifiers, conjoined independent goals, fuzzy adjectives, overloaded terms). For each found, the step names the ambiguity, presents choices when the options are clear, and blocks until resolved or explicitly deferred. Added to both `create-roadmap` (as Step 4) and `edit-roadmap` (as Step 3).

2. **Reflect-confirm gate** (inspired by the Discovery Conversation Guide's reflect-confirm-proceed loop) — A new step that synthesizes understanding into 2–3 natural sentences and asks "Is that right?" before any drafting or editing begins. Blocks until the user confirms or corrects. Added to both skills (as Step 5 in create-roadmap, Step 4 in edit-roadmap).

3. **Decision points section in the roadmap template** (inspired by Forge Idea's memlog) — A new `## Decision points` table between "Alternatives considered" and "Phases" that records each choice resolved during clarification (Decision | Options considered | Chosen | Why). This gives future readers an audit trail and makes it easy for `/edit-roadmap` to revisit decisions.

The self-review checklists in both skills were extended with a check that no unresolved ambiguities remain and that deferred decisions are recorded.

## Constraints

- No new scripts or external dependencies — everything is implemented as instructions in the skill markdown files.
- Token overhead must stay minimal — the ambiguity table and confirm prompt add ~200 tokens per invocation, not the 73 elicitation methods or persona system that _bmad uses.
- The roadmap template structure must remain backward-compatible — existing roadmaps without a Decision points section must still be valid.
- The edit-roadmap skill must stay "surgical" — ambiguity resolution only applies to sections the user wants to change, not the entire document.

## Consequences

- Roadmaps will have fewer silent assumptions because the model must surface "or" forks and other ambiguities before drafting.
- Iteration cycles should decrease because the reflect-confirm gate catches misunderstandings that structured questions miss.
- Decision points create an audit trail that helps future readers (and future `/edit-roadmap` invocations) understand why certain choices were made.
- The clarify-first workflow is now longer (8 steps instead of 6 for create-roadmap, 7 instead of 5 for edit-roadmap) but each step is lightweight and many can be skipped (e.g., "no ambiguities found" moves straight through).
- The ambiguity signal table is a heuristic — it won't catch every possible ambiguity. The reflect-confirm gate serves as a safety net for anything the scan misses.

## Validation

- Manual test: invoke `/create-roadmap` with a scope containing "or" (e.g., "Add linting or type checking") and verify the model surfaces the fork and asks which one.
- Manual test: invoke `/create-roadmap` with a vague adjective (e.g., "better performance") and verify the model asks for a testable definition.
- Manual test: invoke `/edit-roadmap` on an existing roadmap and request a change containing an ambiguity — verify the resolve step fires.
- Verify that existing roadmaps without a Decision points section are still valid (backward compatibility).