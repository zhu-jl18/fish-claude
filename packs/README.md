# Packs 指南

Pack 是一组协同工作的组件组合包，可能包含 commands、skills、hooks、subagents、config 片段等，也可以是外部工具集的参考页。

## Pack 典型结构

```text
<pack-name>/
├── README.md           # 安装说明与概览
├── SKILL.md            # 协议/skill 定义（可选）
├── settings.json       # Claude Code hook 配置片段（可选）
├── hooks/              # 生命周期 hook 脚本（可选）
├── commands/           # slash command 模板（可选）
└── tests/              # 测试文件（可选）
```

## 安装模式

```bash
cp -r <pack>/commands/  <project>/.claude/commands/
cp -r <pack>/hooks/     <project>/.claude/hooks/
# 将 <pack>/settings.json 合并到 <project>/.claude/settings.json
```

## 可用 Pack

| Pack | 说明 |
| --- | --- |
| [code-dispatcher-toolkit](code-dispatcher-toolkit.md) | 基于 `code-dispatcher` CLI 的多后端 AI 编码工具集，包含执行器、编排 skill、prompt 模板与安装脚本 |
| [harness](harness.md) | Claude Code 长运行会话 skill+hook 组合包，跨上下文窗口的任务持久化、失败恢复和进度追踪 |
