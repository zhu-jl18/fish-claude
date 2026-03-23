#!/usr/bin/env python3
"""Self-reflection Stop hook — harness 任务循环完成后注入自省 prompt。

仅在以下条件同时满足时生效：
  1. .harness/tasks.json 存在（harness 曾被初始化）
  2. .harness/active 不存在（harness 任务已全部完成）

当 harness 未曾启动时，本 hook 是完全的 no-op。

配置:
  - REFLECT_MAX_ITERATIONS 环境变量（默认 3）
  - 设为 0 可禁用
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

# Add hooks directory to sys.path for _harness_common import
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import _harness_common as hc
except ImportError:
    hc = None  # type: ignore[assignment]

DEFAULT_MAX_ITERATIONS = 3


def _read_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _find_harness_root(payload: dict[str, Any]) -> Optional[Path]:
    """查找 .harness/tasks.json 所在的目录。存在则说明 harness 曾被使用。"""
    if hc is not None:
        return hc.find_harness_root(payload)

    # Fallback: inline discovery if _harness_common not available
    candidates: list[Path] = []
    state_root = os.environ.get("HARNESS_STATE_ROOT")
    if state_root:
        p = Path(state_root)
        if (p / ".harness/tasks.json").is_file():
            try:
                return p.resolve()
            except Exception:
                return p
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        candidates.append(Path(env_dir))
    cwd = payload.get("cwd") or os.getcwd()
    candidates.append(Path(cwd))
    seen: set[str] = set()
    for base in candidates:
        try:
            base = base.resolve()
        except Exception:
            continue
        if str(base) in seen:
            continue
        seen.add(str(base))
        for parent in [base, *list(base.parents)[:8]]:
            if (parent / ".harness/tasks.json").is_file():
                return parent
    return None


def _counter_path(session_id: str) -> Path:
    """每个 session 独立计数文件。"""
    return Path(tempfile.gettempdir()) / f"claude-reflect-{session_id}"


def _read_counter(session_id: str) -> int:
    p = _counter_path(session_id)
    try:
        return int(p.read_text("utf-8").strip().split("\n")[0])
    except Exception:
        return 0


def _write_counter(session_id: str, count: int) -> None:
    p = _counter_path(session_id)
    try:
        p.write_text(str(count), encoding="utf-8")
    except Exception:
        pass


def _extract_original_prompt(transcript_path: str, max_bytes: int = 100_000) -> str:
    """从 transcript JSONL 中提取第一条用户消息作为原始 prompt。"""
    try:
        p = Path(transcript_path)
        if not p.is_file():
            return ""
        with p.open("r", encoding="utf-8") as f:
            # JSONL 格式，逐行解析找第一条 user message
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                if not isinstance(entry, dict):
                    continue
                # Claude Code transcript 格式：role + content
                role = entry.get("role") or entry.get("type", "")
                if role == "user":
                    content = entry.get("content", "")
                    if isinstance(content, list):
                        # content 可能是 list of blocks
                        texts = []
                        for block in content:
                            if isinstance(block, dict):
                                t = block.get("text", "")
                                if t:
                                    texts.append(t)
                            elif isinstance(block, str):
                                texts.append(block)
                        content = "\n".join(texts)
                    if isinstance(content, str) and content.strip():
                        # 截断过长的 prompt
                        if len(content) > 2000:
                            content = content[:2000] + "..."
                        return content.strip()
    except Exception:
        pass
    return ""


def main() -> int:
    payload = _read_payload()
    session_id = payload.get("session_id", "")
    if not session_id:
        return 0  # 无 session_id，放行

    # 守卫：仅当 harness 完成所有任务后（.harness/reflect 存在）才触发自省
    # 这避免了两个问题：
    #   1. 历史残留的 .harness/tasks.json 导致误触发（false positive）
    #   2. harness-stop.py 移除 .harness/active 后 Claude Code 跳过后续 hook（false negative）
    root = _find_harness_root(payload)
    if root is None:
        return 0

    if not (root / ".harness/reflect").is_file():
        return 0

    # 读取最大迭代次数
    try:
        max_iter = int(os.environ.get("REFLECT_MAX_ITERATIONS", DEFAULT_MAX_ITERATIONS))
    except (ValueError, TypeError):
        max_iter = DEFAULT_MAX_ITERATIONS

    # 禁用
    if max_iter <= 0:
        return 0

    # 读取当前计数
    count = _read_counter(session_id)

    # 超过最大次数，清理 marker 并放行
    if count >= max_iter:
        try:
            (root / ".harness/reflect").unlink(missing_ok=True)
        except Exception:
            pass
        return 0

    # 递增计数
    _write_counter(session_id, count + 1)

    # 提取原始 prompt
    transcript_path = payload.get("transcript_path", "")
    original_prompt = _extract_original_prompt(transcript_path)
    last_message = payload.get("last_assistant_message", "")
    if last_message and len(last_message) > 3000:
        last_message = last_message[:3000] + "..."

    # 构建自省 prompt
    parts = [
        f"[Self-Reflect] 迭代 {count + 1}/{max_iter} — 请在继续之前进行自省检查：",
    ]

    if original_prompt:
        parts.append(f"\n📋 原始请求：\n{original_prompt}")

    parts.append(
        "\n🔍 自省清单："
        "\n1. 对照原始请求，逐项确认每个需求点是否已完整实现"
        "\n2. 检查是否有遗漏的边界情况、错误处理或异常场景"
        "\n3. 代码质量：是否有可以改进的地方（可读性、性能、安全性）"
        "\n4. 是否需要补充测试或文档"
        "\n5. 最终确认：所有改动是否一致且不互相冲突"
        "\n\n如果一切已完成，简要总结成果即可结束。如果发现问题，继续修复。"
    )

    reason = "\n".join(parts)

    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
