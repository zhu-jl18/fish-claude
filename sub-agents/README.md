# sub-agents

## 总览

| CLI | 定义形态 | 派发方式 | 嵌套 | 远程 | 亮点 |
|-----|---------|---------|------|------|------|
| Claude | frontmatter + markdown | 自动（按 description）或显式指名 | 禁止 | — | 专家卡片，独立 context |
| Codex | TOML role layer | 主 agent spawn 子线程 | `max_depth` 控制 | — | 通用 lane 分工 |
| OMP | 调用时 prompt 动态组装 | Task 工具派发 | 无限制（独立 session） | — | swarm DAG 编排 + 强制结构化返回 |
| Gemini | frontmatter + markdown | 以 tool name 暴露，自动或 `@name` | 硬禁止 | A2A 协议 | tool 级白名单 + 远程 subagent |

---

## Claude

| 模块 | 说明 | 适用场景 |
| ---- | ---- | -------- |
| [code-simplifier](claude/code-simplifier.md) | 代码简化与精炼专家，提升可读性和一致性 | 代码重构、风格统一、可维护性优化 |

Claude 有两条协作路线：**subagent**（单会话内派发专家）和 **agent teams**（多会话协作，experimental）。

### Subagent

每个 subagent 是一个 Markdown 文件，YAML frontmatter 写元数据，body 是它自己的 system prompt——本质上是一张具名专家卡片。

Host 会根据 subagent 的 `description` 结合当前任务自动派发，也可以显式指名调用。

**Frontmatter 字段**（来自 Claude Code 官方文档）：

| 字段 | 必填 | 作用 |
| ---- | :---: | ---- |
| `name` | ✅ | 唯一标识，小写 + 连字符 |
| `description` | ✅ | host 调度依据 |
| `tools` | — | tool 白名单；不写就继承 host 当前可用工具 |
| `disallowedTools` | — | 从继承列表里剔除的 tool |
| `model` | — | `sonnet` / `opus` / `haiku` / 具体 model id / `inherit`（默认） |
| `permissionMode` | — | `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan` |
| `maxTurns` | — | 最大 turn 数，到上限自动停 |
| `skills` | — | 启动时注入的 skill 列表（subagent **不继承** host 的 skill） |
| `mcpServers` | — | 该 subagent 可用的 MCP server |
| `hooks` | — | subagent 作用域的 lifecycle hook |
| `memory` | — | 持久 memory scope：`user` / `project` / `local` |
| `background` | — | 是否默认后台运行 |
| `effort` | — | 覆盖 session effort：`low` / `medium` / `high` / `max` |

几个要点：

- 独立 context window，不继承 host 的 system prompt 和对话历史；跑完把结果汇总回主线程
- tool 和 permission 可单独配：`tools` + `disallowedTools` + `permissionMode` 三层覆写
- 定义来源：`--agents` CLI flag、`.claude/agents/`（项目）、`~/.claude/agents/`（用户）、插件 `agents/`
- 支持 foreground / background、resume、transcript、hooks
- Subagent **不能**再 spawn 其他 subagent（无嵌套）

### Agent Teams（experimental）

跟 subagent 不同层。subagent 是单会话里的隔离 worker，用来压上下文、返回摘要；agent teams 是多会话协作系统：**lead + teammates + shared task list + mailbox**，队友之间直接通信，file locking 防抢同一文件。适合需要长期分工协作的场景。

---

## Codex

`codex/*.toml` 是 Codex role layer 的唯一真源；`config-files/codex/` 里的主配置只引用 `agents/*.toml`，不重复维护。

| 文件 | Role | 用途 |
| ---- | ---- | ---- |
| [default.toml](codex/default.toml) | `default` | 默认协作 role，通用任务派遣 |
| [explorer.toml](codex/explorer.toml) | `explorer` | 只读证据收集、高上下文代码理解 |
| [worker.toml](codex/worker.toml) | `worker` | 有界实现 / 编辑类执行任务 |
| [spark.toml](codex/spark.toml) | `spark` *(本地)* | 128k 文本-only，低上下文速度优先 |
| [awaiter.toml](codex/awaiter.toml) | `awaiter` *(本地)* | 长运行命令的等待 / 轮询 |
| [role-layer.example.toml](codex/role-layer.example.toml) | — | role layer 写法示例 |

