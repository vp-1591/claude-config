#!/usr/bin/env python3
"""Stop hook: type-check the project with its own venv's pyright.

Runs once per turn (on Stop, not per-edit) so it never fires against a
mid-refactor intermediate state the way a PostToolUse hook would. Finds
pyright the same way ruff-check.py finds ruff: walk up from the project
root looking for .venv/venv, bounded by $CLAUDE_PROJECT_DIR, falling back
to $VIRTUAL_ENV (see hook_common.find_venv). If the project has no venv,
or its venv has no pyright, the hook skips silently (exit 0).

Only reportGeneralTypeIssues-and-friends at "error" severity are treated
as blocking; warnings/information are ignored so pre-existing, unsuppressed
noise doesn't gate every turn. Legacy debt is expected to be handled with
`# pyright: ignore[...]` / pyrightconfig excludes, not by this hook.

If pyright exceeds the timeout (hook_common.TOOL_TIMEOUT_SECONDS) the hook
skips rather than stalling the stop.

Exit codes follow Claude Code Stop hook semantics:
  0  no errors, nothing to check, no pyright available, or timeout -- allow stop
  2  pyright reported errors -- stop is blocked, this report is surfaced
     to the model as the reason to keep working
"""

import json
import os
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
        return 0  # no/blank input; nothing to check

    # Avoid re-blocking forever if a previous Stop hook already forced a
    # continuation this turn.
    if data.get("stop_hook_active"):
        return 0

    project_root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    root = Path(project_root)

    venv = find_venv(root)
    pyright = find_tool(venv, "pyright") if venv else None
    if pyright is None:
        return 0  # no project venv, or no pyright in it -- skip

    result = run_tool([str(pyright), "--outputjson"], cwd=root)
    if result is None:
        print("pyright timed out; skipping type check", file=sys.stderr)
        return 0

    try:
        report = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        # pyright crashed/misconfigured rather than found type errors --
        # don't block the turn on a broken invocation.
        return 0

    errors = [
        d for d in report.get("generalDiagnostics", [])
        if d.get("severity") == "error"
    ]
    if not errors:
        return 0

    print(f"pyright found {len(errors)} error(s) in {root}:\n", file=sys.stderr)
    for d in errors:
        file = d.get("file", "?")
        line = d.get("range", {}).get("start", {}).get("line", 0) + 1
        col = d.get("range", {}).get("start", {}).get("character", 0) + 1
        rule = f" [{d['rule']}]" if d.get("rule") else ""
        print(f"{file}:{line}:{col}: {d.get('message', '')}{rule}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
