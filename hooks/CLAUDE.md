## hooks/settings.json

Version-controlled, hooks-only mirror of the `hooks` section in
`~/.claude/settings.json` (which is not in this repo). `~/.claude/hooks` is
symlinked here, so scripts in this directory are live — but hook
*registrations* are not.

When adding, moving, or removing a hook registration, update both
`hooks/settings.json` and `~/.claude/settings.json` in the same change
and keep them in sync before opening a PR. Nothing detects drift.