官方 builtin role：`default / worker / explorer`；`spark`、`awaiter` 是本仓库自定义。

### vs Claude

Claude 是"预定义领域专家，host 按 description 自动派发"；Codex 是"主 agent 自己当调度器，spawn 子线程按职能分工"。Codex role 偏通用 lane（探索 / 执行 / 等待），不走专家卡片路线。

### multi-agent 底层

multi-agent 的 feature flag 矩阵和配置生效细节见 [codex/multi-agent-internals.md](codex/multi-agent-internals.md)。

---

## Oh My Pi

OMP 的 subagent 分两层：**内置 Task 工具** + **swarm-extension** 包。没有专门的 role 配置文件，角色在调用时直接用 prompt 描述。

### 内置 Subagent（Task 工具）

源码在 `packages/coding-agent/src/prompts/system/subagent-*.md`。Host 通过 Task 工具派发子任务，每个 subagent 跑在独立 OMP session 里。

系统 prompt 结构（handlebars 模板）：

```
{{base}}                               # 基础 system prompt
# Acting as: {{agent}}                 # 本次角色描述（调用方提供）
# Job: 你在处理一个委派的 sub-task
  ├─ {{worktree}}   可选：隔离工作树，不得修改外部文件
  └─ {{contextFile}} 可选：conversation 导出文件，可 tail/grep
# Closure: 必须恰好调用一次 submit_result，否则任务不算关
  └─ {{outputSchema}} 可选：结构化 JTD schema，结果必须匹配
# Giving Up: 放弃是最后手段；必须用 submit_result 的 result.error 说明
```

几个约束：

- subagent **独立 context**，不继承 host 对话历史
- 结束条件**唯一**：调用 `submit_result`。不能在正文里塞 JSON，也不能用文本摘要代替 `result.data`
- skill 继承：Task subagent 走正常 session 创建流程，继承当前 session 的 discovered skills；**不支持** per-task skill pinning（源码 `docs/skills.md`）
- 可选 `worktree` 参数：subagent 在隔离 git worktree 里干活，物理防误改主仓

### swarm-extension（DAG 编排）

官方 package：`packages/swarm-extension/`。把多 agent 工作流写成 YAML，调度器构建 DAG、拓扑排序成 wave。每个 agent 是完整 OMP subagent（full tool set：bash / python / read / write / edit / grep / find / fetch / web_search / browser）。

入口：

- TUI 内：`/swarm <path-to.yaml>`（注册自 `src/extension.ts`）
- 独立运行：`bun run src/cli.ts <path-to.yaml>`（无 TUI、无 timeout，适合长跑）

YAML 结构：

```yaml
swarm:
  name: my-pipeline          # 必填，state 存在 .swarm_<name>/
  workspace: ./workspace     # 必填，共享工作目录
  mode: pipeline             # pipeline | parallel | sequential（默认 sequential）
  target_count: 10           # pipeline 模式的迭代次数，默认 1
  model: claude-opus-4-6     # 默认 model（可被 per-agent 覆盖）

  agents:
    finder:
      role: web-scraper                 # 必填，作为 system prompt
      task: |                           # 必填，多行 user prompt
        Find 10 relevant URLs …
      extra_context: |                  # 可选，附加到 system prompt
        Only consider sources after 2024.
      reports_to: [analyzer]            # 可选，声明下游
      waits_for: []                     # 可选，声明上游
      model: claude-sonnet-4-5          # 可选，per-agent 覆盖
```

三种执行模式：

| Mode | 行为 |
| ---- | ---- |
| `sequential`（默认） | 按声明顺序串行跑一遍 |
| `parallel` | 所有 agent 并发（除非 `waits_for` / `reports_to` 强制排序） |
| `pipeline` | 整张 agent DAG 重复跑 `target_count` 次（累积式工作，如"找 50 个东西，每轮找一个"） |

DAG 调度（源码 `src/swarm/dag.ts`）：

- `waits_for: [a, b]` — 两者都完成才启动
- `reports_to: [x]` — 等价于 `x.waits_for` 加上自己
- 同一 wave 内并发执行；wave 之间按拓扑序串行
- 有 cycle 直接拒绝执行

