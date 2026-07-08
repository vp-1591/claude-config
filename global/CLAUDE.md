## Image Analysis

When you need to analyze or describe an image file, use the `describe-image`
command via Bash rather than attempting to read it directly:

    describe-image "path/to/image.png"
    describe-image "path/to/image.png" "specific question about the image"

This calls a qwen3.5:397b:cloud and returns a text description you can reason about. Do not use the Read tool on images or files that may contain images(e.g. pdf) because that throws API Error: 400 this model does not support image input.

## Commits

Commit messages must include a bullet list with detailed changes in the commit body. Use multiple -m flags; Git does not parse \n as a line break.

## Git workflow

- Never commit directly to `main`. Create a feature branch first:
  `git checkout -b feat/<short-description>`
- Run relevant tests before opening a PR.
- Open a pull request:
  `gh pr create --fill`
- Wait for all CI checks to pass before merging.
- Do not squash-merge PRs. Use regular merge with branch deletion so that branch list stays clean (`gh pr merge --merge --delete-branch`) to preserve the full commit history.

## Search on repeat failures

After **2 failed attempts** at the same fix, stop guessing — `WebSearch` the error message, then `WebFetch` relevant results. Only apply fixes backed by what you find.

"Same fix" = still trying to achieve the same goal (get X deployed, make test Y pass). The error changing between attempts doesn't reset the budget — you're still stuck. Only a **successful fix followed by a genuinely new problem** resets it.