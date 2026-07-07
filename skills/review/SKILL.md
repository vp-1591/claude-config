---
name: review
allowed-tools: Bash(review-context:*), Bash(review-find-claude:*), Bash(review-filter:*), Bash(review-link:*), Bash(review-post:*), Bash(gh pr diff:*)
description: Code review a pull request
disable-model-invocation: false
---

Provide a code review for the given pull request.

Setup note: this skill depends on five scripts (`review-context`,
`review-find-claude`, `review-filter`, `review-link`, `review-post`) being
on `PATH`. They handle everything that has exactly one correct way to do
it, so no tokens are spent explaining plumbing.

To do this, follow these steps precisely:

1. **Gather context.** Run `review-context <number>` and parse its JSON output. If `"eligible"` is `false`, stop — do not proceed. Keep `head_sha`, `author`, and `files` from this output for later steps; do not re-fetch them.

2. **Obvious-noise pre-filter.** Using the `files` list from step 1, stop without invoking any agent if either is true:
   - Every changed file matches a lockfile/generated-file pattern (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`, `*.snap`, `go.sum`, and similar).
   - `author` is a known bot account (e.g. `dependabot[bot]`, `renovate[bot]`).

3. **Single Haiku agent call — triviality + summary.** Give the agent the PR diff (`gh pr diff <number>`) and ask it to return only this JSON:
   ```json
   {"proceed": <bool>, "summary": "<1-3 sentence summary of the change>"}
   ```
   `proceed` is `false` if the PR is trivial, automated, or obviously fine and needs no human-facing review. This judgement isn't scripted — the definition of "trivial" shifts over time and needs a model, not a fixed rule. If `proceed` is `false`, stop.

4. **Discover CLAUDE.md paths.** Run `review-find-claude` with the `files` list from step 1 as arguments. Use its output (one path per line) in the next step.

5. **Parallel Sonnet subagents.** Launch the `review-bug-scanner` and `review-security` subagents in parallel. Give each the PR number, `head_sha`, and the CLAUDE.md paths from step 4. Each independently returns a list of issues (file/line, description, reason flagged). This is reasoning work and stays with the agents.

6. If neither agent returned any issues, stop.

7. **Single batched scoring call.** Launch exactly one `review-issue-scorer` call with *all* issues from step 5 in a single request (never one call per issue). It returns evidence flags per issue — this also stays with a model, since verifying "does this code actually prove the issue" requires reading and judgement. Save its JSON output to a file.

8. **Filter deterministically.** Run `review-filter` on the scorer's output file. It applies the fixed decision table in code — do not re-evaluate the flags yourself. If the result is an empty array, stop.

9. **Build links.** For each surviving issue, run `review-link --sha <head_sha> --file <path> --start <line> --end <line>` to get its permalink. Provide at least 1 line of context before and after the flagged line in `--start`/`--end` (e.g. flagging lines 5–6 → `--start 4 --end 7`).

10. **Write the review body.** Compose the comment using the format below. This is the one part of output construction that still needs judgement (clear, brief descriptions; correct citations) so it isn't scripted. Save it to a file.

11. **Re-check eligibility.** Run `review-context <number>` again in case state changed mid-run. If no longer eligible, stop without posting.

12. **Post the review.** Run `review-post <number> <body-file>`.

Notes:

- Use `gh` (via the scripts, or `gh pr diff` directly for the agents) rather than web fetch.
- Make a todo list first.
- You must cite and link each issue (e.g. if referring to a CLAUDE.md, link it).
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

---

- Or, if you found no issues:

---

### Code review

No issues found. Checked for bugs, security, and CLAUDE.md compliance.

🤖 Generated with [Claude Code](https://claude.ai/code)

---
