## Tool Priority

- On Windows, Codex executes shell commands via PowerShell 7 (`pwsh`) by default—use PowerShell syntax and avoid `cmd.exe`-only flags (e.g., `cd /d X:\Toys\novel-format` fails in PowerShell).

- On Linux/macOS, Codex executes shell commands via `bash` by default—use Bash syntax and avoid `sh`-only flags (e.g., `cd /path/to/dir` is fine in Bash but fails in `sh`). 

- USE TOOL DIRECTLY. AVOID shell wrappers such as  `cmd /c`, `pwsh.exe -NoLogo -NoProfile -Command`, and `powershell.exe -NoLogo -NoProfile -Command` **unless necessary**. 

- USE TOOL DIRECTLY. AVOID shell wrappers such as `bash -lc` **unless necessary**.   

## Tool Orchestration (Default: Parallel)

Use `multi_tool_use.parallel` to parallel tool invocation (accelerates batch reading, searching, and execution) whenever possible.
