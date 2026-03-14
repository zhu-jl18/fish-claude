# harness

长运行 agent 框架 pack 参考页。

## 来源

- 来自: `makoMakoGo/code-dispatcher-toolkit` → `bundles/harness/`
- URL: <https://github.com/makoMakoGo/code-dispatcher-toolkit/tree/main/bundles/harness>

## 简介

- Claude Code 长运行会话 skill+hook 组合包，用于跨上下文窗口的任务持久化、失败恢复和进度追踪
- 核心由 skill 协议（状态机与恢复规则）+ 项目 hooks（防止过早停止）组成，运行时状态统一写入 `.harness/`
- 移植自 cexll/myclaude，与 code-dispatcher 互补而非替代

## 包含组件

| 类型 | 内容 |
| --- | --- |
| Skill | `SKILL.md` — harness 协议与恢复规则 |
| Hooks | 8 个 Python 脚本（Stop / SessionStart / TeammateIdle / SubagentStop / self-reflect） |
| Config | `settings.json` — hook 注册配置片段 |
| Tests | hook 测试与基础 e2e 场景 |

## 命令

- `/harness init <project-path>` — 初始化
- `/harness run` — 启动/恢复无限循环
- `/harness status` — 查看进度与统计
- `/harness add "task description"` — 添加任务
