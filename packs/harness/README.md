# harness

`harness` 是给 Claude Code 用的长运行任务 pack，用来把任务状态、恢复规则和生命周期 hooks 组织成一套可复用方案。适合跨上下文窗口、需要持续推进、或者要在多次会话里接着做的任务。

## 包含内容

- `SKILL.md`：定义任务状态机、恢复流程和执行约束
- `settings.json`：Claude Code hooks 配置片段
- `hooks/`：`Stop`、`SessionStart`、`TeammateIdle`、`SubagentStop` 等 hook 脚本
- `tests/`：hook 测试与基础 e2e 场景

## 安装

1. 复制 `SKILL.md` 到 `~/.claude/skills/harness/` 或 `<project>/.claude/skills/harness/`
2. 将当前目录下的 `hooks/` 复制到目标项目的 `.claude/hooks/`
3. 把 `settings.json` 中的 hooks 配置合并到目标项目的 `.claude/settings.json` 或 `.claude/settings.local.json`
4. 确认 `python3`、`git`、`bash` 可用

推荐结构：

```text
<project>/.claude/
├── hooks/
│   ├── _harness_common.py
│   ├── harness-claim.py
│   ├── harness-renew.py
│   ├── harness-sessionstart.py
│   ├── harness-stop.py
│   ├── harness-subagentstop.py
│   ├── harness-teammateidle.py
│   └── self-reflect-stop.py
├── settings.json
└── skills/
    └── harness/
        └── SKILL.md
```

## 依赖

- Claude Code project hooks
- `python3`
- `git`
- `bash`

## 使用方式

按 `SKILL.md` 里的协议直接使用：

- `/harness init <project-path>`
- `/harness add "task description"`
- `/harness status`
- `/harness run`

这个 pack 只提供协议和 hooks，不额外定义项目级命令封装。

## 运行产物

运行状态统一写入项目根目录下的 `.harness/`：

- `.harness/tasks.json`
- `.harness/progress.txt`
- `.harness/active`
- `.harness/reflect`
- `.harness/stop-counter`
- `.harness/init.sh`
- `.harness/tasks.json.bak`
- `.harness/tasks.json.tmp`

如果项目已经有 `.gitignore`，初始化后应把 `.harness/` 加进去。

## 说明

- `harness-claim.py` 和 `harness-renew.py` 是辅助脚本，不会自动注册成 Claude hooks
- `TeammateIdle` 和 `SubagentStop` 只在启用 teammate/subagent 时有意义，不用也不会出问题
- 如果项目里还有别的 `Stop` hooks，保持 harness 相关 hooks 连续放置，避免执行顺序被打乱


