#!/usr/bin/env python3
"""Tests for the block-dotenv-reads hook.

Run with: python hooks/test_block_dotenv_reads.py
"""

import json
import subprocess
import sys
from pathlib import Path


HOOK = Path(__file__).parent / "block-dotenv-reads.py"


def run_hook(tool: str, tool_input: dict) -> int:
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input})
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode


def test_read_tool() -> None:
    assert run_hook("Read", {"file_path": "/app/.env"}) == 2
    assert run_hook("Read", {"file_path": "/app/.env.local"}) == 2
    assert run_hook("Read", {"file_path": "/app/.env.production"}) == 2
    assert run_hook("Read", {"file_path": "C:\\project\\.env"}) == 2
    assert run_hook("Read", {"file_path": "/app/.env.example"}) == 0
    assert run_hook("Read", {"file_path": "/app/.env.sample"}) == 0
    assert run_hook("Read", {"file_path": "/app/.env.template"}) == 0
    assert run_hook("Read", {"file_path": "/app/.env.dist"}) == 0
    assert run_hook("Read", {"file_path": "/app/.envrc"}) == 0
    assert run_hook("Read", {"file_path": "/app/src/main.py"}) == 0


def test_grep_tool() -> None:
    assert run_hook("Grep", {"path": "/app", "glob": ".env"}) == 2
    assert run_hook("Grep", {"path": "/app/.env.local", "glob": "*.py"}) == 2
    assert run_hook("Grep", {"path": "/app", "glob": ".env.example"}) == 0
    assert run_hook("Grep", {"path": "/app/.env.sample", "glob": "*.py"}) == 0


def test_bash_tool() -> None:
    assert run_hook("Bash", {"command": "cat .env"}) == 2
    assert run_hook("Bash", {"command": "type .env"}) == 2
    assert run_hook("Bash", {"command": "Get-Content .env"}) == 2
    assert run_hook("Bash", {"command": "Select-String SECRET .env"}) == 2
    assert run_hook("Bash", {"command": "sed -n '1,5p' .env"}) == 2
    assert run_hook("Bash", {"command": "awk '{print}' .env"}) == 2
    assert run_hook("Bash", {"command": "source .env"}) == 2
    assert run_hook("Bash", {"command": ". .env"}) == 2
    assert run_hook("Bash", {"command": "cat .env.example"}) == 0
    assert run_hook("Bash", {"command": "cat .env.sample"}) == 0
    assert run_hook("Bash", {"command": "git commit -m \"mention .env\""}) == 0
    assert run_hook("Bash", {"command": "python app.py"}) == 0


def main() -> int:
    failures = []
    for name, fn in [
        ("test_read_tool", test_read_tool),
        ("test_grep_tool", test_grep_tool),
        ("test_bash_tool", test_bash_tool),
    ]:
        try:
            fn()
        except AssertionError as exc:
            failures.append(f"{name}: {exc}")
            print(f"FAIL: {name}")
        else:
            print(f"PASS: {name}")

    if failures:
        print(f"\n{len(failures)} test(s) failed:")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print("\nAll tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
