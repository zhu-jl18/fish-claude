# Tools

本地维护/迁移工具与 patch。

| Tool | Type | Runtime | 说明 |
| --- | --- | --- | --- |
| [claude-code-launcher](claude-code-launcher/) | launcher | PowerShell | 交互式启动器，按 `settings*` 文件选配置 |
| [clean-chat-history](clean-chat-history/) | maintenance | Python | 清理 Claude Code / Codex / Gemini CLI 对话历史 |
| [codex-provider-history-migrator](codex-provider-history-migrator/) | migration | Python | 迁移 Codex `model_provider`，恢复 history / resume / fork |
| [omp-patch-codex-websearch-byok](omp-patch-codex-websearch-byok/) | patch | Bun/TS | OMP codex web_search 支持自定义后端 |
| [omp-patch-custom-mcp](omp-patch-custom-mcp/) | patch | Bun/TS | OMP MCP 发现增加 Claude/Codex 用户级开关 |
| [omp-patch-status-line-default-metrics](omp-patch-status-line-default-metrics/) | patch | Bun/TS | 调整 OMP status line 窄宽度保留优先级 |
