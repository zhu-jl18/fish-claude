# Packs 指南

`packs/` 用来收纳两类内容：

- 可直接安装到 Claude Code 的组合包
- 与本仓库常搭配使用的外部工具参考页

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

如果某个 pack 目录包含 `SKILL.md`，还需要把它复制到 `.claude/skills/<pack-name>/`。

## 可用 Pack

| Pack | 说明 |
| --- | --- |
| [code-dispatcher-toolkit](code-dispatcher-toolkit.md) | 基于 `code-dispatcher` CLI 的多后端 AI 编码工具集，包含执行器、编排 skill、prompt 模板与安装脚本 |
| [rtk](rtk.md) | RTK 外部工具参考页；说明 Claude/Codex 官方接入方式，以及基于 OMP rules 的本地 OMP 适配 |
| [harness](harness/) | Claude Code 长运行会话 skill+hook 组合包，跨上下文窗口的任务持久化、失败恢复和进度追踪 |
| [codex-review-loop](codex-review-loop/) | Claude Code 专用 review loop bundle，Stop 时触发 Codex 多视角 review |
| [context-mode](context-mode.md) | Claude Code plugin + MCP server；sandbox 内处理大输出，~98% context 压缩，附 session continuity |
| [caveman](caveman.md) | Claude Code/Codex plugin；caveman-speak 削减 ~75% 输出 token，附 commit/review/compress 子命令 |
