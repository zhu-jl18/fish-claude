# codex-review-loop

`codex-review-loop` 是给 Claude Code 用的 review loop pack。它让 Claude 先完成实现，再在 `Stop` 阶段触发 Codex 做独立 review；Claude 读取 review 结果后继续处理，直到没有新问题或你手动取消。

## 包含内容

- `commands/codex-review-loop.md`：启动 loop
- `commands/cancel-codex-review-loop.md`：取消 loop
- `hooks/codex-review-loop-stop.sh`：`Stop` hook 脚本
- `settings.json`：hook 配置片段

## 安装

将当前目录下的内容复制到目标项目的 `.claude/`：

```bash
cp -r commands/ <project>/.claude/commands/
cp -r hooks/ <project>/.claude/hooks/
chmod +x <project>/.claude/hooks/codex-review-loop-stop.sh
```

再把 `settings.json` 中的 `hooks.Stop` 合并到 `<project>/.claude/settings.json` 或 `<project>/.claude/settings.local.json`。

推荐结构：

```text
<project>/.claude/
├── commands/
│   ├── codex-review-loop.md
│   └── cancel-codex-review-loop.md
├── hooks/
│   └── codex-review-loop-stop.sh
└── settings.json
```

## 依赖

- `codex` CLI 在 PATH 中
- `~/.codex/config.toml` 开启：

```toml
[features]
multi_agent = true
```

这个 pack 不依赖 `code-dispatcher`。

## 使用方式

启动：

```text
/codex-review-loop Implement feature X with tests
```

取消：

```text
/cancel-codex-review-loop
```

## 运行产物

- 状态文件：`.claude/review-loop.local.md`
- review 文件：`reviews/review-<id>.md`
- 日志：`.claude/review-loop.log`

建议把 `reviews/` 加入 `.gitignore`，避免 review 产物混进提交。


