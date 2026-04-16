# Tools

这个目录存放一些给用户手动运行的日常 CLI 辅助工具与配套说明。

## PowerShell

- `ccc.ps1`：交互式 Claude Code 启动器。列出当前用户 Claude 配置目录中的 `settings*` 文件，选择后以 `--dangerously-skip-permissions` 模式启动 Claude Code。

```powershell
. tools/ccc.ps1
ccc
```

## Python

- `clean_chat_history.py`：多 CLI 对话历史清理（Claude Code / Codex / Gemini CLI）
  说明见 `tools/docs/clean_chat_history.md`
- `migrate_codex_provider_history.py`：修复 Codex `model_provider` 变更后 chat history / resume / fork 无法正确加载
  说明见 `tools/docs/migrate_codex_provider_history.md`


## OMP Patches

Local patches for the installed OMP binary. Each patch directory contains an `apply.ts` runner and a `patch.diff`.

- `omp-patch-codex-websearch-byok`：让 OMP 的 codex web_search provider 支持自定义 OpenAI Responses 后端（baseUrl+apiKey），不再强制走 ChatGPT OAuth。适用于 juya(new-api) -> CPA 等反代链路。

```bash
bun run tools/omp-patch-codex-websearch-byok/apply.ts          # apply
bun run tools/omp-patch-codex-websearch-byok/apply.ts --status # check status
bun run tools/omp-patch-codex-websearch-byok/apply.ts --reverse # revert
```