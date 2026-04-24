# omp-patch-codex-websearch-byok

让 OMP codex `web_search` provider 支持自定义 Responses 兼容后端，不强制 ChatGPT OAuth。

- 从 OMP agent 配置解析 `baseUrl`、`apiKey`、模型
- 保留 OAuth 路径；BYOK 配置可用时优先走自定义后端
- 补齐网关返回的 markdown 链接 / `web_search_call` 来源提取

```bash
bun run tools/omp-patch-codex-websearch-byok/apply.ts           # apply
bun run tools/omp-patch-codex-websearch-byok/apply.ts --status  # check
bun run tools/omp-patch-codex-websearch-byok/apply.ts --reverse # revert
```

Runner 自动定位 OMP 全局安装目录，用 `git apply` 打补丁。`--status` 返回 `needs-rebase` 说明版本不匹配。
