#!/usr/bin/env python3
"""Stop hook: lint the changed .py files with the project's own ruff.

Runs once per turn (on Stop, not per-edit) so it never fires against a
mid-edit intermediate state the way a PostToolUse hook would. The files to
lint are the Python files changed in the working tree relative to HEAD
(staged + unstaged diff, plus untracked .py files), found via git in the
project root ($CLAUDE_PROJECT_DIR, falling back to the hook's cwd). Outside
a git repository, or with no changed .py files, the hook skips silently.
No guard against pre-existing lint noise in untouched files.

Finds ruff the same way pyright-check.py finds pyright: walk up from the
project root looking for .venv/venv, bounded by $CLAUDE_PROJECT_DIR,
falling back to $VIRTUAL_ENV (see hook_common.find_venv). If the project
has no venv, or its venv has no ruff, the hook skips silently (exit 0) so
it never blocks stops in projects that don't use ruff. If ruff exceeds the
timeout (hook_common.TOOL_TIMEOUT_SECONDS) the hook skips too rather than
stalling the stop.

Exit codes follow Claude Code Stop hook semantics:
  0  no issues, nothing to lint, no ruff available, or timeout -- allow stop
  2  ruff reported/fixed issues -- stop is blocked, this report is surfaced
     to the model as the reason to keep working
"""

import os
import subprocess
import sys
from pathlib import Path

from hook_common import (
    ensure_utf8_stderr,
    find_tool,
    find_venv,
    read_hook_input,
    run_tool,
)


def changed_py_files(root: Path) -> list[Path]:
    """Existing .py files changed in the working tree under ``root``.

    Staged and unstaged changes vs HEAD, plus untracked files; sorted for
    deterministic output. Empty when this isn't a git repository.
    """
    tracked = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", "HEAD", "--", "*.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if tracked.returncode != 0:
        return []  # not a repo, or git unavailable -- nothing to lint
    untracked = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "--", "*.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    names = sorted(set(tracked.stdout.split()) | set(untracked.stdout.split()))
    return [root / name for name in names if (root / name).is_file()]


def main() -> int:
    ensure_utf8_stderr()
    data = read_hook_input()
    if data is None:
        return 0  # no/blank input; nothing to lint

    # Avoid re-blocking forever if a previous Stop hook already forced a
    # continuation this turn.
    if data.get("stop_hook_active"):
        return 0

    project_root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    root = Path(project_root)
    files = changed_py_files(root)
    if not files:
        return 0

    venv = find_venv(root)
    ruff = find_tool(venv, "ruff") if venv else None
    if ruff is None:
        return 0  # no project venv, or no ruff in it -- skip

    blocked = False
    for file_path in files:
        result = run_tool(
            [
                str(ruff),
                "check",
                "--fix",
                "--show-fixes",
                "--exit-non-zero-on-fix",
                str(file_path),
            ],
            cwd=file_path.parent,
        )
        if result is None:
            print(f"ruff timed out on {file_path}; skipping", file=sys.stderr)
            continue
        if result.returncode != 0:
            blocked = True
            print(f"{file_path}:\n", file=sys.stderr)
            if result.stdout:
                print(result.stdout, file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
    return 2 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
