# Sync Readme

社区 skill 占位页，后续可继续补安装方式、常用工作流和适用边界。

## 来源

- GitHub: `Li-ionFractalNanocore/cc-wrap`
- 地址: <https://github.com/Li-ionFractalNanocore/cc-wrap/tree/main/.claude/skills/sync-readme>

## 简介

- 多语言 README 同步 skill：自动识别项目中最新版本的 README，将其翻译/同步到其他语言版本
- 工作流：Glob 查找所有 README → git log 对比最新版 → 翻译同步 → 输出报告
- 支持任意语言组合（README.md、README_CN.md、README_JA.md 等）
- 时间戳冲突时主动询问用户确认源文件

## 安装

将上游仓库的 `SKILL.md` 复制到项目的 `.claude/skills/sync-readme/SKILL.md`：

```bash
mkdir -p .claude/skills/sync-readme
curl -o .claude/skills/sync-readme/SKILL.md \
  https://raw.githubusercontent.com/Li-ionFractalNanocore/cc-wrap/main/.claude/skills/sync-readme/SKILL.md
```

## 适用场景

- 多语言文档仓库，需要保持各语言 README 一致
- 更新主 README 后批量同步翻译版本

## 待补

- 常用命令与工作流
- 适合场景与不适合场景
