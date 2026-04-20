# omp-patch-codex-websearch-byok

给已安装的 OMP 二进制打本地补丁，让 codex `web_search` provider 支持自定义 Responses 兼容后端，而不是强制依赖 ChatGPT OAuth。

## What changes

- 允许从 OMP agent 配置中解析 Responses 兼容 provider 的 `baseUrl`、`apiKey` 与模型。
- 保留原有 OAuth 路径；若存在可用的 BYOK 配置，则优先走自定义后端。
- 补齐网关返回的 markdown 链接 / `web_search_call` 来源提取。

## Usage

```bash
bun run tools/omp-patch-codex-websearch-byok/apply.ts          # apply
bun run tools/omp-patch-codex-websearch-byok/apply.ts --status # check status
bun run tools/omp-patch-codex-websearch-byok/apply.ts --reverse # revert
```

## Notes

- 目录内包含 `apply.ts` 与 `patch.diff`。
- runner 会自动定位全局安装的 OMP 包根目录，并用 `git apply` 执行补丁。
- `--status` 返回 `needs-rebase` 时，说明当前安装版本与补丁不再干净匹配，需要手动 rebase。
