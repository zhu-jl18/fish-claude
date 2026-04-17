# sub-agents

## Claude

| 模块 | 说明 | 适用场景 |
| ---- | ---- | -------- |
| [code-simplifier](claude/code-simplifier.md) | 代码简化与精炼专家，提升可读性和一致性 | 代码重构、风格统一、可维护性优化 |

Claude 的协作分两条路线：**subagent**（单会话专家）和 **agent teams**（多会话协作，experimental）。

### Subagent

定义形态是 `Markdown + YAML frontmatter + prompt body`：frontmatter 是结构化元数据，body 是这个 subagent 自己的 system prompt——一份具名专家卡片，不是单纯说明文字。

触发方式是 trigger / delegation：host 结合 subagent 的 `description` 与当前任务 / 上下文自动派发，也可以显式指名调用。

**Frontmatter 字段**（来自 Claude Code 官方文档）：

| 字段 | 必填 | 作用 |
| ---- | :---: | ---- |
| `name` | ✅ | 唯一标识，小写 + 连字符 |
| `description` | ✅ | host 调度依据；告诉 Claude 何时派发 |
| `tools` | — | tool allowlist；省略则继承 host 当前可用工具 |
| `disallowedTools` | — | 从继承列表中剔除的 tool |
| `model` | — | `sonnet` / `opus` / `haiku` / 具体 model id / `inherit`（默认） |
| `permissionMode` | — | `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan` |
| `maxTurns` | — | 最大 turn 数，到上限自动停 |
| `skills` | — | 启动时注入的 skill 列表（subagent **不继承** host 的 skill） |
| `mcpServers` | — | 该 subagent 可用的 MCP server |
| `hooks` | — | subagent 作用域的 lifecycle hook |
| `memory` | — | 持久 memory scope：`user` / `project` / `local` |
| `background` | — | 是否默认以后台任务形式运行 |
| `effort` | — | 覆盖 session effort：`low` / `medium` / `high` / `max` |

**关键机制**：

- 独立 context window，不继承 host 的 system prompt 与对话历史；隔离上下文执行任务，将结果汇总回主线程
- tool / permission 可单独配置，`tools` + `disallowedTools` + `permissionMode` 三层覆写
- 定义来源：`--agents` CLI flag、项目级 `.claude/agents/`、用户级 `~/.claude/agents/`、插件内 `agents/`
- 支持 foreground / background、resume、transcript、hooks
- Subagent **不能**再 spawn 其他 subagent（无嵌套）

### Agent Teams（experimental）

与 subagent 不是同一层东西。subagent 是单会话里的隔离 worker，用来压缩上下文 / 返回摘要；agent teams 是多会话协作系统：**lead + teammates + shared task list + mailbox**，队友之间可直接通信，file locking 防止抢同一文件。适合需要长期分工协作的场景。

### 与 Codex 的差异

Claude = "预定义领域专家，host 按 `description` 自动派发"；Codex = "主 agent 自己当调度器，spawn 通用 lane 分工"。Claude subagent 偏专家卡片，Codex role 偏通用能力。



## Oh My Pi

OMP 的 subagent 是两层：**内置 Task 工具** + **swarm-extension** 包。没有专门的 role metadata 配置文件，角色由调用时的 prompt 直接描述。

### 内置 Subagent（Task 工具）

源码：`packages/coding-agent/src/prompts/system/subagent-*.md`。Host agent 通过 Task 工具派发子任务，每个 subagent 跑在独立 OMP session 里。

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

关键约束：

- subagent **独立 context**，不继承 host 对话历史
- 结束条件**唯一**：调用 `submit_result`。不允许在正文里塞 JSON、也不允许用文本摘要代替 `result.data`
- skill 继承：Task subagent 走正常 session 创建流程，继承当前 session 的 discovered skills；**不支持** per-task skill pinning（源码 `docs/skills.md`）
- 可选 `worktree` 参数：subagent 在隔离 git worktree 里干活，物理防止误改主仓

### swarm-extension（DAG 编排）

官方 package：`packages/swarm-extension/`。把多 agent 工作流写成 YAML，调度器构建 DAG、拓扑排序成 wave，每个 agent 是完整 OMP subagent（full tool set：bash / python / read / write / edit / grep / find / fetch / web_search / browser）。

**使用入口**：

- TUI 内：`/swarm <path-to.yaml>`（注册自 `src/extension.ts`）
- 独立运行：`bun run src/cli.ts <path-to.yaml>`（无 TUI、无 timeout，适合长跑）

