# Context7 MCP

为 LLM 提供实时、版本准确的第三方库文档和代码示例。

## 安装

依赖：`npx`（通过 Node.js 提供）。

建议先在 [context7.com/dashboard](https://context7.com/dashboard) 申请免费 API Key 以获得更高速率限制。

### Claude Code 本地连接

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

去掉 `--scope user` 则仅对当前项目生效。

### Claude Code 远程连接

```bash
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

## 使用方式

提供两个工具：

1. `resolve-library-id` — 将库名解析为 Context7 兼容 ID
2. `query-docs` — 根据 ID 查询文档和代码示例

调用顺序：先 `resolve-library-id` 拿到 ID，再 `query-docs` 查文档。

## 注意事项

1. 无需 activate 或 onboarding 流程，装好即用。
2. API Key 不要硬编码到规则文件里，通过 `claude mcp add` 的参数传入。
3. 当行为可能因库版本不同而有差异时，先从 lockfile/config 确认项目版本，再带版本查询。
