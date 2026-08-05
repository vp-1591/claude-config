#!/usr/bin/env python3
"""Shared helpers for Claude Code hook scripts (ruff-check.py, pyright-check.py).

Python puts the hook script's own directory on sys.path, so ``import
hook_common`` resolves whether the hook runs from the repo or from a
junctioned copy under ~/.claude/hooks. Everything common to the two hooks
lives here:

  - locating a project venv (walk up, bounded by CLAUDE_PROJECT_DIR)
  - locating a tool executable inside that venv
  - reading Claude Code hook input JSON from stdin
  - running the tool with UTF-8 capture and a hang timeout
"""

import json
import os
import subprocess
import sys
from pathlib import Path

VENV_DIRS = (".venv", "venv")

# Ceiling on a hook's tool invocation. A hook that hangs (huge project, slow
# tool startup) must not stall the edit (PostToolUse) or the whole stop
# (Stop), so both hooks skip with exit 0 if the tool exceeds this.
TOOL_TIMEOUT_SECONDS = 120


def ensure_utf8_stderr() -> None:
    """Make stderr UTF-8 so tool reports with non-ASCII stay readable."""
    sys.stderr.reconfigure(encoding="utf-8")


def venv_bin(venv: Path) -> Path:
    """Platform venv bin dir: ``Scripts`` on Windows, ``bin`` elsewhere."""
    return venv / ("Scripts" if sys.platform == "win32" else "bin")


def find_venv(start: Path) -> Path | None:
    """Closest project venv for a file/dir at ``start``, or None.

    Walks up from ``start``; the first directory containing a ``.venv`` or
    ``venv`` with a python interpreter wins. Stops at ``$CLAUDE_PROJECT_DIR``
    when set (the project root Claude Code uses for this session); otherwise
    falls back to the first directory with ``.git`` or ``pyproject.toml``.
    Falls back to ``$VIRTUAL_ENV`` when no local venv is found.
    """
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    boundary = Path(project_root).resolve() if project_root else None

    current = start
    while True:
        for name in VENV_DIRS:
            candidate = current / name
            python = venv_bin(candidate) / ("python.exe" if sys.platform == "win32" else "python")
            if candidate.is_dir() and python.is_file():
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
        python = venv_bin(candidate) / ("python.exe" if sys.platform == "win32" else "python")
        if candidate.is_dir() and python.is_file():
            return candidate
    return None


def find_tool(venv: Path, name: str) -> Path | None:
    """Path to the venv's ``name`` executable, or None if not installed."""
    exe = venv_bin(venv) / (f"{name}.exe" if sys.platform == "win32" else name)
    return exe if exe.is_file() else None


def read_hook_input() -> dict | None:
    """Parse the Claude Code hook input JSON from stdin; None if absent."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return None


def run_tool(
    args: list[str],
    *,
    cwd: Path | str | None = None,
    timeout: float = TOOL_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess | None:
    """Run a tool capturing UTF-8 output; None if it exceeded ``timeout``.

    Hooks call this for the tools they wrap; a returned None means "timed
    out, skip" so the hook can exit 0 instead of stalling the session.
    """
    try:
        return subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
