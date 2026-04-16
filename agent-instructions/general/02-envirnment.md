# Environment

<for Windows>
Platform:
- Windows 11 with pwsh7, cmd, or Git Bash.

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

---

## Optional: Claude Code Shell Quirks

When using PowerShell:

- Windows PowerShell (5.x) does not support `&&`; use `;` or `if ($?) { ... }`. pwsh 7+ supports `&&` and `||` natively.
- Quote paths that contain spaces or non-ASCII characters.

When using Git Bash on Windows:

- **NUL file bug**: Claude Code may create actual files named `nul` when commands redirect output to `NUL` (e.g., `> NUL`, `2> NUL`). `NUL` is a reserved device name on Windows; if a `nul` file is created, delete it via UNC path: `del "\\.\<full-path>\nul"`

## Optional: Codex APP + WSL2 Backend

When running in Codex CLI or the Codex desktop app, this instruction file lives in the Windows-side `~/.codex/` and is read regardless of backend.

If launched via WSL2 backend, you are physically running inside WSL2. In that case, also check the WSL2-side `~/My_WSL2_Config.md` file — it may contain additional environment configuration (e.g. local dev environment notes) that is more relevant to your actual runtime context.