Agent 间通信：**只走共享 workspace 文件系统**。orchestrator 不传数据，只管启停顺序。常见协议：signal files（`signals/*.txt` 状态标记）、结构化输出（`analyzed/item_N.md`、`results/*.json`）、tracking files（`processed.txt` 去重）。

---

## Gemini CLI

Gemini CLI 把每个 subagent 暴露成**同名 tool**给主 agent——主 agent 调这个 tool 就等于委派任务。支持 local 和 remote（Agent2Agent / A2A 协议）两种形态。

### 定义

与 Claude 一样：Markdown + YAML frontmatter，body 是 subagent 的 system prompt。

放置位置：

- 项目级：`.gemini/agents/*.md`（随仓库共享）
- 用户级：`~/.gemini/agents/*.md`（个人私有）

### Frontmatter Schema

官方文档 `docs/core/subagents.md`：

| 字段 | 类型 | 必填 | 作用 |
| ---- | ---- | :---: | ---- |
| `name` | string | ✅ | slug 形式（小写 + 数字 + `-` / `_`）；作为 tool name 暴露给主 agent |
| `description` | string | ✅ | 主 agent 的调度依据 |
| `kind` | string | — | `local`（默认）/ `remote` |
| `tools` | array | — | tool 白名单，支持通配符 `*` / `mcp_*` / `mcp_<server>_*`；不写继承主 session 所有 tool |
| `mcpServers` | object | — | 仅对该 subagent 可见的 inline MCP server |
| `model` | string | — | 具体 model id（如 `gemini-3-flash-preview`）；默认 `inherit` |
| `temperature` | number | — | 0.0–2.0，默认 1 |
| `max_turns` | number | — | 最大对话轮数，默认 30 |
| `timeout_mins` | number | — | 最长执行时间（分钟），默认 10 |

示例：

```yaml
---
name: security-auditor
description: Specialized in finding security vulnerabilities in code.
kind: local
tools:
  - read_file
  - grep_search
model: gemini-3-flash-preview
temperature: 0.2
max_turns: 10
---
```

### 内置 Subagent（源码 `packages/core/src/agents/`）

| Name | 角色 | 触发方式 |
| ---- | ---- | -------- |
| `codebase_investigator` | 代码库分析、依赖理解 | 自动派发 |
| `cli_help` | CLI 内置帮助 | 自动派发 |
| `generalist` | 全能代理，继承主 agent 全部 tool，用于高消耗子任务 | `@generalist` 显式调用 |
| `browser_agent` *(experimental)* | 浏览器自动化（需 Chromium） | 需显式启用 |
| `memory_manager` | 持久 memory 管理 | 内部调度 |
| `skill_extraction` | skill 抽取 | 内部调度 |

### 调用方式

- **自动派发**：主 agent 根据 subagent 的 `description` 自动决定
- **强制派发**：`@<subagent-name> <prompt>`（如 `@security-auditor ...`）

### 隔离与安全

每个 subagent 可独立声明 `tools` 白名单（支持三级通配符 `*` / `mcp_*` / `mcp_<server>_*`）和 inline `mcpServers`（只对本 subagent 可见，不污染全局）。Policy Engine 的 `[[rules]]` 可加 `subagent = "..."` 做 per-subagent 权限规则（`policy.toml`）。

**subagent 不能调用其他 subagent**——即使 `tools: ["*"]` 也看不到其他 agent tool。硬规则，防无限嵌套。

### Remote Subagent（A2A 协议）

源码 `packages/a2a-server/` + `packages/core/src/agents/a2a-client-manager.ts`。frontmatter 用 `kind: remote` 并给 `agent_card_url` 或 `agent_card_json`：

```yaml
---
name: my-remote-agent
kind: remote
agent_card_url: https://my-agent.example.com/.well-known/agent.json
auth:
  type: http
  scheme: Bearer
  token: $MY_BEARER_TOKEN
---
```

支持的鉴权：`apiKey` / `http`（Bearer / Basic / Raw）/ `google-credentials`（ADC）/ `oauth`。secret 值支持动态解析：`$ENV_VAR`、`!command`（shell 输出）、字面量、`$$` / `!!` 转义。
