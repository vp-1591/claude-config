---
name: manage-adr
description: Record an important completed change (feature, infra, or behavior change) as an ADR. Not every fix or refactor qualifies — see the gate in the skill body. Invoke after implementation is complete; it is the final step of a change, not a planning step. Do not use for reading existing ADRs; locate them by grepping docs/adr/README.md for the area, connector, or technology involved.
model: sonnet
---
## Architecture Decision Records (ADRs)

Record decisions in `docs/adr/` as one numbered Markdown file per decision
(for example `0001-add-local-transform-tests.md`). Not every change earns an
ADR — create one only when it passes **all three**:

### When to record an ADR

1. **Revert test** — a future reader (human or agent) with no context would
   plausibly undo this in favor of the obvious alternative. A bug fix or
   routine implementation fails here: the *why* doesn't need defending if
   nobody would revert it.
2. **At least two** of these signals:
   - A plausible alternative was rejected for a non-obvious reason.
   - Hard to reverse (public interface, data schema, migration, dependency
     or provider lock-in).
   - Sets or changes a convention other code will inherit.
   - Adds a constraint future work must respect.
   - Knowingly accepts a real downside — the Consequences name a genuine
     negative, not just "the bug is fixed."
   - Crosses a security, privacy, or IAM boundary.
   - The *why* is not recoverable from reading the code alone.
3. **No suppressor**: a bug fix restoring already-intended behavior (a
   correction, not a decision); a one-character / single-config-value / typo
   fix; routine follow-through of an already-recorded ADR; a grab-bag of
   unrelated small fixes (belongs in the PR — split out any one that
   qualifies on its own); a pure internal refactor with no new pattern
   adopted; or the only alternative is "leave the bug."

**Borderline** (exactly one signal, e.g. a convention with no tradeoff):
prefer a code comment (`# Decision: docs/adr/…`, see below) over a full ADR.

Each ADR must contain:

- `## Context` — the problem, motivation, or situation that requires a decision.
  What triggered this ADR? What constraint or requirement forced a choice? Include
  relevant background (existing behavior, technical limitations, user pain) so a
  reader unfamiliar with the project can understand *why* this decision came up.

- `## Decision` — what was chosen and why. State the decision explicitly, then
  explain the reasoning. Include key alternatives considered and why they were
  rejected. A reader should be able to understand not just what was decided, but
  why other options didn't win.

- `## Constraints` — what this decision rules out or must not break. List
  boundaries: things that must remain true (existing connectors keep working, no
  new AWS resources, must support Python 3.11+, etc.) and things that are
  explicitly out of scope. This section prevents scope creep and makes the
  decision's limits clear.

- `## Consequences` — trade-offs, side effects, and follow-up work. What becomes
  easier or harder? What new dependencies or risks does this introduce? What will
  need to change later? Include both positive and negative outcomes.

- `## Validation` — how to verify this decision was implemented correctly. Reference
  specific tests, manual checks, or CI steps that confirm the change works. Vague
  statements like "tests pass" should be replaced with concrete verification: which
  tests, what they assert, what manual steps were performed.

### Workflow

This skill runs after implementation. Before writing the new ADR, locate
relevant existing ADRs by grepping `docs/adr/README.md` for the area,
connectors, and technologies touched, and read them. Skip superseded entries
unless a current ADR cites one as carried forward unchanged. If an active ADR
conflicts with the change, stop and ask the user how to proceed.

After making the change:

1. Create the next numbered ADR — take the next integer above the highest
   `0XXX` row in the index (e.g. `grep -oE "0[0-9]{3}" docs/adr/README.md |
   sort | tail -1`, or read the last rows).
2. If the new ADR explicitly supersedes a relevant ADR you read (either by
   stating so directly or by replacing, removing, rewriting, or redesigning
   the same component), mark that ADR as superseded by:
   - updating its row in `docs/adr/README.md`
   - inserting immediately below its title:
     ```markdown
     > **Superseded by [ADR XXXX](./XXXX-filename.md)** — <reason>.
     ```
3. Update `docs/adr/README.md`:
   - Append one row to the `## Index` table:
     `| XXXX | Title | YYYY-MM-DD | active | — |`
   - If step 2 applied, update only that ADR's existing row:
     `| YYYY | ... | superseded | XXXX |`
4. Do not modify any other README rows or metadata.
5. Do not perform orphan or drift detection.

### Code comments referencing ADRs

When code implements a non-obvious ADR decision — the behavior isn't
inferable from the code alone, or it reverses a prior approach (not routine,
self-explanatory implementation) — add a one-line comment at the decision
point, in the language's native comment syntax:

```
# Decision: docs/adr/0012-....md
```

If the code references an ADR that's superseded, update the comment to point at
the superseding ADR instead.

### Carrying decisions forward unchanged

If a superseding ADR reaffirms part of a superseded ADR's decision without
changing it, don't just say "unchanged" — name the origin, so the reasoning
stays reachable even though the superseded ADR is normally skipped:

- In the superseded ADR's marker: extend the step-2 marker with `; <what carries forward unchanged>, see XXXX §Decision.`
- In the superseding ADR's own Decision section: `<thing> remains unchanged (originally decided in ADR YYYY, §Decision).`
- If XXXX is later superseded itself and still carries that same piece forward, keep the original ADR number in the note (e.g. "unchanged since 0095"), not just the immediate predecessor.
