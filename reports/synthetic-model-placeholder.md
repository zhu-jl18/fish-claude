# Claude Code `<synthetic>` 模型名占位符

> 调研日期：2026-04-25

## 问题

运行 `tokscale` 时会发现一条不认识的模型记录：

```
│ Claude │ anthropic │ <synthetic> │ 0 │ 0 │ $0.00 │ — — │
```

Provider 显示 `anthropic`，但模型名是 `<synthetic>`，input/output token 全为 $0$。

## 结论

**`<synthetic>` 不是真实模型，是 Claude Code 在 API 请求失败时自动生成的占位记录。**

当请求出错（模型不存在、限速 429、服务不可用 503/502、上下文溢出等），客户端拿不到真实模型名，就填 `<synthetic>` 写入会话日志，附带一条错误消息。token 全为 0，没有实际调用发生。

**与第三方代理无关，与 Synthetic 平台无关。** 就是 Claude Code 自身行为。

## 本地数据

扫描全部会话文件，找到 **48 条** `<synthetic>` 记录，横跨 **8 个版本**（v2.1.81 ~ v2.1.119），时间跨度 2026-03-27 ~ 2026-04-25。

触发场景：

| 场景 | 次数 |
|------|------|
| 模型不存在/无权限 | 12 |
| 503 Service Unavailable | 8 |
| 静默丢弃（No response requested） | 8 |
| 429 Rate Limit | 4 |
| 400 Bad Request | 4 |
| 502 Gateway Error | 2 |
| Context Window Overflow | 2 |
| 500 Internal Error | 2 |
| 网络错误 | 2 |
| 其他 | 4 |

最新版 v2.1.119 今天凌晨仍有 9 条，均为模型不存在错误。

## 典型错误内容

```
There's an issue with the selected model (claude-sonnet-4-6). It may not exist or you may not have access to it.
API Error: 503 {"error":{"message":"Service Unavailable"}}
API Error: Request rejected (429) · Rate limit reached for requests
API Error: The model has reached its context window limit.
No response requested.
```

