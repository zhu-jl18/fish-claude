# Themes

## Warp

### 主题目录

| OS | 路径 |
|----|------|
| macOS | `~/.warp/themes/` |
| Linux | `${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal/themes/` |
| Windows | `%APPDATA%\warp\Warp\data\themes\` |

### 社区主题仓库

- [warpdotdev/themes](https://github.com/warpdotdev/themes) — 官方社区主题。标准主题（Dracula、Nord、Solarized、Catppuccin 等）+ 特别版（Barbie、Lumon、Oppenheimer、Pride、Asteroid City、Winter、Thanksgiving、Grafbase）+ base16 系列
- [SilentGlasses/warp_themes](https://github.com/SilentGlasses/warp_themes) — 39 个第三方主题，部分带背景图（Ame-Nami、Neural Nebula、Ukiyo、Kali Blue 等）

克隆后放对应目录，重启 Warp 即可在 Settings → Appearance 中选择。

## Claude Code

### 主题目录

| Scope | 路径 |
|-------|------|
| User | `~/.claude/themes/` |
| Plugin | `<plugin>/themes/` |

### 使用方式

- `/theme` 命令创建/切换主题
- 手动编辑 `~/.claude/themes/*.json`
- 插件可通过 `themes/` 目录分发
