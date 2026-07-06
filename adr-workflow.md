## Architecture Decision Records (ADRs)

Record every feature, fix, infrastructure change, behavior change, or notable
implementation decision in `docs/adr/` using one numbered Markdown file per
decision (for example `0001-add-local-transform-tests.md`).

Each ADR must contain:

- `## Context`
- `## Decision`
- `## Consequences`
- `## Validation`

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