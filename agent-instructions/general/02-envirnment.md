# Environment

<for Windows>
Platform:
- Most of the time: Windows 11 with pwsh7, cmd, or Git Bash.
- Some sessions may be launched by a Windows app while the actual thread runs in WSL2.

Python:
- Use `uv` for general projects; use conda for ML / scientific projects.
- Strict environment isolation is mandatory. Never install packages globally.

Git/GitHub:
- Default account: `<default-account>` with noreply email `<github-number-id+username@users.noreply.github.com>`.
- Alternative accounts: `<alt-account-1>`, `<alt-account-2>`.
- Use `gh` and `git config --local` to ensure the correct identity for each project.
- If account separation matters, keep remotes / keys / local git config aligned with the intended account.
</for Windows>

<for WSL2>
Platform:
- WSL2 Ubuntu 24.04.x on Windows 11.
- The default interactive shell may be fish, but automation / agents often run `bash -lc`, so shell init behavior can differ.
- When the user gives a Windows path, convert it to the matching WSL path before accessing it.

Python:
- Use `uv` for general projects; use conda for ML / scientific projects.
- Prefer per-repo `.venv` isolation; avoid global package installation.

Go:
- Go may live under `~/.local/go`, with tools under `$HOME/go/bin`.
- Make sure PATH assumptions work in both fish and `bash -lc` contexts.

Rust:
- Rust is typically managed with `rustup` under `~/.cargo`.
- Fish and bash may load Rust environment from different init files.

Git/GitHub:
- Default account: `<default-account>` with noreply email `<github-number-id+username@users.noreply.github.com>`.
- Alternative accounts: `<alt-account-1>`, `<alt-account-2>`.
- Some repos switch identity via local config or `includeIf`; do not hardcode repo paths in decisions.
- Prefer SSH aliases in `~/.ssh/config` when account separation matters.
- `git push` / `git pull` follow the remote URL and SSH key / alias; `gh pr` / `gh repo` / `gh issue` follow the active `gh` account.
- Use `git-account status` or `git var GIT_AUTHOR_IDENT` + `git remote -v` to confirm git identity.
- Use `git-account gh status` or `gh auth status` when `gh` commands are involved.
</for WSL2>
