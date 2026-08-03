## ADRs
Before changing code in an area with existing ADRs, locate the relevant ADRs by
grepping the index `docs/adr/README.md` for the area name plus every connector
or broker name and key technology involved (no skill needed for this — it's a
plain file read). The index is a flat static table, so grep is exact; the only
risk is recall, so search several terms. If nothing matches and the area is
broad, fall back to grepping ADR file contents (`grep -ril <term> docs/adr/`)
and then to reading the whole index. Take the next ADR number from the highest
numbered row. Skip superseded entries for decision-making, but consult them if
a current ADR cites one as "carried forward unchanged."

When planning a change, include "record ADR" as the final step of the plan —
do not invoke the manage-adr skill during planning. After implementation is
complete, you MUST invoke the manage-adr skill to create, update, or supersede
the ADR. Do not hand-write or copy-template an ADR file yourself.

## Roadmap lifecycle

Roadmaps are forward-looking plans. ADRs are permanent decision records. When a
roadmap's decisions have been implemented and recorded as ADRs, the roadmap has
served its purpose.

**Statuses:** `active` (in progress), `completed` (all success criteria met),
`abandoned` (no longer pursuing).

**Before deleting a roadmap**, verify every Decision point and Alternatives
considered entry is covered by an ADR. If an ADR exists for each, delete the
roadmap and remove its row from `docs/roadmaps/README.md`. If gaps remain,
create the missing ADRs first.

**When all success criteria are met**, mark the roadmap `completed` in the
index (via `/edit-roadmap`) or delete it — do not leave completed roadmaps
marked `active`.
