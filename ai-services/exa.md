# Exa

Exa 是面向 AI 应用的搜索与内容提取服务，常用于语义搜索、网页抓取和结果摘要。

- 官网：<https://exa.ai>
- 文档：<https://docs.exa.ai>
- Hosted MCP：`https://mcp.exa.ai/mcp`
- 类型：语义搜索与内容提取 API

## 免费额度

- 注册即送约 1000 次免费查询额度
- 偶尔会有兑换码
- Hosted MCP 免费接口

## Hosted MCP 免费计划与限流

Exa 提供 hosted MCP 服务，并带有免费计划，但官方未公开具体限流阈值。文档同时说明：如果命中免费计划的限流，可能返回 `429`；如果要绕过免费计划限流并用于生产环境，应改为携带自己的 API key。

## 配置示例

### 不带 API key

```json
{
  "mcpServers": {
    "exa": {
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

### 带 API key

```json
{
  "mcpServers": {
    "exa": {
      "url": "https://mcp.exa.ai/mcp",
      "headers": {
        "x-api-key": "YOUR_EXA_API_KEY"
      }
    }
  }
}
```

## OMP 中的例子

OMP 里实际就两种调用方式：

- 有 `EXA_API_KEY`：走 Exa Search API 直连，即 `POST https://api.exa.ai/search`
- 没有 `EXA_API_KEY`：fall back 到 Exa hosted MCP，即 `https://mcp.exa.ai/mcp?tools=web_search_exa`


## 参考

- Exa MCP：<https://docs.exa.ai/reference/exa-mcp>
- Exa Rate Limits：<https://docs.exa.ai/reference/rate-limits> 