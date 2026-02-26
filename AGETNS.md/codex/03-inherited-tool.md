## Tool Priority

- You can also use command in PowerShell on Windows so do not make low-level mistakes, for example: "cd /d X:\Toys\novel-format" fails because the `/d` syntax is for cmd, not PowerShell.
- For semantic codebase understanding, prefer `codebase-retrieval` first; use `rg` for exact string/file matching.
- USE TOOL DIRECTLY. AVOID shell wrappers such as  `cmd /c`, `pwsh.exe -NoLogo -NoProfile -Command`, and `powershell.exe -NoLogo -NoProfile -Command` **unless necessary**. 

## Tool Orchestration (Default: Parallel)

Use `multi_tool_use.parallel` to parallel tool invocation (accelerates batch reading, searching, and execution) whenever possible.