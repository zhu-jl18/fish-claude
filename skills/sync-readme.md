# Sync Readme

## 来源

- GitHub: `Li-ionFractalNanocore/cc-wrap`
- URL: <https://github.com/Li-ionFractalNanocore/cc-wrap/tree/main/.claude/skills/sync-readme>

## 简介

- 多语言 README 同步 skill：自动识别项目中最新版本的 README，将其翻译/同步到其他语言版本
- 工作流：Glob 查找所有 README → git log 对比最新版 → 翻译同步 → 输出报告
- 支持任意语言组合（README.md、README_CN.md、README_JA.md 等）
- 时间戳冲突时主动询问用户确认源文件
- 也适合配置说明驱动的仓库：当配置样例、安装命令或目录结构更新后，可用它同步 README / README.en.md 等多语言文档

## 安装

### Oh My Pi

将上游 `SKILL.md` 放到用户级 skills 目录：

```bash
mkdir -p ~/.omp/agent/skills/sync-readme
curl -o ~/.omp/agent/skills/sync-readme/SKILL.md \
  https://raw.githubusercontent.com/Li-ionFractalNanocore/cc-wrap/main/.claude/skills/sync-readme/SKILL.md
```

## 适用场景

- 多语言文档仓库，需要保持各语言 README 一致
- 更新主 README 后批量同步翻译版本
- 配置仓库中 `config-files/`、安装命令或目录结构变更后，同步各语言 README / 配置说明
