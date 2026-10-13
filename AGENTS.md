## Goal
Version control and develop lightweight harness that helps follow better methodologies when developing with ai (similar to BMAD but customized for lighter token usage and smaller projects).

## Skill setup
Skills, commands, agents, and hooks ship as the `config` plugin (repo root is the plugin root — see `.claude-plugin/`). Install once per machine:

```
claude plugin marketplace add <path-to-this-repo>
claude plugin install config@claude-config --scope user
```

The marketplace entry uses a relative source path, so the plugin loads in place from the working tree — repo edits are live on the next session start or `/reload-plugins`, no reinstall needed.

The `/junction` skill is now only for what the plugin cannot ship: junctioning `shared/` into a project's `.claude/` and symlinking `global/CLAUDE.md` to `~/.claude/CLAUDE.md`.

## Global config setup
`global/CLAUDE.md` is the version-controlled source for `~/.claude/CLAUDE.md` (user-level instructions). It's linked via a **file symlink** (created with developer mode enabled). Edits in either location update the same file on disk. Unlike hard links, symlinks survive atomic saves and git checkout without breaking.

## Shared directory

Files in shared directory are opt-in and are imported only to projects that need it. It is intentional and these files must not be leaked to user level CLAUDE.md. This project imports `shared/adr-workflow.md` — see CLAUDE.md (Claude Code) and `opencode.json` instructions (opencode).

## Prompt evals (pending)

Before making substantial changes to skills or harness instructions, consider
whether prompt evals are in place first. Without evals, it's hard to tell if a
change improves or regresses behavior. See
`todo-prompt-evals.md` in project memory for context.
