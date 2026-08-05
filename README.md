# claude-config

Version control for my claude code files and lightweight Claude Code harness for structured AI-assisted development. Similar in spirit to [BMAD](https://github.com/BMAD-code-org/BMAD-METHOD) but optimized for smaller projects and lower token usage.

## Design philosophy

The key insight: **not every step in an AI workflow needs AI judgment**. The harness keeps workflows lightweight by relying on Claude Code's built-in capabilities where they exist, and scripted deterministic steps where a decision has one right answer.

## What's included

### Skills

| Skill | Description |
|-------|-------------|
| `create-roadmap` | Clarify-first roadmap drafting — asks targeted questions before writing to reduce iteration cycles |
| `edit-roadmap` | Surgically edit an existing roadmap, preserving structure and unchanged sections |
| `manage-adr` | Create, update, or supersede ADRs after implementation is complete |
| `junction` | Windows junction linking for skill directories into `~/.claude/skills/` |

### Shared

| Path | Description |
|------|-------------|
| `shared/adr-workflow.md` | Architecture Decision Record workflow guidelines |

### Docs

| Path | Description |
|------|-------------|
| `docs/adr/` | Project ADRs, indexed in `docs/adr/README.md` |

## Setup

Use the junction skill to link skill directories into `~/.claude/skills/`:

```
/junction
```

This creates Windows directory junctions (not file symlinks) so that scripts and other assets within skill folders are included.