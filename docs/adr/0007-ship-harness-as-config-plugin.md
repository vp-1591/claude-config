# Ship skills, commands, agents, and hooks as the `config` plugin

## Context

This repo fed Claude Code through junctions/symlinks into `~/.claude` (skills,
agents, commands, hooks, shared) plus a manually-maintained mirror of hook
registrations (`hooks/settings.json` ↔ `~/.claude/settings.json`), with nothing
detecting drift between them. The drift materialized: the `SessionStart` ollama
hook existed only in `~/.claude/settings.json` and never made it into the repo
mirror.

Claude Code's plugin system can load all four component types from a single
directory whose layout this repo already matched (`skills/`, `agents/`,
`commands/`, `hooks/` at the root), including hooks registered in plugin-shipped
`hooks/hooks.json` in the same shape as settings-level hooks. Plugins loaded
from a local marketplace with a relative source path load in place from the
working tree, preserving the live-edit property the junctions provided.

## Decision

The goal is a single version-controlled source of truth for every component the
harness ships, with no manual sync step that can drift. The mechanism chosen to
serve that goal is the repo root as a Claude Code plugin (`.claude-plugin/`
manifest, name `config` — Anthropic reserves the `claude-` prefix for its own
plugins), served by the local `claude-config` marketplace defined in
`.claude-plugin/marketplace.json` with a relative source path so it loads in
place.

- Skills, commands, agents, and all hook registrations ship in the plugin;
  the `hooks/settings.json` mirror is deleted.
- `global/CLAUDE.md` (symlinked to `~/.claude/CLAUDE.md`) and `shared/`
  (opt-in per-project imports) stay outside the plugin: plugins cannot ship
  persistent instructions (a root `CLAUDE.md` is never loaded as context) or
  opt-in imports, and plugin enable/disable is coarser than per-file `@import`.
- The `junction` skill stays project-level; it now serves only what the plugin
  cannot ship (`shared/` junctions, the `CLAUDE.md` symlink).

Alternatives rejected:

- **Status quo (junctions + mirror)** — rejected because the mirror drift had
  already happened; the only component where the current model was worse than
  the plugin model was hook registration, and that alone drove the migration.
- **Full plugin conversion** (also moving CLAUDE.md/shared in) — rejected
  because the plugin format has no mechanism for either, so the
  junction/symlink machinery would be kept anyway while adding plugin
  complexity on top.

## Constraints

- `~/.claude/settings.json` must never hold a `hooks` section: settings-level
  and plugin hooks are not deduplicated — both run on every event.
- All hook registrations live only in `hooks/hooks.json`, with scripts
  referenced via `${CLAUDE_PLUGIN_ROOT}` (exec form) so they resolve inside
  the repo regardless of what exists under `~/.claude`.
- The plugin name must not start with `claude-`/`anthropic-` (reserved by
  Anthropic; `claude plugin validate` rejects it).
- `shared/` files must not be leaked into user-level CLAUDE.md (per AGENTS.md);
  the plugin must not become a side channel for that.
- opencode keeps consuming only `shared/adr-workflow.md` via `opencode.json`;
  it cannot load `.claude-plugin` plugins.

## Consequences

- Positive: hook registrations are code-reviewed in one place and can no
  longer drift from the deployed machine; one command installs/updates all
  components on a new machine; the junction farm for skills/agents/commands/
  hooks is gone.
- Negative: bare command names (`/planner`, `/edit-roadmap`) are now aliases
  for `config:*` names — they keep working only while unambiguous, so
  references in `shared/adr-workflow.md` rely on nothing else claiming those
  names.
- Negative: components of a plugin enabled at user scope load in every
  project; per-project opt-out is coarser than not junctioning a directory.
- Negative: `claude plugin install`/`update` snapshots the entire working
  tree — **including gitignored files** — into
  `~/.claude/plugins/cache/claude-config/config/<sha>/`. The snapshot has
  been observed to contain the gitignored `.env`, `tmp/`,
  `.claude/settings.local.json`, and `__pycache__`. The repo guards `.env`
  reads with a PreToolUse hook, yet the install mechanism copies the file
  outside the repo. Accepted risk: the cache is user-profile-local and
  orphaned snapshots are cleaned up after 14 days; the `.env` file stays in
  the repo, and the existing snapshot can be deleted once orphaned.
- `claude plugin validate` cannot verify `${CLAUDE_PLUGIN_ROOT}` script
  resolution — hook changes must be verified by firing the hooks (debug log),
  not by validation alone.
- Repo root is now dual-purpose (project + plugin root); the root `CLAUDE.md`
  triggers a harmless validator warning because plugins never load it as
  context.

## Validation

- `claude plugin validate .` exits 0 (manifest, frontmatter, hooks shape).
- A headless session (`claude -p --debug-file <log> "say ok"`) shows: hooks
  loaded from the repo's `hooks/hooks.json`, skills/commands/agents loaded
  from the plugin directories, and each of SessionStart/Stop hooks finishing
  with status 0 exactly once per event, attributed to `config@claude-config`
  with repo-root script paths — no second execution from `~/.claude/hooks`
  paths.
- `pytest hooks/test_block_dotenv_reads.py` passes (3 tests).
- Manual: a headless session asked to Read a `.env` file is blocked by
  `block-dotenv-reads.py` via the plugin's PreToolUse registration.