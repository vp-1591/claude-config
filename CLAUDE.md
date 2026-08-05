## Goal
Version control and develop lightweight harness that helps follow better methodologies when developing with ai (similar to BMAD but customized for lighter token usage and smaller projects).

## Skill setup
Use the `/junction` skill to link skill directories from this repo into `~/.claude/skills/`. Do not create single-file symlinks — always junction the whole skill directory so that scripts and other assets are included.

## Global config setup
`global/CLAUDE.md` is the version-controlled source for `~/.claude/CLAUDE.md` (user-level instructions). It's linked via a **file symlink** (created with developer mode enabled). Edits in either location update the same file on disk. Unlike hard links, symlinks survive atomic saves and git checkout without breaking.

## Shared directory

Files in shared directory are opt-in and are imported only to projects that need it. It is intentional and these files must not be leaked to user level CLAUDE.md

@~/.claude/shared/adr-workflow.md

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

## Prompt evals (pending)

Before making substantial changes to skills or harness instructions, consider
whether prompt evals are in place first. Without evals, it's hard to tell if a
change improves or regresses behavior. See
`todo-prompt-evals.md` in project memory for context.

> **Note:** This is a soft reminder, not a hard gate. If the change is urgent
> or trivial, proceed — but add an eval afterward.
