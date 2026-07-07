---
name: review
allowed-tools: Bash(gh pr view:*), Bash(gh api:*), Bash(gh pr diff:*), Bash(gh pr review:*), Bash(find:*)
description: Code review a pull request
disable-model-invocation: false
---

Provide a code review for the given pull request.

To do this, follow these steps precisely:

1. **Eligibility + context gather (bash only, no agent).** Run `gh pr view <number> --json state,isDraft,headRefOid,author,files` and `gh api repos/{owner}/{repo}/pulls/{number}/reviews`. Stop (do not proceed) if the PR is closed, is a draft, or already has a review from you whose `commit_id` matches the current `headRefOid`. Otherwise keep the file list and author from this call — do not re-fetch them in later steps.

2. **Obvious-noise pre-filter (bash only, no agent).** Stop without invoking any agent if either is true:
   - Every changed file matches a lockfile/generated-file pattern (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`, `*.snap`, `go.sum`, and similar).
   - The PR author is a known bot account (e.g. `dependabot[bot]`, `renovate[bot]`).

3. **Discover CLAUDE.md paths (bash only, no agent).** Using the file list from step 1, walk up each changed file's directory tree with `find` and collect any `CLAUDE.md` that exists, plus the repo root `CLAUDE.md` if present. De-duplicate.

4. **Single Haiku agent call — triviality + summary.** Give the agent the PR diff and ask it to return only this JSON:
   ```json
   {"proceed": <bool>, "summary": "<1-3 sentence summary of the change>"}
   ```
   `proceed` is `false` if the PR is trivial, automated, or obviously fine and needs no human-facing review. If `proceed` is `false`, stop.

5. **Parallel Sonnet subagents.** Launch the `review-bug-scanner` and `review-security` subagents in parallel. Give each the PR number, head SHA, and the CLAUDE.md paths from step 3. Each independently returns a list of issues (file/line, description, reason flagged).

6. If neither agent returned any issues, stop.

7. **Single batched scoring call.** Launch exactly one `review-issue-scorer` call with *all* issues from step 5 in a single request (never one call per issue, regardless of how many issues there are). It returns the evidence flags defined in its own spec — not a numeric score.

8. **Apply the decision table yourself (no agent, deterministic).** For each issue, keep it only if ALL of these are true from step 7's output:
   - `on_modified_lines`
   - `verified_by_reading_file`
   - `code_confirms_issue`
   - `has_direct_evidence_quote`
   - `pre_existing` is false
   - `caught_by_tooling` is false

   AND at least one of:
   - `practical_impact == "high"`
   - `claude_md_relevance == "explicit"`

   Discard everything else. If nothing survives, stop.

9. **Re-check eligibility (bash only, no agent).** Repeat the closed/draft/already-reviewed check from step 1 against the current `headRefOid`, in case state changed mid-run. If no longer eligible, stop without posting.

10. **Post the review.** Use `gh pr review <number> --comment -b "<body>"`, tied to the current head commit. Keep the body brief, no emojis, and cite/link relevant code, files, and URLs.

Notes:

- Use `gh` to interact with GitHub rather than web fetch.
- Make a todo list first.
- You must cite and link each issue (e.g. if referring to a CLAUDE.md, link it).
- For your final comment, follow this format precisely (example with 3 issues):

---

### Code review

Found 3 issues:

1. <brief description of bug> (CLAUDE.md says "<...>")

<link to file and line with full sha1 + line range for context, note that you MUST provide the full sha and not use bash here, eg. https://github.com/anthropics/claude-code/blob/1d54823877c4de72b2316a64032a54afc404e619/README.md#L13-L17>

2. <brief description of bug> (some/other/CLAUDE.md says "<...>")

<link to file and line with full sha1 + line range for context>

3. <brief description of bug> (bug due to <file and code snippet>)

<link to file and line with full sha1 + line range for context>

🤖 Generated with [Claude Code](https://claude.ai/code)

<sub>- If this code review was useful, please react with 👍. Otherwise, react with 👎.</sub>

---

- Or, if you found no issues:

---

### Code review

No issues found. Checked for bugs, security, and CLAUDE.md compliance.

🤖 Generated with [Claude Code](https://claude.ai/code)

---

- When linking to code, follow this format precisely, otherwise the Markdown preview won't render correctly: `https://github.com/anthropics/claude-cli-internal/blob/c21d3c10bc8e898b7ac1a2d745bdc9bc4e423afe/package.json#L10-L15`
  - Requires the full git sha — commands like `$(git rev-parse HEAD)` interpolated into the link will not work, since your comment is rendered directly as Markdown.
  - Repo name must match the repo you're reviewing.
  - `#` sign after the file name.
  - Line range format is `L[start]-L[end]`.
  - Provide at least 1 line of context before and after, centered on the flagged line (e.g. commenting on lines 5–6 → link to `L4-7`).