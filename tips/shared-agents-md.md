# 一份 AGENTS.md 给所有 CLI 用

大部分 CLI 直接读仓库根目录的 `AGENTS.md`，只有 Claude Code 和 Gemini CLI 例外——它们读自己的文件，但可以通过 `@` 导入复用 `AGENTS.md`。

## 直接读 AGENTS.md

Codex、Warp、Oh My Pi 直接用 `AGENTS.md`，无需额外配置。

## 需要绕一下

**Claude Code** 读 `CLAUDE.md`：

```markdown
@AGENTS.md

# Claude Code 专属规则
```

**Gemini CLI** 读 `GEMINI.md`，同样支持 `@AGENTS.md`：

```markdown
@AGENTS.md

# Gemini CLI 专属规则
```

## 结论

仓库里维护一份 `AGENTS.md`，Claude Code 和 Gemini CLI 各写一个两三行的文件 `@AGENTS.md` 再追加自己的规则，Codex / Warp / OMP 直接读。所有 CLI 共享同一套项目规范。
