## Image Analysis

When you need to analyze or describe an image file, use the `describe-image`
command via Bash rather than attempting to read it directly:

    describe-image "path/to/image.png"
    describe-image "path/to/image.png" "specific question about the image"

This calls a qwen3.5:397b:cloud and returns a text description you can reason about. Do not use the Read tool on images or files that may contain images(e.g. pdf) because you can NOT process images. For pdf files you must write script in tmp/ folder that extracts text and images to read it's contents.

## Commits

Commit messages must include a bullet list with detailed changes in the commit body. Use multiple -m flags; Git does not parse \n as a line break.

## Git workflow

- Never commit directly to `main`. Create a feature branch first:
  `git checkout -b feat/<short-description>`
- Run relevant tests before opening a PR.
- After committing open a pull request:
  `gh pr create --fill`
- Do not merge without explicit request from user. When you are requested to merge, wait for all CI checks to pass before merging.
- Do not squash-merge PRs. Use regular merge with branch deletion so that branch list stays clean (`gh pr merge --merge --delete-branch`) to preserve the full commit history.

## Secrets
Do not print or read files or configs containing secrets without explicit permission.

## Search on repeat failures

After **2 failed attempts** at the same fix, stop guessing — `WebSearch` the error message, then `WebFetch` relevant results. Only apply fixes backed by what you find.

"Same fix" = still trying to achieve the same goal (get X deployed, make test Y pass). The error changing between attempts doesn't reset the budget — you're still stuck. Only a **successful fix followed by a genuinely new problem** resets it.

## Subagents
Always use TaskOutput awaiting tool to wait for subagents when you need their results

## Mocking external APIs
Before mocking any external object/library, inspect the real API (source, `inspect.signature`, or a live call) and match method names/signatures exactly — never infer them from memory or convention. If the real surface can't be resolved statically (no stub, C extension, `Any`), verify at runtime instead of trusting the type checker's silence.
