# AI Coding Discipline

## 来源

- GitHub: `luoling8192/ai-coding-principles`
- URL: <https://github.com/luoling8192/ai-coding-principles/tree/main/ai-coding-discipline>

## 简介

- 一组面向 AI coding agent 的强约束编码纪律，目标是压制常见的 AI 编码反模式
- 核心规则包括：禁止静默 fallback、禁止业务逻辑 catch-all、测试必须验证具体业务结果、禁止硬编码查表式假实现、修 bug 先红后绿、修复时不删调试日志
- 适合在写代码、改代码、修 bug、补测试、review 代码时作为默认 skill 常驻

## 安装

### Oh My Pi

将上游 `SKILL.md` 放到用户级 skills 目录：

```bash
mkdir -p ~/.omp/agent/skills/ai-coding-discipline
curl -o ~/.omp/agent/skills/ai-coding-discipline/SKILL.md \
  https://raw.githubusercontent.com/luoling8192/ai-coding-principles/main/ai-coding-discipline/SKILL.md
```

## 适用场景

- 代码编写 / 重构 / 修 bug
- 测试编写与补强
- review AI 生成代码时防止常见糊弄式实现
