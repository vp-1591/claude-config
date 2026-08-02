## Goal
Version control and develop lightweight harness that helps follow better methodologies when developing with ai (similar to BMAD but customized for lighter token usage and smaller projects).

## Skill setup
Use the `/junction` skill to link skill directories from this repo into `~/.claude/skills/`. Do not create single-file symlinks — always junction the whole skill directory so that scripts and other assets are included.

## Global config setup
`global/CLAUDE.md` is the version-controlled source for `~/.claude/CLAUDE.md` (user-level instructions). It's linked via a **file symlink** (created with developer mode enabled). Edits in either location update the same file on disk. Unlike hard links, symlinks survive atomic saves and git checkout without breaking.

## Shared directory

Files in shared directory are opt-in and are imported only to projects that need it. It is intentional and these files must not be leaked to user level CLAUDE.md

@~/.claude/shared/adr-workflow.md

## Prompt evals (pending)

Before making substantial changes to skills or harness instructions, consider
whether prompt evals are in place first. Without evals, it's hard to tell if a
change improves or regresses behavior. See
`todo-prompt-evals.md` in project memory for context.

> **Note:** This is a soft reminder, not a hard gate. If the change is urgent
> or trivial, proceed — but add an eval afterward.
