## ADRs
Before changing code in an area with existing ADRs, locate the relevant ADRs by
grepping the index `docs/adr/README.md` for the area name plus every connector
or broker name and key technology involved (no skill needed for this — it's a
plain file read). The index is a flat static table, so grep is exact; the only
risk is recall, so search several terms. If nothing matches and the area is
broad, fall back to grepping ADR file contents (`grep -ril <term> docs/adr/`)
and then to reading the whole index. Skip superseded entries for
decision-making, but consult them if a current ADR cites one as "carried forward
unchanged."

When planning a change, include "record ADR" as the final step of the plan —
do not invoke the manage-adr skill during planning. After implementation is
complete, you MUST invoke the manage-adr skill to create, update, or supersede
the ADR. Do not hand-write or copy-template an ADR file yourself — the required
sections (Context, Decision, Constraints, Consequences, Validation) are defined
in the skill, so read existing ADRs only to understand prior decisions, never to
learn the format.

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

## PR review: ADR/roadmap consistency

When reviewing a PR (built-in `/review` or `/code-review`), verify that its
code, ADR(s), and roadmap(s) stay consistent with each other and with
pre-existing active decisions. Read `docs/adr/README.md` and
`docs/roadmaps/README.md` (the indexes) before reviewing; treat any `active`
ADR as binding and skip `superseded` rows.

Check:

- **Docs agree** — if the PR touches both an ADR and a roadmap, their
  decisions must make compatible technical claims. Flag only concrete textual
  conflicts (quote the line in each), and judge which document's reasoning
  fits the PR's goal rather than defaulting to "the ADR wins."
- **Code matches docs** — the diff's code must implement the decision in the
  ADR/roadmap it touches. Flag only where a specific line contradicts it.
- **No violations of prior docs** — the diff must not break a constraint in an
  active ADR it didn't touch, or do something a roadmap's "Out of scope" list
  excludes.
- **Missing ADR** — a PR with a notable feature/fix/behavior/infra change
  should add an ADR, or its description/commits should say why not. Flag
  otherwise.
- **Supersede, don't rewrite** — substantive edits to an active ADR's recorded
  decision are a process violation; new decisions get a new ADR that
  supersedes the old one.
- **Roadmap decisions need ADRs** — for a touched or deleted roadmap, each
  filled-in Decision point should be covered by an active ADR (same
  component/feature in title or Context, or linked by number).
- **Completed roadmaps** — flag active roadmaps whose success criteria are all
  met; they should be `completed` or deleted.
