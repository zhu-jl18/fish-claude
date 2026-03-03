## Tool Priority

- On Windows, Codex executes shell commands via PowerShell 7 (`pwsh`) by default—use PowerShell syntax and avoid `cmd.exe`-only flags (e.g., `cd /d X:\Toys\novel-format` fails in PowerShell).

- USE TOOL DIRECTLY. AVOID shell wrappers such as  `cmd /c`, `pwsh.exe -NoLogo -NoProfile -Command`, and `powershell.exe -NoLogo -NoProfile -Command` **unless necessary**. 

## Tool Orchestration (Default: Parallel)

Use `multi_tool_use.parallel` to parallel tool invocation (accelerates batch reading, searching, and execution) whenever possible.
