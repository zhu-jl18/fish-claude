# omp-patch-custom-mcp

给已安装的 OMP 二进制打本地补丁，为 MCP 发现增加细粒度的用户级开关。

## What changes

- 新增 `mcp.enableClaudeUser` 设置，用于控制是否加载 Claude Code 用户级 MCP。
- 新增 `mcp.enableCodexUser` 设置，用于控制是否加载 Codex 用户级 MCP。
- 在 MCP 重新发现与连接路径中透传这两个设置，避免只能全开或全关用户级来源。

## Usage

```bash
bun run tools/omp-patch-custom-mcp/apply.ts          # apply
bun run tools/omp-patch-custom-mcp/apply.ts --status # check status
bun run tools/omp-patch-custom-mcp/apply.ts --reverse # revert
```

## Notes

- 目录内包含 `apply.ts` 与 `patch.diff`。
- runner 会自动定位全局安装的 OMP 包根目录，并用 `git apply` 执行补丁。
- `--status` 返回 `needs-rebase` 时，说明当前安装版本与补丁不再干净匹配，需要手动 rebase。