**YAML 结构**：

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

**三种执行模式**：

| Mode | 行为 |
| ---- | ---- |
| `sequential`（默认） | 按声明顺序串行跑一遍 |
| `parallel` | 所有 agent 并发（除非有 `waits_for` / `reports_to` 强制排序） |
| `pipeline` | 把整张 agent DAG 重复跑 `target_count` 次（累积式工作，如 "找 50 个东西，每轮找一个"） |

**DAG 调度细节**（源码 `src/swarm/dag.ts`）：

- `waits_for: [a, b]` — 两者都完成才启动
- `reports_to: [x]` — 等价于 `x.waits_for` 加上自己
- 同一 wave 内并发执行；wave 之间按拓扑序串行
- 有 cycle 直接拒绝执行

**Agent 通信**：**只走共享 workspace 文件系统**。orchestrator **不传递数据**，只管启停顺序。常见协议：signal files（`signals/*.txt` 状态标记）、结构化输出（`analyzed/item_N.md`、`results/*.json`）、tracking files（`processed.txt` 去重）。

### 与 Claude / Codex 的差异

- **定义形态**：Claude 是结构化 frontmatter + markdown；Codex 是 TOML role layer；OMP 内置 subagent **没有持久 role 配置**，由调用时 prompt 动态组装
- **嵌套**：Claude subagent 不能再 spawn；Codex 有 `max_depth` 控制；OMP 内置 Task 无显式嵌套限制（每个都是独立 session）
- **结构化返回**：OMP 是三家里**唯一强制**的——必须 `submit_result`，可选 `outputSchema`（JTD）校验
- **多 agent 编排**：Claude 靠 agent teams（experimental）；Codex 靠 multi-agent v2 tool surface + role；OMP 靠 swarm-extension DAG YAML，**把编排从 prompt 里抽出来写成配置文件**，最贴近传统 CI / workflow 模型



## Codex

`codex/*.toml` 是 Codex role layer 的唯一真源；`config-files/codex/` 里的主配置只引用 `agents/*.toml` 布局，不再重复维护。

| 文件 | Role | 用途 |
| ---- | ---- | ---- |
| [default.toml](codex/default.toml) | `default` | 默认协作 role，通用任务派遣 |
| [explorer.toml](codex/explorer.toml) | `explorer` | 只读证据收集、高上下文代码理解 |
| [worker.toml](codex/worker.toml) | `worker` | 有界实现 / 编辑类执行任务 |
| [spark.toml](codex/spark.toml) | `spark` *(本地)* | 128k 文本-only，低上下文速度优先 |
| [awaiter.toml](codex/awaiter.toml) | `awaiter` *(本地)* | 长运行命令的等待 / 轮询 |
| [role-layer.example.toml](codex/role-layer.example.toml) | — | role layer 写法示例 |

官方 builtin role 当前是 `default / worker / explorer`；`spark`、`awaiter` 是本仓库自定义。

### 与 Claude subagent 的差异

Claude 是"预定义领域专家，按 description 自动派发"；Codex 是"主 agent 自己当调度器，spawn 子线程按职能分工"。所以 Codex role 偏通用 lane（探索 / 执行 / 等待），不走专家卡片路线。

### multi-agent 两个 flag 的关系

Codex 的 multi-agent 走**门控 + 变体切换**两层 feature flag（源码 `codex-rs/features/src/lib.rs` + `tools/src/tool_registry_plan.rs`）：

| Flag | 角色 | Stage | Default |
| ---- | ---- | ----- | ------- |
| `multi_agent` | **门控**；是否注册 multi-agent tool | Stable | **true** |
| `multi_agent_v2` | **变体切换**；v1 还是 v2 tool surface | UnderDevelopment | false |

注册逻辑等价于：

```
if multi_agent {
    if multi_agent_v2 { register v2 tools }
    else              { register v1 tools }
}
```

组合矩阵：

| `multi_agent` | `multi_agent_v2` | 实际注册 |
| --- | --- | --- |
| true  | true  | **v2 tools**（`spawn_agent / send_message / followup_task / wait_agent / close_agent / list_agents`） |
| true  | false | v1 tools（`spawn_agent / send_input / resume_agent / wait_agent / close_agent / list_agents`） |
| false | \*    | 啥都不注册（门控关了，v2 单开无用） |

