## Goal
Version control and develop lightweight harness that helps follow better methodologies when developing with ai (similar to BMAD but customized for lighter token usage and smaller projects).

## Skill setup
Use the `/junction` skill to link skill directories from this repo into `~/.claude/skills/`. Do not create single-file symlinks — always junction the whole skill directory so that scripts and other assets are included.

## Global config setup
`global/CLAUDE.md` is the version-controlled source for `~/.claude/CLAUDE.md` (user-level instructions). It's linked via a **hard link** (not symlink/junction — Windows requires elevation for file symlinks, and it's a single file with no assets). Edits in either location update the same file on disk.
