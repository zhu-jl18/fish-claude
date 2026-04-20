# caveman

外部工具参考页。

## 来源

- GitHub: `JuliusBrussee/caveman`
- URL: <https://github.com/JuliusBrussee/caveman>

## 为什么选它

- 个人偏好 `full` 预设的碎片句 + 短词替换风格，读着顺
- 省 token 是附加作用，不是选它的第一理由

## 具体原理

本质是 prompt injection —— 不改模型权重，也不拦截输出，纯靠把规则写进 system context 让模型自己约束。

- **Claude Code / Codex**
  - `SessionStart` hook 读 `$CLAUDE_CONFIG_DIR/.caveman-active` 确定当前 mode，读 `skills/caveman/SKILL.md` 过滤到该 mode，把规则作为 hidden stdout 写入 —— Claude Code / Codex 把 SessionStart hook 的 stdout 注入为 system context
  - `UserPromptSubmit` hook 每轮额外下发一个 `additionalContext` 提醒，防止对话中途被其他插件或 context 压缩把 SessionStart 注入的规则盖掉
  - `~/.caveman-active` 这个 flag 文件同时给 statusline 脚本读，渲染 `[CAVEMAN:MODE]` 角标
- **Gemini CLI**：`GEMINI.md` context 文件，每次启动自动加载
- **Cursor / Windsurf / Cline / Copilot**：原生 rule 文件（`alwaysApply: true` / `trigger: always_on`），IDE 层自动注入每轮 prompt
- **无 hook / rule 机制的 agent**：`npx skills add` 本地下发 skill 文件，用户每次会话手动 `/caveman` 触发

## 与本仓库的关系

- 与 `output-styles/` 不同：`output-styles/` 是 Claude Code 原生机制，替换 Claude Code 默认 system prompt，仅限 Claude Code；caveman 是 hook 注入附加规则，跨 agent 通用
- 细节见 caveman 仓库 README
