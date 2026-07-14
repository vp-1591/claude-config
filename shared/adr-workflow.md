## Architecture Decision Records (ADRs)

Record every feature, fix, infrastructure change, behavior change, or notable
implementation decision in `docs/adr/` using one numbered Markdown file per
decision (for example `0001-add-local-transform-tests.md`).

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

Before making changes:

1. Read `docs/adr/README.md` if it exists; otherwise read all ADRs in
   `docs/adr/`.
2. Read ADRs relevant to the area being modified.
3. Ignore ADRs marked with:
   ```markdown
   > **Superseded by ADR XXXX**
   ```
4. If an active ADR conflicts with the requested change, stop and ask the user
   how to proceed.

After making the change:

1. Create the next numbered ADR.
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

When a piece of code implements a non-obvious decision from an ADR — the
correct behavior isn't inferable from reading the code alone, or this code
reverses/replaces a prior approach — add a one-line comment at the decision
point, in the language's native comment syntax:

```
# Decision: docs/adr/0012-....md
```

Do not add this for routine implementation of an ADR's decision where the
code is self-explanatory.

If the code references an ADR that's superseded, update the comment to point at
the superseding ADR instead.