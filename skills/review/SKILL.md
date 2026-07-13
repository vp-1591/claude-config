---
name: review
allowed-tools: Bash
description: Code review a pull request
disable-model-invocation: false
---

Provide a code review for the given pull request.

All helper scripts live under `${CLAUDE_SKILL_DIR}/scripts/` and are
invoked with that prefix — no PATH setup required. They handle everything
that has exactly one correct way to do it, so no tokens are spent
explaining plumbing.

All intermediate files go in the project-level `.claude/_review-artifacts/`
directory (relative to the repo root, not `~/.claude/`) — never scatter them
across temp directories. The directory is created in step 2 and reused
throughout. File paths are fixed, not chosen ad hoc.

To do this, follow these steps precisely:

1. **Gather context and checkout PR branch.** Run `${CLAUDE_SKILL_DIR}/scripts/review-context <number>` and parse its JSON output. If `"eligible"` is `false`, stop — do not proceed. Keep `head_sha`, `author`, and `files` from this output for later steps; do not re-fetch them. The script also checks out the PR's head commit so local file reads match the diff. If `"branch_switch"` is present in the output, the working tree was switched — remember `"original_branch"` for the review comment. If `"branch_switch"` has `"switched": false`, local file reads may not match the PR diff (degraded mode); note this in the review comment.

2. **Prepare artifact directory.** Run `mkdir -p .claude/_review-artifacts` (project-level, not `~/.claude/`). All intermediate files from this pipeline go here.

3. **Obvious-noise pre-filter.** Using the `files` list from step 1, stop without invoking any agent if either is true:
   - Every changed file matches a lockfile/generated-file pattern (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`, `*.snap`, `go.sum`, and similar).
   - `author` is a known bot account (e.g. `dependabot[bot]`, `renovate[bot]`).

4. **Single Haiku agent call — triviality + summary.**  Launch the review-triage subagent with the PR number. It returns:
   ```json
   {"proceed": <bool>, "summary": "<1-3 sentence summary of the change>"}
   ```
   `proceed` is `false` if the PR is trivial, automated, or obviously fine and needs no human-facing review. This judgement isn't scripted — the definition of "trivial" shifts over time and needs a model, not a fixed rule. If `proceed` is `false`, stop.

5. **Discover CLAUDE.md paths.** Run `${CLAUDE_SKILL_DIR}/scripts/review-find-claude` with the `files` list from step 1 as arguments. Use its output (one path per line) in the next step.

6. **Parallel Sonnet subagents.** Launch the `review-bug-scanner`, `review-security`, and `review-consistency` subagents in parallel. Give `review-bug-scanner` and `review-security` the PR number, `head_sha`, and the CLAUDE.md paths from step 5, as before. Give `review-consistency` the PR number, `head_sha`, and the `files` list from step 1 — it reads `docs/adr/README.md` and `docs/roadmaps/README.md` itself to determine active ADRs/roadmaps and cross-reference them against `files`. Each subagent independently returns a list of issues (file/line, description, reason flagged). This is reasoning work and stays with the agents.

7. If none of the three agents returned any issues, stop.

8. **Single batched scoring call.** Launch exactly one `review-issue-scorer` call with *all* issues from step 6 in a single request (never one call per issue). It returns evidence flags per issue — this also stays with a model, since verifying "does this code actually prove the issue" requires reading and judgement. Save its JSON output to `.claude/_review-artifacts/scorer-output.json`.

9. **Filter deterministically.** Run `${CLAUDE_SKILL_DIR}/scripts/review-filter` on `.claude/_review-artifacts/scorer-output.json`. It applies the fixed decision table in code — do not re-evaluate the flags yourself. If the result is an empty array, stop.

10. **Build links.** For each surviving issue, run `${CLAUDE_SKILL_DIR}/scripts/review-link --sha <head_sha> --file <path> --start <line> --end <line>` to get its permalink. Provide at least 1 line of context before and after the flagged line in `--start`/`--end` (e.g. flagging lines 5–6 → `--start 4 --end 7`).

11. **Write the review body.** Compose the comment using the format below. This is the one part of output construction that still needs judgement (clear, brief descriptions; correct citations) so it isn't scripted. Save it to `.claude/_review-artifacts/review-body.md`.

12. **Handle diff-agnostic issues.** Some `review-consistency` issues are diff-agnostic (e.g. a missing ADR, or a conflict between two docs not tied to one line) and will have `line_start`/`line_end` as `null`. Skip `review-link` for these — there is no commit line to point to. In the review body, reference the doc path(s) directly instead (e.g. `docs/adr/0007-...md`) rather than fabricating a link.

13. **Re-check eligibility.** Run `${CLAUDE_SKILL_DIR}/scripts/review-context <number>` again in case state changed mid-run. If no longer eligible, stop without posting.

14. **Post the review.** Run `${CLAUDE_SKILL_DIR}/scripts/review-post <number> .claude/_review-artifacts/review-body.md`.

Notes:

- Use `gh` (via the scripts, or `gh pr diff` directly for the agents) rather than web fetch. All scripts are invoked via `${CLAUDE_SKILL_DIR}/scripts/<name>` — no PATH setup needed.
- Make a todo list first.
- You must cite and link each issue (e.g. if referring to a CLAUDE.md, link it).
- **Branch checkout:** `review-context` checks out the PR's head commit so subagents read the correct files. After the review, your working tree stays on that commit. The original branch is saved in `.claude/_review-artifacts/checkout-state-<number>.json` (keyed by PR number, so a leftover file from a different PR's review is never mistaken for this run's state). If `branch_switch` was returned, append a line to the review comment: `> Switched to PR branch for review. Run \`git checkout <original_branch>\` to return.`
- For your final comment, follow this format precisely (example with 3 issues):

---

### Code review

Found 3 issues:

1. <brief description of bug> (CLAUDE.md says "<...>")

<link from review-link>

2. <brief description of bug> (some/other/CLAUDE.md says "<...>")

<link from review-link>

3. <brief description of bug> (bug due to <file and code snippet>)

<link from review-link>

🤖 Generated with [Claude Code](https://claude.ai/code)

<sub>- If this code review was useful, please react with 👍. Otherwise, react with 👎.</sub>

> Switched to PR branch for review. Run `git checkout <original_branch>` to return.

---

- Or, if you found no issues:

---

### Code review

No issues found. Checked for bugs, security, and CLAUDE.md compliance.

🤖 Generated with [Claude Code](https://claude.ai/code)

> Switched to PR branch for review. Run `git checkout <original_branch>` to return.

---