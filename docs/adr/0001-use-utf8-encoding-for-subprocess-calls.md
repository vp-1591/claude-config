# 0001 — Use UTF-8 encoding for subprocess calls

## Context

The `review-context` script uses `subprocess.run()` with `text=True` to capture output from `gh api` calls. On Windows, Python's default text encoding is `cp1252`, but GitHub API responses are always UTF-8. When a response contains characters outside the cp1252 range (e.g., byte `0x8d`), the background reader thread throws `UnicodeDecodeError`, which causes `stdout` to be `None`. Downstream `json.loads()` then fails with `TypeError: the JSON object must be str, bytes or bytearray, not NoneType`.

This is a Windows-specific bug — Linux/macOS default to UTF-8 and never hit it.

## Decision

Pass `encoding="utf-8"` to all `subprocess.run()` calls in the `run()` helper of `review-context`. This forces Python to decode subprocess output as UTF-8, matching the actual encoding of GitHub API responses.

## Constraints

- This only affects the `subprocess.run` call in the `run()` helper; it does not change file I/O encoding.
- The fix must not break behavior on Linux/macOS, where UTF-8 is already the default.

## Consequences

- **Positive:** The `review-context` script now works correctly on Windows when PR data contains non-ASCII characters (emoji in usernames, international characters in review bodies, etc.).
- **Neutral:** All subprocess output from the `run()` helper is now explicitly decoded as UTF-8. This is correct for `gh` commands, which always output UTF-8.
- **Negative:** None expected. If a future command produces output in a different encoding, `encoding` could be overridden per-call, but the `run()` helper currently serves only `gh` and `git`, both of which output UTF-8.

## Validation

- Run `review-context <PR_NUMBER>` on Windows against a PR whose data contains non-ASCII characters. The command should succeed and print valid JSON instead of crashing with `UnicodeDecodeError` or `TypeError`.