要点：
- 两个 flag **不是互斥**，而是**叠加**。v2 依赖 `multi_agent` 门控才能 register。
- 同一 session `if/else` 互斥，v2 开启后 v1 tools 完全不注册，模型层看不到 v1。
- `multi_agent = true` 默认就是 true，显式写是**防御性冗余**（防 upstream 改 default + 意图明确）。只写 `multi_agent_v2 = true` 也能工作。

### 配置生效机制

- `config.toml` 里 `[agents.<role>]` 负责 role metadata：`description`（给 host agent 调度用）、`config_file`、`nickname_candidates`
- role 自己实际收到的 prompt 写在 role layer 的 `developer_instructions`
- 同名 `[agents.<role>]` shadow 掉 builtin 对应项
- role layer 只覆写文件里实际写出的键，其余继承父线程当前有效配置
- spawn runtime 会重写 live `approval_policy`、`shell_environment_policy`、`sandbox`、`cwd`（源码 `core/src/tools/handlers/multi_agents_common.rs`），这几项放 role layer 里没用
- 调度侧配置：`[agents]` 下的 `max_threads`、`max_depth` 控制并发与嵌套深度



## Gemini CLI

Gemini CLI 的 subagent 是把每个 agent 暴露成**同名 tool**给主 agent；主 agent 调这个 tool 就等于委派任务。支持 local 和 remote（Agent2Agent / A2A 协议）两种形态。

### 定义形态

与 Claude 类似：**Markdown + YAML frontmatter**，body 就是该 subagent 的 system prompt。

放置位置：

- 项目级：`.gemini/agents/*.md`（随仓库共享）
- 用户级：`~/.gemini/agents/*.md`（个人私有）

### Frontmatter Schema

官方文档 `docs/core/subagents.md` 的 **Configuration schema**：

| 字段 | 类型 | 必填 | 作用 |
| ---- | ---- | :---: | ---- |
| `name` | string | ✅ | slug 形式（小写 + 数字 + `-` / `_`）；作为 tool name 暴露给主 agent |
| `description` | string | ✅ | 给主 agent 看的调度依据 |
| `kind` | string | — | `local`（默认）/ `remote` |
| `tools` | array | — | tool 白名单，支持通配符 `*` / `mcp_*` / `mcp_<server>_*`；省略则继承主 session 所有 tool |
| `mcpServers` | object | — | 仅对这个 subagent 可见的 inline MCP server |
| `model` | string | — | 具体 model id（如 `gemini-3-flash-preview`）；默认 `inherit` |
| `temperature` | number | — | 0.0–2.0，默认 1 |
| `max_turns` | number | — | 最大对话轮数，默认 30 |
| `timeout_mins` | number | — | 最长执行时间（分钟），默认 10 |

**Frontmatter 示例**（`docs/core/subagents.md`）：

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

- **自动派发**：主 agent 根据 subagent 的 `description` 自动决定是否调用
- **强制派发**：`@<subagent-name> <prompt>`（例如 `@security-auditor ...`）

### Tool 隔离 + Policy Engine

每个 subagent 可独立声明：

- `tools` 白名单 + 通配符
- inline `mcpServers`（只对本 subagent 可见，不污染全局）
- Policy Engine 的 `[[rules]]` 可加 `subagent = "..."` 字段做 per-subagent 权限规则（`policy.toml`）

### Recursion Protection

**subagent 不能调用其他 subagent**，即使 `tools: ["*"]` 也看不到其他 agent tool。硬规则，防止无限嵌套。

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

### 与 Claude / Codex / OMP 的差异

- **暴露方式**：Claude subagent 是 "按 description 自动路由的委派目标"；Codex role 是 "主 agent 自己 spawn 子线程时选的 lane"；Gemini 更激进——**subagent 直接以 tool name 暴露给主 agent**，调用语义等同于 tool call
- **远程能力**：Gemini 是四家里**唯一内置标准化远程协议（A2A）** 的。Codex 的 multi-agent 和 OMP swarm 都只跑本地 subprocess
- **Tool 白名单精度**：Gemini 的 `tools` 支持三级通配符（`*` / `mcp_*` / `mcp_<server>_*`）+ policy.toml per-subagent 规则，是四家里最细的
- **嵌套保护**：Gemini 和 Claude 一样硬禁止 subagent 嵌套；Codex 靠 `max_depth` 限额；OMP swarm 则是靠 DAG cycle 检测
