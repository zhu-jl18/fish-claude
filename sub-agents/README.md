# sub-agents

## Claude

| 模块 | 说明 | 适用场景 |
| ---- | ---- | -------- |
| [code-simplifier](claude/code-simplifier.md) | 代码简化与精炼专家，提升可读性和一致性 | 代码重构、风格统一、可维护性优化 |

Claude 的 subagent 机制可以分两个层面来看。

一是传统的领域专家 subagent，专人专责，例如`code-simplifier`这类专门做代码简化和精炼的 subagent。这一层整体上更接近 trigger / delegation：Claude 会结合 subagent 的 `description`、当前任务和当前上下文，自动判断是否满足条件来调用某个 subagent；当然也可以显式指定某个 subagent 来处理任务。

这类自定义 subagent 本质上是 `Markdown + YAML frontmatter + prompt body`。frontmatter 里通常放 `name`、`description`、`tools`、`model` 之类的配置，正文则是这个 subagent 自己的 system prompt。也就是说，它不是单纯一段说明文字，而是一个具名专家配置。

有几个机制细节需要明确：

- subagent 有自己的 context window，不会完整继承主 agent 的 system prompt 和对话历史，默认更像“隔离上下文后执行任务，再将结果汇总回主线程”
- tools 和 permissions 可以单独配置；tools 默认继承主线程当前可用工具，但也可以额外做 allowlist / denylist 和 permissionMode 覆写
- 定义来源不只有本地 `.md` 文件，还可以来自 `--agents`、项目级 `.claude/agents/`、用户级 `~/.claude/agents/` 和插件里的 `agents/`
- 单个 subagent 支持 foreground / background、resume、transcript、hooks 这些能力，但 subagent 不能继续 spawn 其他 subagent

二是更加灵活的 agent teams。Claude 官方已经将其作为正式的 experimental 机制开放。它和上面的 subagent 不是一回事：subagent 更像单会话里的专用 worker，用来隔离噪音、压缩上下文、返回摘要；agent teams 则更像多会话协作系统，有 lead、teammates、shared task list 和 mailbox，队友之间可以直接通信，还有 file locking 来避免抢同一个文件。至于它和 kimi 那种 swarm 的区别，后面可以再单独展开。



## Codex

| 模块 | 说明 | 职责 |
| ---- | ---- | ---- |
| `codex/*.toml` | Codex sub-agent role layer | 子代理角色配置；唯一模板来源 |
| [role-layer.example.toml](codex/role-layer.example.toml) | role layer 配置示例 | 配置模板参考 |

这里的 `codex/*.toml` 是 Codex role layer 的唯一真源。`config-files/` 里的 Codex 主配置模板只负责引用 `agents/*.toml` 这一目标布局，不再重复维护一份同内容文件。

Codex 更加类似于主 agent 自己 spawn 出 subagent thread 然后委派其任务，数目、角色和调用时机都由主 agent 控制，更加 autonomous，也更 orchestration-first 一些。因此它的 subagent role 一般不会特别强调领域专家，而是更偏 general 的功能分工。官方当前 builtin role 是 `default`、`worker`、`explorer`；这个仓库额外补了本地自定义的 `spark` 和 `awaiter`，分别负责默认协作、探索性任务、速度优先的低上下文任务、执行性任务和等待/观察类任务。主 agent 根据当前需要来 spawn 出不同 role 的 subagent 来协助完成任务，目的更像是加速主 agent 的任务完成效率，防止主 agent 被过于细节的上下文干扰注意力。

换句话说，Claude 更像是“有一组预定义专家，Claude 视情况把任务委派过去”；Codex 更像是“主 agent 本身就是调度器，需要的时候自己拉起几个子线程分工处理”。这也是为什么 Codex 的 subagent 角色通常更适合做 `default`、`explorer`、`spark`、`worker` 这类 lane，再按需要补本地自定义 role，而不是纯领域专家卡片。

具体的配置生效机制上，Codex 更接近一套明确的 multi-agent orchestration：

- `config.toml` 里的 `[agents.<role>]` 负责 role metadata：`description`、`config_file`、`nickname_candidates`
- `description` 主要给 host agent 看，负责告诉主线程“什么时候该派这个 role”；role 自己实际收到的 prompt 则放进对应 role layer 的 `developer_instructions`
- 同名 `[agents.<role>]` 会优先于 builtin role metadata；写了就会 shadow builtin 对应项
- role layer 只覆写文件里实际写出的配置键；没写的继续继承父线程当前有效配置  
- spawn runtime 会重新写回 live `approval_policy`、`shell_environment_policy`、`sandbox` 和 `cwd`，这些通常不值得放进 role layer
- 官方当前是默认开启 multi-agent，但 `spawn_agent` 仍属于显式授权工具。只有用户明确要求 delegation / sub-agents / parallel agent work 时才应该触发。
- 官方 multi-agent 文档里现在还有 `max_threads`、`max_depth` 这类调度配置，也明确写了 spawn、follow-up routing、wait、close 这些生命周期动作
- 当前官方 multi-agent 文档里的 builtin role 是 `default`、`worker`、`explorer`
- `spark` 和 `awaiter` 在这里是本地自定义 role，不是当前官方默认 builtin role
