## hooks/hooks.json

Hook registrations shipped by the `config` plugin (repo root is the plugin
root — see `.claude-plugin/plugin.json`). Scripts are invoked via
`${CLAUDE_PLUGIN_ROOT}/hooks/...` paths, so they resolve inside the repo
regardless of what exists under `~/.claude`.

`~/.claude/settings.json` must not hold a `hooks` section: hooks registered
there and in this file both run on every event (no deduplication), so any
leftover settings-level registration means the hook fires twice. To add,
move, or remove a registration, edit only `hooks/hooks.json`.