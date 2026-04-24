# code-dispatcher-toolkit

多后端 AI 编码工具集：CLI 调度器 + workflow skill + 安装脚本。

## 来源

- GitHub：<https://github.com/makoMakoGo/code-dispatcher-toolkit>

## 是什么

核心是一个 CLI 调度器 `code-dispatcher`，统一入口调度 `codex`、`claude`、`gemini` 三个后端：

接收任务 → 选后端 → 构建参数 → 分发执行 → 收集结果

- `--backend` 切换或并行调用多个后端
- `--parallel` 基于 DAG 调度同时跑独立任务
- `--resume` 上下文重置后继续未完成任务
- 统一配置 `~/.code-dispatcher/.env`

后端定位（推荐，可自由指定）：

- `codex`：复杂逻辑、bug 修复、重构
- `claude`：快速任务、review、补充分析
- `gemini`：前端 UI/UX 原型

> 核心思路基于 [`cexll/myclaude`](https://github.com/cexll/myclaude) 的 codeagent wrapper，经大量重构。

## Skills

| 名称 | 用途 |
|------|------|
| `dev` | 需求澄清 → 计划 → 并行执行 → 验证 |
| `code-council` | 2-3 个 AI reviewer 并行 + host 终审 |
| `pr-review-reply` | 自主处理 PR bot review，修复或反驳 |
| `code-dispatcher` | 执行器使用说明，`--parallel` / `--resume` 机制 |

## 安装

```bash
python3 install.py                    # 下载 CLI 二进制 + 生成配置
python3 install.py --skip-dispatcher  # 仅安装 skills
```

Skill 复制到对应 CLI 的 skills 目录（`~/.claude/skills/`、`~/.codex/skills/`、`~/.gemini/skills/` 等）即可。
