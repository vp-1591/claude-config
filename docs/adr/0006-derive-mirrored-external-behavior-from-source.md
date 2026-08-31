# 0006 — Derive mirrored external behavior from source, not memory

## Context

A consumer project's TTS server gate set `HF_HUB_OFFLINE=1` based on a hand-maintained
list ("kokoro needs exactly `config.json` and `kokoro-v1_0.pth`") written from memory.
kokoro actually fetches in two phases — weights at construction, a voice file lazily at
first synthesis (`pipeline.py:142`) — so offline mode locked out a file that could never
download, and every synthesis failed permanently. Test fixtures were built from the same
partial list, so the test suite could only confirm the assumption. The existing
`## Mocking` rule ("inspect the real API before mocking") did not fire anywhere:
the gate was production code, not a mock, and even a faithful fixture would have passed
the gate's unit tests.

The RCA's structural finding: any code that answers "is the external state sufficient?"
is a *mirror* of someone else's runtime behavior. A mirror written from memory — with no
shared definition, no citation, and no test able to contradict it — cannot self-correct.
The user-level CLAUDE.md carries rules across all sessions, so this is where the
prevention belongs.

## Decision

Add a standalone `## Mirroring external behavior` section to `global/CLAUDE.md`,
alongside (not inside) `## Mocking`:

1. **Scope by epistemics, not by artifact** — everything that encodes what an external
   dependency does (test fixtures, cache-completeness checks, preflight gates, mocks)
   must be derived from the dependency's source or a live probe, never from memory —
   the author's or the code's own list.
2. **Behavior, not surface** — "inspecting the real API" includes *what it reads and
   when* (lazy fetches at first use), not just method signatures.
3. **A disagreeing test must exist** — at least one end-to-end test exercises the real
   dependency in the gated mode, so a wrong list fails instead of tautologically passing.
4. **Traceability** — hand-maintained requirement lists cite the source (`file:line`)
   they were derived from.

`## Mocking > External APIs` gained a pointer to the new section; its two subsections
are unchanged.

The goal is that no project inheriting these instructions can re-encode external
behavior from memory without at least one live observation of that behavior and one
test able to contradict the copy.

**Alternatives rejected:**

- *Subsection under `## Mocking`* — rejected because the section's trigger words
  ("mocking") don't fire for runtime gates; writing a preflight check doesn't feel like
  mocking, so practitioners never consult it. A standalone section with its own trigger
  vocabulary ("cache", "preflight", "fixture") matches the failure rather than the
  mechanism.
- *The originally proposed "verify before gating" rule* ("enumerate every artifact the
  dependency reads at runtime, including lazily fetched ones") — rejected as unbounded:
  enumerating *every* runtime-read artifact is impossible to complete and invites
  pretending completion. Scoping to the artifact actually gated on, plus one
  end-to-end test, prevents the incident class at a fraction of the cost.
- *Relying on the missing e2e test alone* — rejected: catching the instance without
  fixing the cause leaves the list free to drift on the next refactor.

## Constraints

- The rule lives in user-level CLAUDE.md (`global/CLAUDE.md`), so it ships in every
  session of every project — it must stay short; no expanding it into a checklist-length
  procedure.
- The existing `## Mocking` section's rules stay intact and unchanged — this section
  generalizes the principle to non-mock artifacts; it does not replace or relax them.
- No runtime enforcement (hooks/CI) is introduced in this decision — adherence is
  instruction-driven. Out of scope: prompt-eval coverage for this rule (blocked on the
  pending evals infrastructure).

## Consequences

- **Cheaper prevention**: the kokoro-class failure (gate trusts a memory-derived
  completeness list; fixtures inherit it; nothing contradicts either) has four named,
  mechanically checkable obligations attached anywhere it could recur.
- **Token cost in every session**: the section loads globally for a failure mode that
  is rare per-project. Accepted: the RCA showed the cost of the miss (silent permanent
  breakage in a consumer project) outweighs ~120 tokens/session.
- **Risk of over-application**: models may demand live probes for trivial cases
  (e.g., verifying `pathlib` reads a file). Mitigated by scoping the trigger to
  *encoding what a dependency does* (mirrors), not ordinary code that merely uses it.
- **No automated enforcement**: effectiveness depends on instruction adherence; the
  pending prompt-evals work should add this rule as a test case.

## Validation

- `git diff` on `global/CLAUDE.md` shows the new `## Mirroring external behavior`
  section and the pointer sentence in `## Mocking > External APIs`, with no other
  changes to that file.
- A fresh session (or re-read of the linked `~/.claude/CLAUDE.md`) shows the section
  present and correctly symlinked.
- First consumer-project run after adoption: any cache gate, preflight check, or
  external-behavior fixture written from memory should either cite a `file:line` or be
  flagged — manual review of the next PR touching such code.