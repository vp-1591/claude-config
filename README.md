# claude-config

Version control for my Claude Code configuration files, plus a lightweight harness for structured AI-assisted development.

## Why

AI-assisted development drifts without structure: decisions get made and forgotten, plans go stale. This repo adds just enough process to prevent that — roadmaps for forward-looking plans, ADRs as permanent decision records, and review-time consistency checks — while staying small enough to fit the token budget of a side project. Anything Claude Code already does well (planning, editing, reviewing) is reused rather than reimplemented.

## What's included

### Skills

| Skill | Description |
|-------|-------------|
| `create-roadmap` | Clarify-first roadmap drafting — asks targeted questions before writing to reduce iteration cycles |
| `edit-roadmap` | Surgically edit an existing roadmap, preserving structure and unchanged sections |
| `manage-adr` | Create, update, or supersede ADRs after implementation is complete |
| `junction` | Windows junction linking for skill directories into `~/.claude/skills/` |

### Agents

| Agent | Description |
|-------|-------------|
| `plan-auditor` | Reviews a written implementation plan, before any code is written, for weak-mock anti-patterns and DRY/YAGNI/SOLID violations |

### Commands

| Command | Description |
|---------|-------------|
| `investigate` | Find root cause and report — investigation only, no fix, to keep investigation out of the fix context |
| `planner` | Write a plan, then review it for YAGNI/DRY/KISS/SOLID violations before implementation |
| `mermaid` | Create a mermaid diagram |
| `pre-compact` | Write plan status, problems, and next steps to `tmp/PROGRESS.md` before compacting |

### Hooks

| Path | Description |
|------|-------------|
| `hooks/settings.json` | Version-controlled mirror of the `hooks` section in `~/.claude/settings.json` |
| `hooks/*.py` | Hook scripts — lint (ruff, pyright) and guard against reading dotenv files — plus tests |

### Config

| Path | Description |
|------|-------------|
| `global/CLAUDE.md` | Version-controlled source for `~/.claude/CLAUDE.md` (linked via file symlink) |
| `opencode.json` | opencode config; imports `shared/adr-workflow.md` |

### Shared

| Path | Description |
|------|-------------|
| `shared/adr-workflow.md` | Architecture Decision Record workflow guidelines (opt-in, imported per project) |

### Docs

| Path | Description |
|------|-------------|
| `docs/adr/` | Project ADRs, indexed in `docs/adr/README.md` |