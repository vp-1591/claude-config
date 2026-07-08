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

## Stuck? Search, don't guess

After **two failed attempts** at fixing the same problem, stop guessing and
switch to evidence-based debugging:

1. **Web search** the exact error message (or its most distinctive parts)
   using `WebSearch`.
2. If results are unclear, **fetch and read** the most relevant pages with
   `WebFetch`.
3. Only apply fixes **directly supported by search results** or official docs.

### What counts as "same problem"
- The error message is the same or shares distinctive tokens with a previous
  attempt's error.
- You're still editing the same file, function, or failing test.
- The error category repeats (e.g. third `TypeError`, third missing import,
  third test asserting the same thing).

### What does NOT count
- A **genuinely new error** that appeared after a fix landed — that gets its
  own two-attempt budget. "Fix A → new error B" is progress, not a loop.
- Exploring different solutions to a **design question** where there is no
  error to search for — use your judgment there.

The point is: if you catch yourself reaching for "maybe this will work" without
new information, you've used your budget. Go search.