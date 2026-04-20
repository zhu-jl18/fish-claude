# claude-code-launcher

交互式 Claude Code 启动器。

## What

列出当前用户 Claude 配置目录中的 `settings*` 文件，选择后以 `--dangerously-skip-permissions` 模式启动 Claude Code。

## Usage

```powershell
. tools/claude-code-launcher/ccc.ps1
ccc
```

## Notes

- 依赖 Windows PowerShell 环境中的 `USERPROFILE` 与 `claude` 命令。
- 脚本会从 `~/.claude` 中枚举 `settings*` 文件。
