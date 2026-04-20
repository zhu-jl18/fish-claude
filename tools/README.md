# Tools

用户侧维护/迁移工具与本地 patch 索引。

| Tool | Type | Runtime | Source | Summary |
| --- | --- | --- | --- | --- |
| [claude-code-launcher](claude-code-launcher/) | launcher | PowerShell | local | 交互式 Claude Code 启动器，按 `settings*` 文件选择配置后启动 |
| [clean-chat-history](clean-chat-history/) | maintenance | Python | local | 清理 Claude Code / Codex / Gemini CLI 的本地对话历史 |
| [codex-provider-history-migrator](codex-provider-history-migrator/) | migration | Python | local | 迁移 Codex `model_provider` 历史归属，恢复 history / resume / fork 可见性 |
| [omp-patch-codex-websearch-byok](omp-patch-codex-websearch-byok/) | patch | Bun / TypeScript | local | 让 OMP codex `web_search` provider 支持自定义 Responses 兼容后端 |
| [omp-patch-custom-mcp](omp-patch-custom-mcp/) | patch | Bun / TypeScript | local | 为 OMP MCP 发现增加 Claude/Codex 用户级开关 |
| [omp-patch-status-line-default-metrics](omp-patch-status-line-default-metrics/) | patch | Bun / TypeScript | local | 调整 OMP 默认 status line 的指标保留优先级 |