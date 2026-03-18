# Scripts

这个目录存放一些日常 CLI 工具脚本与配套说明。

## PowerShell

- `ccc.ps1`：交互式 Claude Code 启动器。列出当前用户 Claude 配置目录中的 `settings*` 文件，选择后以 `--dangerously-skip-permissions` 模式启动 Claude Code。

```powershell
. scripts/ccc.ps1
ccc
```

## Python

- `clean_chat_history.py`：多 CLI 对话历史清理（Claude Code / Codex / OpenCode / Gemini CLI）
  说明见 `scripts/docs/clean_chat_history.md`
- `migrate_codex_provider_history.py`：修复 Codex `model_provider` 变更后 chat history / resume / fork 无法正确加载
  说明见 `scripts/docs/migrate_codex_provider_history.md`
