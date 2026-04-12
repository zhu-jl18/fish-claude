# Software Design Philosophy

## 来源

- GitHub: `luoling8192/software-design-philosophy-skill`
- URL: <https://github.com/luoling8192/software-design-philosophy-skill>

## 简介

- 基于 John Ousterhout《A Philosophy of Software Design》的设计哲学 skill
- 核心关注点是复杂度管理：deep module、信息隐藏、减少 information leakage、把复杂度往下压、让常见路径更简单
- 适合在架构讨论、API 设计、模块拆分、重构、命名与注释评审时作为设计视角补充

## 安装

### Oh My Pi

将上游 `SKILL.md` 放到用户级 skills 目录：

```bash
mkdir -p ~/.omp/agent/skills/software-design-philosophy
curl -o ~/.omp/agent/skills/software-design-philosophy/SKILL.md \
  https://raw.githubusercontent.com/luoling8192/software-design-philosophy-skill/main/SKILL.md
```

## 适用场景

- 代码评审时检查复杂度、信息泄漏、接口深浅
- 模块拆分、API 设计、重构取舍
- 命名、注释、错误处理策略的设计讨论

## 待补

- Claude Code / Codex / Gemini CLI 的安装写法
- 常用工作流
- 不适合场景
