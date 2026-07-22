# 0002 — Numbered roadmap prefixes

## Context

Roadmap files in `docs/roadmaps/` were named by slug only (e.g. `ci-pipeline.md`), with a slug-based index in `README.md`. Without a number prefix, there was no way to see the order in which roadmaps were created when scanning the directory or index. ADRs already use four-digit numbered prefixes, which makes creation order immediately visible.

## Decision

Adopt the same four-digit zero-padded number prefix convention for roadmaps: `docs/roadmaps/<NNNN>-<slug>.md` (e.g. `0001-ci-pipeline.md`). Update the README index to use `#` as the first column instead of `Slug`. Keep the existing `Notes` column — roadmaps don't need a `Superseded by` column because they rarely supersede each other the way ADRs do.

## Constraints

- Existing roadmaps (none yet) would need renaming if any existed.
- The `create-roadmap` and `edit-roadmap` skills must determine the next number by scanning the directory.
- The index format must remain compatible with manual editing.

## Consequences

- **Positive:** Roadmap references are unambiguous (`roadmap 0001` vs `roadmap ci-pipeline`). File listings sort chronologically. The convention mirrors ADRs, reducing cognitive overhead.
- **Negative:** Slightly more work to create a roadmap (scan directory for next number). Negligible in practice.

## Validation

- Run `/create-roadmap` and confirm the generated file uses a `<NNNN>-<slug>.md` name and the README index has a `#` column with the number.