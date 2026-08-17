#!/usr/bin/env python3
"""PreToolUse hook that blocks direct reads from .env files.

Allows common template files that should contain placeholders rather than
real secrets. Blocks .env, .env.local, .env.production, and other runtime
.env* variants.

Reads JSON from stdin: {"tool_name": "...", "tool_input": {...}}.
Exits with code 0 (allow) or 2 (block).
"""

import json
import re
import sys

from hook_common import ensure_utf8_stderr, read_hook_input


_DOTENV_FILENAME_RE = re.compile(
    r"(?<![a-zA-Z0-9_])(\.env(?:\.[a-zA-Z0-9_]+)*)(?![a-zA-Z0-9_])",
    re.IGNORECASE,
)

_SAFE_DOTENV_NAMES = frozenset(
    {
        ".env.dist",
        ".env.example",
        ".env.sample",
        ".env.template",
    }
)


def _is_real_dotenv(text: str) -> bool:
    """Return True if *text* references a real .env file."""
    for match in _DOTENV_FILENAME_RE.finditer(text):
        filename = match.group(1).lower()
        if filename not in _SAFE_DOTENV_NAMES:
            return True
    return False


_READ_COMMANDS = frozenset(
    {
        "awk",
        "cat",
        "code",
        "explorer",
        "gc",
        "get-content",
        "grep",
        "head",
        "less",
        "more",
        "nano",
        "nl",
        "notepad",
        "nvim",
        "open",
        "rev",
        "rg",
        "sed",
        "select-string",
        "start",
        "tac",
        "tail",
        "type",
        "vi",
        "vim",
        "xdg-open",
    }
)

_READ_CMD_RE = re.compile(
    r"(?:^|[\|;&])\s*("
    + "|".join(re.escape(command) for command in _READ_COMMANDS)
    + r")\s+.*?\.env(?:\.[a-zA-Z0-9_]+)*(?:[^a-zA-Z0-9.]|$)",
    re.IGNORECASE,
)

_SOURCE_RE = re.compile(
    r"(?:^|[\|;&])\s*(?:source|\.)\s+.*?\.env(?:\.[a-zA-Z0-9_]+)*(?:[^a-zA-Z0-9.]|$)",
    re.IGNORECASE,
)


def _is_read_dotenv_command(command: str) -> bool:
    """Return True if *command* reads or sources a real .env file."""
    for match in _READ_CMD_RE.finditer(command):
        if _is_real_dotenv(match.group(0)):
            return True
    for match in _SOURCE_RE.finditer(command):
        if _is_real_dotenv(match.group(0)):
            return True
    return False


_BLOCKED_MSG = "Blocked: reading .env files is not allowed (security: secrets)."


def _block() -> None:
    print(_BLOCKED_MSG, file=sys.stderr)
    sys.exit(2)


def _check_read_tool(tool_input: dict) -> None:
    if _is_real_dotenv(tool_input.get("file_path", "")):
        _block()


def _check_grep_tool(tool_input: dict) -> None:
    path = tool_input.get("path", "")
    glob_pattern = tool_input.get("glob", "")
    if _is_real_dotenv(path) or _is_real_dotenv(glob_pattern):
        _block()


def _check_bash_tool(tool_input: dict) -> None:
    if _is_read_dotenv_command(tool_input.get("command", "")):
        _block()


_TOOL_CHECKERS = {
    "Read": _check_read_tool,
    "Grep": _check_grep_tool,
    "Bash": _check_bash_tool,
}


def main() -> int:
    ensure_utf8_stderr()
    data = read_hook_input()
    if data is None:
        return 0

    checker = _TOOL_CHECKERS.get(data.get("tool_name", ""))
    if checker:
        checker(data.get("tool_input") or {})
    return 0


if __name__ == "__main__":
    sys.exit(main())
