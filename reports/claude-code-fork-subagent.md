# Claude Code forked subagent 机制说明

> 调研日期：2026-04-30
> 来源：Claude Code 官方文档、Claude Code changelog v2.1.117 / v2.1.121、GitHub issues #28570 / #39335 / #42621 / #34916

## 结论

`CLAUDE_CODE_FORK_SUBAGENT=1` 启用的是 **forked subagent**：子 agent 从当前主会话分叉出去，继承主会话已有上下文，而不是像普通 named subagent 那样从 fresh context 开始。

它适合当前上下文很重要、重新 briefing 成本高的并行任务。fork 的中间工具调用留在子上下文里，主会话只收到最终结果。

## 启用方式

写入 `~/.claude/settings.json`：

```json
{
  "env": {
    "CLAUDE_CODE_FORK_SUBAGENT": "1"
  }
}
```

## 使用方式

直接在 Claude Code 里运行：

```text
/fork draft unit tests for the parser changes so far
```

`/fork` 后面的内容就是 forked subagent 的 directive。fork 会在后台运行，你可以继续在主对话工作；完成后它会把结果回传到主对话。

## Background task 开关

| 配置 | 行为 |
|------|------|
| `CLAUDE_CODE_FORK_SUBAGENT=1` | fork 默认后台运行；主对话可以继续交互，fork 完成后把结果回传到主对话 |
| `CLAUDE_CODE_FORK_SUBAGENT=1` + `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` | 禁用 background task 功能；fork/subagent 以前台同步方式运行，主对话会等它完成后才继续 |

`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` 禁用的是 background task 能力本身，包括自动后台化和 `Ctrl+B` 后台化。官方文档把 foreground subagent 定义为 blocking：它会阻塞主对话直到完成；权限提示和澄清问题会透传到当前终端。

## 主对话生命周期与社区反馈

background fork/subagent 是异步任务。主对话在委派完成后可以进入 idle 状态，不需要持续心跳轮询；后台任务完成后通过 `<task-notification>` / 结果消息回到主对话。

社区反馈与这个模型一致，但也暴露出边界问题：

- GitHub issue #28570：background subagents 在主会话 stop 后仍可能继续运行，说明后台任务生命周期独立于主 turn。
- GitHub issue #39335：background subagent 完成通知有时不会实时到达，要等用户交互才 flush。
- GitHub issue #42621：background agent 完成通知可能触发新的 assistant turn；如果当时有 pending confirmation，存在自确认风险。
- GitHub issue #34916：`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` 对单个 subagent 有效，但多 subagent 场景曾被反馈仍会后台化；这属于实现 bug，不是目标语义。

## 启用后的行为变化

启用 `CLAUDE_CODE_FORK_SUBAGENT=1` 后有三点变化：

1. Claude 原本会使用 `general-purpose` subagent 的场景，会改为 forked subagent。
2. 所有 subagent spawn 默认后台运行。需要同步运行时可设置 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`。
3. `/fork` 变成启动 forked subagent，不再是 `/branch` 的别名。

如果需要原来的分支对话功能，明确使用：

```text
/branch
```

## forked subagent 与 named subagent 的区别

| 项 | Forked subagent | Named subagent |
|----|-----------------|----------------|
| 上下文 | 继承主会话完整 history | fresh context，只收到传入 prompt |
| system prompt / tools | 与主会话相同 | 来自 subagent definition |
| model | 与主会话相同 | 来自 subagent `model` 配置或继承主会话 |
| 中间工具调用 | 留在 fork 子上下文 | 留在 subagent 子上下文 |
| 回主对话 | 最终结果 | 最终结果 |
| prompt cache | 共享主会话 cache prefix | 独立 cache |

`Explore`、`Plan`、自定义 named subagent 仍按 named subagent 路径运行。fork 替代的是未指定具体 `subagent_type`、原本会落到 `general-purpose` 的默认路径。

## 使用判断

适合 fork：

- 子任务强依赖当前主对话背景
- 不想把大量搜索、测试、日志输出塞回主会话
- 想从同一个上下文起点并行探索多个方向
- 任务足够独立，可以后台完成后只回报结果

适合 named subagent：

- 任务角色稳定，例如 Explore、Plan、reviewer、debugger
- 希望用独立 system prompt、工具限制或模型配置
- 不希望子 agent 继承完整主会话上下文

## 限制

- forked subagent 不能继续 fork，避免递归分叉。
- fork 会继承完整主会话 history；长会话里 fork 的上下文更重，只是 prompt cache 能降低重复前缀成本。
- prompt cache 节省效果依赖 provider/gateway 对 Claude prompt caching 的支持。

## 关键参考

- Claude Code subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code changelog v2.1.117: https://code.claude.com/docs/en/changelog#2-1-117
- Claude Code changelog v2.1.121: https://code.claude.com/docs/en/changelog#2-1-121
- GitHub issue #28570: https://github.com/anthropics/claude-code/issues/28570
- GitHub issue #39335: https://github.com/anthropics/claude-code/issues/39335
- GitHub issue #42621: https://github.com/anthropics/claude-code/issues/42621
- GitHub issue #34916: https://github.com/anthropics/claude-code/issues/34916