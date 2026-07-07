---
name: junction
description: Create a Windows junction from a repo directory to the user's .claude directory
---

Create a Windows junction (directory symlink) from a directory in this repo to
the user's `~/.claude/` directory.

## Usage

Call this skill with the directory name (relative to repo root) you want to
junction. For example, to junction the `shared/` directory:

    /junction shared

This creates: `~/.claude/shared` → `<repo-root>/shared`

## Process

1. **Resolve the user's home directory.** Use `$env:USERPROFILE` in PowerShell
   or `$HOME` in bash — never hardcode a username.

2. **Validate the source directory exists** in the repo root. If not, stop.

3. **Check the target path** (`$HOME/.claude/<name>`):
   - If it doesn't exist → proceed to create the junction.
   - If it exists as a junction already → report the existing target and stop
     (it's already set up).
   - If it exists as a real directory → report the conflict and stop.

4. **Create the junction** using PowerShell (reliable on Windows):

   ```powershell
   $target = "$env:USERPROFILE\.claude\<name>"
   $source = "<absolute-repo-path>\<name>"
   New-Item -ItemType Junction -Path $target -Value $source
   ```

5. **Verify** the junction was created by listing its contents. If empty or
   missing, report the error.

## Notes

- Use `powershell.exe -Command` — `cmd.exe /c mklink /J` output is unreliable
  in this environment.
- The source directory stays in version control. The junction is just a
  pointer — no files are moved.
- To remove a junction, use `cmd.exe /c rmdir` (not `rm`/`rmdir` in bash).
