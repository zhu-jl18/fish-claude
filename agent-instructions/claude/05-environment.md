# Environment

## OS & Shells

Windows 11: git bash, pwsh7 and cmd

When using PowerShell:

- Windows PowerShell (5.x) does not support `&&`; use `;` or `if ($?) { ... }`.
  pwsh 7+ supports `&&` and `||` natively.
- Quote paths that contain spaces or non-ASCII characters.

When using Git Bash on Windows:

- **NUL file bug**: Claude Code may create actual files named `nul` when commands
  redirect output to `NUL` (e.g., `> NUL`, `2> NUL`). `NUL` is a reserved device
  name on Windows; if a `nul` file is created, delete it via UNC path:
  `del "\\.\<full-path>\nul"`

## Python

- Use uv for general projects; conda for ML/scientific projects.
- Strict environment isolation is mandatory. Never install packages globally.

## Git / GitHub

GitHub CLI (`gh`) is installed.

- Default account: `<your-username>`.
- Alternative accounts: `<alt-1>`, `<alt-2>`.
- Use `gh cli` and `git config --local` to ensure correct identity for each project.
