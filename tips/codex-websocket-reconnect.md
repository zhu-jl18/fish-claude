# Codex CLI 重连五次问题

## 现象

每次启动 Codex CLI，提示 `Reconnecting...` 五次后才开始正常工作。

## 根因

Codex CLI 默认优先 WebSocket 传输。WebSocket 握手需要 `Connection: Upgrade` + `Upgrade: websocket`，很多代理/VPN/中转服务不支持或阻断这个头，导致握手失败。失败后 Codex 重试 5 次（`stream_max_retries`，默认 5），耗尽后才降级到 HTTP SSE。

源码 `ModelClient::active_ws_version()` 的传输选择优先级：

1. `provider.supports_websockets == false` → HTTP SSE
2. `disable_websockets == true`（运行时，WebSocket 失败后自动置位）→ HTTP SSE
3. `Feature::ResponsesWebsocketsV2` 启用 → WebSocket V2
4. `Feature::ResponsesWebsockets` 启用 → WebSocket V1
5. 以上都不满足 → HTTP SSE

降级是会话级且永久的：一旦触发 `activate_http_fallback()`，该会话后续所有 turn 都走 HTTP SSE，不再尝试 WebSocket。

## 解决

在 `~/.codex/config.toml` 的 `[features]` 中禁用 WebSocket，直接从 HTTP SSE 启动：

```toml
[features]
responses_websockets = false
```

或 CLI 参数：

```bash
codex --disable responses_websockets
```

## 参考

- [DeepWiki: Model Client and API Communication](https://deepwiki.com/openai/codex/3.2-input-handling-and-command-processing)
- [Codex CLI Changelog](https://developers.openai.com/codex/changelog/)
- [Codex CLI 配置详解 (CSDN)](https://yanglinwei.blog.csdn.net/article/details/157177301)
