# context-mode

外部工具参考页。

## 来源

- GitHub: `mksglu/context-mode`
- URL: <https://github.com/mksglu/context-mode>

## 为什么选它

- Claude Code 里主力跑国产模型（GLM 为主），有效上下文窗口比 Anthropic 官方模型短得多
- 大输出堆进对话很快把窗口吃满，接着就是幻觉、丢指令、回答崩坏
- context-mode 把原始数据关在 sandbox，只让摘要回流，窗口占用维持在合理区间，延缓幻觉临界点
- 与 RTK 互补（见下），两者叠加覆盖「进 / 不进上下文」两个层面
- 附带 session continuity：SQLite + FTS5 知识库，`/clear` / compact 后可按 BM25 检索已索引内容

## 具体原理

两套机制配合:PreToolUse hook 分档拦截 / 建议、MCP tool 真正做 sandbox 隔离。

### 1. PreToolUse hook:按工具分档(不是全员 advisory)

源码在 `hooks/core/routing.mjs` 的 `routePreToolUse()`。按规范化后的工具名 + 命令特征分五挡:

| 场景 | action | 效果 |
|---|---|---|
| `WebFetch` | `deny` + reason | 硬拦,直接禁用 |
| `curl`/`wget` 非静默或 stdout 输出 | `modify` → `echo "..."` | 硬拦(命令被换成无害 echo) |
| 内联 `fetch()` / `requests.get` / `http.get` | `modify` → `echo` | 同上 |
| `gradle` / `mvn` / `gradlew` / `mvnw` | `modify` → `echo` | 同上 |
| 其余 `Bash` / `Read` / `Grep` | `context` + `additionalContext` | 贴便利贴(advisory) |

执行链(以一般 Bash 为例):

```
Bash 被触发
    ↓
PreToolUse hook (hooks/pretooluse.mjs)
    ↓
routePreToolUse() → guidanceOnce("bash", BASH_GUIDANCE)
    ↓
返回 { action: "context", additionalContext: "<context_guidance>...</context_guidance>" }
    ↓
formatPreToolUseResponse(claude-code) 包成 { additionalContext: <tip> }
    ↓
Claude Code 原生把 additionalContext 注入模型对话
    ↓
Bash 照样执行,输出照样进上下文 —— tip 只影响下一次决策
```

关键细节:

- **一个 session 每种 tip 只发一次**。`guidanceOnce()` 用 `/tmp/context-mode-guidance-<ppid>/<type>` 文件锁 + in-memory Set 双保险,不会每次 Bash 都刷屏
- **工具名跨平台归一化**。`run_shell_command`/`bash`/`shell`/`run_in_terminal` 等都映射到 canonical `Bash`,所以 ctx 在 Claude Code / Gemini CLI / Cursor / Codex / VS Code Copilot 都认得
- **危险场景真的硬拦**(`deny` 或 `modify` → echo),不是光嘴说;只有无法等价改写的一般 Bash 才退回 advisory
- **MCP execute 同样走安全策略**。`ctx_execute(language: "shell", ...)` 会再过一遍用户的 Bash deny/allow 规则,避免模型借 sandbox 绕权限
- `additionalContext` 是 Claude Code PreToolUse hook 的原生字段,作用是「工具执行前往模型输入塞一段文本」
- tip 模板硬编码在 `hooks/routing-block.mjs`(Read/Grep/Bash 三套,以及 WebFetch/curl/gradle 的长 reason)

### 2. MCP tool:真 sandbox 隔离(主力)

- `ctx_execute` / `ctx_execute_file` / `ctx_batch_execute` / `ctx_fetch_and_index` 在独立子进程跑代码 / 抓 URL
- 原始输出写入 `~/.context-mode/` 下 SQLite FTS5 库,仅 `console.log()` 摘要返回对话
- `ctx_search` 事后按 BM25 按需检索已索引内容
- **唯一真正的 sandbox 路径** —— 一般 Bash 走 hook 的 advisory,要想进沙盒必须模型主动选 MCP tool

## 与 RTK 会冲突吗

**不冲突。** 两者同挂 Bash PreToolUse,但解决的问题不同,互不覆盖:

| | RTK | context-mode |
|---|---|---|
| 改命令能力 | 有(`updatedInput.command`) | 有(`action:"modify" + updatedInput`) |
| 一般 Bash 处理 | 改写成 `rtk <cmd>` 压缩包装 | 发一次 tip,不改写 |
| 危险场景(WebFetch/curl/gradle) | matcher 只 Bash,不介入 | 硬拦(`deny` 或 `modify`→echo) |
| 首次生效 | 所有匹配命令 ✅ | 危险场景 ✅;一般 Bash ❌(只建议) |
| 核心目标 | Token 压缩 | Sandbox 隔离 + 索引检索 |
| 架构 | shell hook → `rtk rewrite` Rust CLI | mjs hook → `routePreToolUse` → 模板 |

执行顺序:Bash 调用触发 → Claude Code 按顺序跑两个 hook → RTK 先改命令(`git status` → `rtk git status`)→ ctx 后发 tip → 最终执行 RTK 改写版。ctx 不会再改 RTK 改过的命令,因为 ctx 只在一般 Bash 上返回 `context`,不是 `modify`;RTK 也不会改 ctx 的 `echo "..."` 替换产物,因为 RTK registry 不认这些 echo。

MCP tool 通道(`ctx_execute` 等)RTK matcher 不认 Bash 之外的工具,完全不介入;此时才是真正的 sandbox。

**分工定位**:

- **RTK** = 一般 Bash 输出**必进上下文**,所以尽量压缩体积(工程手段:改 wrapper)
- **context-mode** = 明确危险场景**硬拦**,sandbox 隔离靠模型**主动调 MCP**(命令无法等价翻译成 sandbox 代码,只能 nudge)

「ctx 对一般 Bash 不如 RTK 那样稳」 —— 这是架构决定的,不是实现偷懒:`git log -200` 没法机械翻译成 `ctx_execute(code: ...)`,模型要自己把意图写成代码才能进沙盒。

## 与本仓库的关系

- 纯外部工具参考页，不在 `mcp/` 下重复写接入指南
- 若项目要硬性约束「大输出必须走 sandbox」，可在 `agent-instructions/claude/` 新增规则片段引用本页
