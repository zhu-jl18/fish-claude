# context-mode

把大输出关在 sandbox，只让摘要进上下文，防止窗口被吃满。

## 来源

- GitHub：<https://github.com/mksglu/context-mode>

## 为什么选它

~~我用国产模型跑 Claude Code，有效上下文比官方模型短。~~

> [!NOTE]
> V4：我不在的时候你们几条野狗很嚣张啊

大输出堆进去很快就幻觉、丢指令。context-mode 把原始数据隔离在 sandbox（SQLite FTS5），只回流摘要，窗口占用可控。

与 RTK 互补：RTK 压缩必然进上下文的输出，context-mode 拦住不该进的。

## 怎么工作

两套机制配合：PreToolUse hook 分档拦截/建议，MCP tool 做真正的 sandbox 隔离。

### PreToolUse hook

按工具名 + 命令特征分档：

| 场景 | 处理 |
|------|------|
| `WebFetch` | 硬拦（deny） |
| `curl` / `wget` 非静默或 stdout 输出 | 硬拦（modify → echo） |
| `gradle` / `mvn` 等构建工具 | 硬拦（modify → echo） |
| 一般 `Bash` / `Read` / `Grep` | 贴 tip（advisory），建议走 sandbox |

每种 tip 一个 session 只发一次，不会重复刷屏。

### MCP tool（sandbox）

`ctx_execute` 在独立子进程跑代码，原始输出写 SQLite，仅摘要返回对话。`ctx_search` 事后按需检索。这才是真正的隔离——一般 Bash 靠模型收到 tip 后主动选 MCP tool 进 sandbox。

## 与 RTK 的配合

两者同挂 Bash PreToolUse，但匹配的命令不重叠：

- RTK 管它有 filter 的命令（git、cargo、npm 等），改写成 `rtk <cmd>` 压缩输出
- context-mode 管危险命令（curl、wget、gradle），硬拦改成 echo；一般 Bash 只贴 tip 建议走 sandbox

举个例：`git status` 触发 → RTK 改成 `rtk git status` → ctx 看这不是危险命令，只贴 tip → 最终执行 `rtk git status`。`curl https://...` 触发 → RTK 不认 curl，放过去 → ctx 认出危险，硬拦改成 echo → RTK 没介入。

各管各的，不打架。
