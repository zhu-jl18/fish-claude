# rtk

外部工具参考页。

## 来源

- GitHub: `rtk-ai/rtk`
- URL: <https://github.com/rtk-ai/rtk>

## 简介

- 一个面向 coding CLI 的 token-optimized CLI proxy，核心做法是把高噪声 shell 输出压缩成更适合 LLM 消费的结果
- 常见用法是把 `git status`、`cargo test`、`pytest -q` 这类命令改成 `rtk <command>`

## 当前支持现状

- Claude Code：官方支持；默认目标就是 Claude Code，推荐用 `rtk init -g`，也可在项目目录运行 `rtk init`；不是 `rtk init --claude`
- Codex：官方支持；运行 `rtk init --codex` 后会写入 `RTK.md` 并把 `@RTK.md` 接入 `AGENTS.md`，本质是提示词注入，不是程序级 hook
- Oh My Pi：RTK 当前没有官方内建支持

## 本仓库里的 OMP 方案

- OMP 这边不是 RTK 官方集成
- 做法是仿照 Codex 的 prompt-level 引导思路，改用 OMP 原生 `rules` 机制注入 RTK 使用规则
- 规则参考文件放在 [`../config-files/oh-my-pi/rules/rtk.md`](../config-files/oh-my-pi/rules/rtk.md)
- 目标路径是 `~/.omp/agent/rules/rtk.md`

