# Tavily

Tavily 是面向 AI Agent 的搜索与提取服务，主打适合 LLM 的搜索结果与内容摘要。

- 官网：<https://tavily.com>
- 文档：<https://docs.tavily.com>
- API：`https://api.tavily.com/search`
- 类型：面向 AI Agent 的搜索与提取 API

## 免费额度

- 每月 1,000 API credits
- 无需信用卡
- Search `basic` 每次请求消耗 1 credit
- Search `advanced` 每次请求消耗 2 credits

## 请求示例

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tvly-YOUR_API_KEY" \
  -d '{"query":"latest ai agent news"}'
```

## 接入方式

- 主线就是带 API key 直连 Tavily Search API：`POST https://api.tavily.com/search`
- 鉴权方式是 `Authorization: Bearer tvly-YOUR_API_KEY`

## 参考

- Tavily Quickstart：<https://docs.tavily.com/documentation/quickstart>
- Tavily Credits & Pricing：<https://docs.tavily.com/documentation/api-credits>