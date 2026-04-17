# Karpathy Guidelines

## 来源

- GitHub: `forrestchang/andrej-karpathy-skills`
- URL: <https://github.com/forrestchang/andrej-karpathy-skills/tree/main/skills/karpathy-guidelines>

## 简介

- 基于 Andrej Karpathy 对 LLM coding pitfalls 的观察整理出来的行为约束 skill
- 核心原则是先澄清假设、优先简单方案、只做手术式变更、把任务改写成可验证目标
- 适合在写代码、review、重构和排查 AI 过度设计问题时作为通用行为层叠加到 Codex / Claude Code

## 安装

### Codex CLI

将上游 `SKILL.md` 放到用户级 skills 目录：

```bash
mkdir -p ~/.codex/skills/karpathy-guidelines
curl -o ~/.codex/skills/karpathy-guidelines/SKILL.md \
  https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/skills/karpathy-guidelines/SKILL.md
```

### Claude Code

通过插件市场安装：

```text
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

## 适用场景

- 需求有歧义，想强制 agent 先暴露假设与 tradeoff
- AI 容易过度设计、乱加抽象、顺手改无关代码
- 希望把“修 bug / 加校验 / 重构”改写成带验证条件的目标驱动执行
