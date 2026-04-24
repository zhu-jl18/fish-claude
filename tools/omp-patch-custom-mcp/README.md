# omp-patch-custom-mcp

为 OMP MCP 发现增加细粒度用户级开关，避免只能全开或全关。

- `mcp.enableClaudeUser`：控制是否加载 Claude Code 用户级 MCP
- `mcp.enableCodexUser`：控制是否加载 Codex 用户级 MCP

```bash
bun run tools/omp-patch-custom-mcp/apply.ts           # apply
bun run tools/omp-patch-custom-mcp/apply.ts --status  # check
bun run tools/omp-patch-custom-mcp/apply.ts --reverse # revert
```

Runner 自动定位 OMP 全局安装目录，用 `git apply` 打补丁。`--status` 返回 `needs-rebase` 说明版本不匹配。
