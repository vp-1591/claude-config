#!/usr/bin/env python3
"""PostToolUse hook: lint the file just edited with the project's own ruff.

Reads the Claude Code hook input JSON from stdin and runs ``ruff check
--fix`` on the edited ``.py`` file, using the ruff installed in the venv of
the project the file belongs to. The venv is found by walking up from the
edited file looking for ``.venv``/``venv`` (bounded by the project root);
``$VIRTUAL_ENV`` is used as a fallback. This makes the hook uv-independent
and pins linting to the exact ruff version the project has installed, so
results match a local ``.venv/Scripts/ruff`` / ``uv run ruff`` invocation.

If the project has no venv, or its venv has no ruff installed, the hook
skips silently (exit 0) so it never blocks edits in projects that don't use
ruff.

Exit codes follow Claude Code hook semantics:
  0  no issues, nothing to lint, or no ruff available -- pass through
  2  ruff reported/fixed issues -- tool result is blocked and this report is
     surfaced to the model as the error
"""

import json
import os
import subprocess
import sys
from pathlib import Path

VENV_DIRS = (".venv", "venv")


def _venv_python(venv: Path) -> Path:
    sub = "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    return venv / sub


def find_venv(start: Path) -> Path | None:
    """Closest project venv for a file at ``start``, or None.

    Walks up from ``start``; the first directory containing a ``.venv`` or
    ``venv`` with a python interpreter wins. Stops at ``$CLAUDE_PROJECT_DIR``
    when set (the project root Claude Code itself uses for this session);
    otherwise falls back to the first directory with ``.git`` or
    ``pyproject.toml``. Falls back to ``$VIRTUAL_ENV`` when no local venv is
    found.
    """
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    boundary = Path(project_root).resolve() if project_root else None

    current = start
    while True:
        for name in VENV_DIRS:
            candidate = current / name
            if candidate.is_dir() and _venv_python(candidate).is_file():
                return candidate
        if boundary is not None:
            if current.resolve() == boundary:
                break
        elif (current / ".git").is_dir() or (current / "pyproject.toml").is_file():
            break
        if current.parent == current:
            break
        current = current.parent
    active = os.environ.get("VIRTUAL_ENV")
    if active:
        candidate = Path(active)
        if candidate.is_dir() and _venv_python(candidate).is_file():
            return candidate
    return None


def find_ruff(venv: Path) -> Path | None:
    """Path to the venv's ruff executable, or None if not installed."""
    bindir = venv / ("Scripts" if sys.platform == "win32" else "bin")
    exe = bindir / ("ruff.exe" if sys.platform == "win32" else "ruff")
    return exe if exe.is_file() else None


def main() -> int:
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0  # no/blank input; nothing to lint

    file_path = (data.get("tool_input") or {}).get("file_path") or ""
    if not file_path or not file_path.endswith(".py") or not Path(file_path).is_file():
        return 0

    venv = find_venv(Path(file_path).parent)
    ruff = find_ruff(venv) if venv else None
    if ruff is None:
        return 0  # no project venv, or no ruff in it -- skip

    result = subprocess.run(
        [
            str(ruff),
            "check",
            "--fix",
            "--show-fixes",
            "--exit-non-zero-on-fix",
            file_path,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
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
