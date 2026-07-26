---
name: junction
description: Create a Windows junction (directory symlink, mklink /J) from a repo directory to the user's .claude directory so skills, configs, and shared files are auto-synced without manual linking per item. Use this when asked to link, symlink, junction, or connect a repo folder into .claude -- especially for batch-linking all skills at once instead of one-by-one.
---

Create a Windows junction (directory symlink, equivalent to `mklink /J`) from a
directory in this repo to the user's `~/.claude/` directory. Unlike individual
symlinks, a junction makes the entire directory tree available -- new files
added to the repo side appear in `~/.claude/` automatically.

## Usage

Call this skill with the directory name (relative to repo root) you want to
junction. For example, to junction the `shared/` directory:

    /junction shared

This creates: `~/.claude/shared` -> `<repo-root>/shared`

## Process

1. **Resolve the user's home directory.** Use `$env:USERPROFILE` in PowerShell
   -- never hardcode a username.

2. **Validate the source directory exists** in the repo root. If not, stop.

3. **Check the target path** (`$HOME/.claude/<name>`):
   - If it doesn't exist -> proceed to create the junction.
   - If it exists as a junction already -> report the existing target and stop
     (it's already set up).
   - If it exists as a real directory -> report the conflict and stop.

4. **Create the junction** using PowerShell.

   **Git Bash trap:** When calling `powershell.exe -Command` from Git Bash,
   `$env:USERPROFILE` is consumed by bash (empty variable) before PowerShell
   sees it. `$HOME` also fails -- bash expands it to `/c/Users/...` which
   PowerShell misreads as `C:\c\Users\...`.

   **Correct approach -- single quotes for the outer shell:**

   ```powershell
   powershell.exe -Command 'New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\<name>" -Value "<absolute-repo-path>\<name>"'
   ```

   Single quotes prevent bash from expanding `$env:USERPROFILE`, so PowerShell
   receives it intact.

   **Fallback -- explicit paths (when single quotes don't work):**

   ```powershell
   powershell.exe -Command "New-Item -ItemType Junction -Path 'C:\Users\vadim\.claude\<name>' -Value '<absolute-repo-path>\<name>'"
   ```

5. **Verify** the junction was created by listing its contents. If empty or
   missing, report the error.

## Notes

- Use `powershell.exe -Command` -- `cmd.exe /c mklink /J` output is unreliable
  in this environment.
- The source directory stays in version control. The junction is just a
  pointer -- no files are moved.
- To remove a junction, use `cmd.exe /c rmdir` (not `rm`/`rmdir` in bash).
- To check if a path is a junction: `fsutil reparsepoint query "<path>"`
