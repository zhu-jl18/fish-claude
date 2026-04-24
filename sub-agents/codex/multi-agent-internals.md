# Codex Multi-Agent 底层细节

## feature flag 矩阵

Codex 的 multi-agent 走**门控 + 变体切换**两层 feature flag（源码 `codex-rs/features/src/lib.rs` + `tools/src/tool_registry_plan.rs`）：

| Flag | 角色 | Stage | Default |
| ---- | ---- | ----- | ------- |
| `multi_agent` | **门控**：是否注册 multi-agent tool | Stable | **true** |
| `multi_agent_v2` | **变体切换**：v1 还是 v2 tool surface | UnderDevelopment | false |

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

- 两个 flag **不是互斥**，是**叠加**。v2 依赖 `multi_agent` 门控才能 register
- 同一 session `if/else` 互斥，v2 开启后 v1 tools 完全不注册，模型层看不到 v1
- `multi_agent = true` 默认就是 true，显式写是**防御性冗余**（防 upstream 改 default + 意图明确）。只写 `multi_agent_v2 = true` 也能工作

## 配置生效机制

- `config.toml` 里 `[agents.<role>]` 负责 role metadata：`description`（给 host agent 调度用）、`config_file`、`nickname_candidates`
- role 自己实际收到的 prompt 写在 role layer 的 `developer_instructions`
- 同名 `[agents.<role>]` shadow 掉 builtin 对应项
- role layer 只覆写文件里实际写出的键，其余继承父线程当前有效配置
- spawn runtime 会重写 live `approval_policy`、`shell_environment_policy`、`sandbox`、`cwd`（源码 `core/src/tools/handlers/multi_agents_common.rs`），这几项放 role layer 里没用
- `[agents]` 下的 `max_depth` 控制嵌套深度；启用 `multi_agent_v2` 时不要再设置 `max_threads`
