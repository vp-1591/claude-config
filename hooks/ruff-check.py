#!/usr/bin/env python3
"""PostToolUse hook: lint the file just edited with the project's own ruff.

Reads the Claude Code hook input JSON from stdin and runs ``ruff check
--fix`` on the edited ``.py`` file, using the ruff installed in the venv of
the project the file belongs to. The venv is found by walking up from the
edited file (see hook_common.find_venv); ``$VIRTUAL_ENV`` is used as a
fallback. This makes the hook uv-independent and pins linting to the exact
ruff version the project has installed, so results match a local
``.venv/Scripts/ruff`` / ``uv run ruff`` invocation.

If the project has no venv, or its venv has no ruff installed, the hook
skips silently (exit 0) so it never blocks edits in projects that don't use
ruff. If ruff exceeds the timeout (hook_common.TOOL_TIMEOUT_SECONDS) the
hook skips too rather than stalling the edit.

Exit codes follow Claude Code hook semantics:
  0  no issues, nothing to lint, no ruff available, or timeout -- pass through
  2  ruff reported/fixed issues -- tool result is blocked and this report is
     surfaced to the model as the error
"""

import sys
from pathlib import Path

from hook_common import (
    ensure_utf8_stderr,
    find_tool,
    find_venv,
    read_hook_input,
    run_tool,
)


def main() -> int:
    ensure_utf8_stderr()
    data = read_hook_input()
    if data is None:
        return 0  # no/blank input; nothing to lint

    file_path = (data.get("tool_input") or {}).get("file_path") or ""
    if not file_path or not file_path.endswith(".py") or not Path(file_path).is_file():
        return 0

    venv = find_venv(Path(file_path).parent)
    ruff = find_tool(venv, "ruff") if venv else None
    if ruff is None:
        return 0  # no project venv, or no ruff in it -- skip

    result = run_tool(
        [
            str(ruff),
            "check",
            "--fix",
            "--show-fixes",
            "--exit-non-zero-on-fix",
            file_path,
        ],
        cwd=Path(file_path).parent,
    )
    if result is None:
        print(f"ruff timed out on {file_path}; skipping", file=sys.stderr)
        return 0
    if result.returncode != 0:
        print(f"{file_path}:\n", file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
