#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path


CLI_MENU = {
    "1": ("claude", "Claude Code"),
    "2": ("codex", "Codex"),
    "3": ("gemini", "Gemini CLI"),
    "4": ("all", "全部"),
}

DAYS_MENU = {
    "1": 3,
    "2": 7,
    "3": 14,
    "4": 30,
    "5": None,
}


@dataclass
class JsonlPrunePlan:
    path: Path
    timestamp_keys: tuple[str, ...]
    unit: str
    preview_removed: int = 0
    preview_total: int = 0


@dataclass
class CliCleanupPlan:
    key: str
    label: str
    file_deletes: list[tuple[Path, Path]] = field(default_factory=list)
    jsonl_prunes: list[JsonlPrunePlan] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def print_header(text: str) -> None:
    print(f"\n=== {text} ===")


def prompt_cli_selection() -> list[str]:
    while True:
        print_header("选择要清理的 Agent CLI")
        print("1. Claude Code")
        print("2. Codex")
        print("3. Gemini CLI")
        print("4. 全部")
        print("0. 取消")
        raw = input("请输入编号（可多选，逗号分隔，如 1,3）: ").strip()

        if raw == "0":
            return []

        tokens = [x.strip() for x in raw.replace(" ", "").split(",") if x.strip()]
        if not tokens:
            continue

        if "4" in tokens:
            return ["claude", "codex", "gemini"]

        selected: list[str] = []
        ok = True
        for token in tokens:
            if token not in CLI_MENU or token == "4":
                ok = False
                break
            cli_key = CLI_MENU[token][0]
            if cli_key not in selected:
                selected.append(cli_key)
        if ok and selected:
            return selected
        print("输入无效，请重新输入。")


def prompt_days() -> int | None:
    while True:
        print_header("选择删除阈值（删除多少天以前的对话）")
        print("1. 3 天前")
        print("2. 7 天前")
        print("3. 14 天前")
        print("4. 30 天前")
        print("5. 自定义天数")
        print("0. 取消")
        choice = input("请输入编号: ").strip()

        if choice == "0":
            return None
        if choice in DAYS_MENU and DAYS_MENU[choice] is not None:
            return DAYS_MENU[choice]
        if choice == "5":
            custom = input("请输入正整数天数: ").strip()
            if custom.isdigit():
                value = int(custom)
                if value >= 1:
                    return value
        print("输入无效，请重新输入。")


def human_size(num_bytes: int) -> str:
    value = float(num_bytes)
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.2f} {unit}"
        value /= 1024
    raise RuntimeError("unreachable")


def collect_old_files(root: Path, cutoff_epoch_s: float, pattern: str = "*.jsonl") -> list[tuple[Path, Path]]:
    items: list[tuple[Path, Path]] = []
    if not root.exists():
        return items
    for file_path in root.rglob(pattern):
        if not file_path.is_file():
            continue
        try:
            if file_path.stat().st_mtime < cutoff_epoch_s:
                items.append((file_path, root))
        except OSError:
            continue
    items.sort(key=lambda x: str(x[0]).lower())
    return items


def collect_files_filtered(
    root: Path,
    include_file: Callable[[Path, Path], bool],
    cutoff_epoch_s: float | None,
) -> list[tuple[Path, Path]]:
    items: list[tuple[Path, Path]] = []
    if not root.exists():
        return items

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            if not include_file(file_path, root):
                continue
            if cutoff_epoch_s is not None and file_path.stat().st_mtime >= cutoff_epoch_s:
                continue
            items.append((file_path, root))
        except OSError:
            continue
    items.sort(key=lambda x: str(x[0]).lower())
    return items


def resolve_numeric_timestamp(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def is_old_jsonl_record(data: dict, timestamp_keys: tuple[str, ...], cutoff: float) -> bool:
    for key in timestamp_keys:
        if key not in data:
            continue
        ts = resolve_numeric_timestamp(data[key])
        if ts is None:
            continue
        return ts < cutoff
    return False


def preview_jsonl_prune(path: Path, timestamp_keys: tuple[str, ...], unit: str, cutoff_epoch_s: float) -> tuple[int, int]:
    if not path.exists():
        return (0, 0)

    cutoff = cutoff_epoch_s * 1000 if unit == "ms" else cutoff_epoch_s
    removed = 0
    total = 0

    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            total += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict) and is_old_jsonl_record(data, timestamp_keys, cutoff):
                removed += 1

    return (removed, total)


def apply_jsonl_prune(path: Path, timestamp_keys: tuple[str, ...], unit: str, cutoff_epoch_s: float) -> tuple[int, int]:
    if not path.exists():
        return (0, 0)

    cutoff = cutoff_epoch_s * 1000 if unit == "ms" else cutoff_epoch_s
    removed = 0
    total = 0

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as tmp:
        tmp_path = Path(tmp.name)
        with path.open("r", encoding="utf-8") as src:
            for raw in src:
                keep = True
                line = raw.strip()
                if not line:
                    tmp.write(raw if raw.endswith("\n") else f"{raw}\n")
                    continue
                total += 1
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    data = None

                if isinstance(data, dict) and is_old_jsonl_record(data, timestamp_keys, cutoff):
                    keep = False
                    removed += 1

                if keep:
                    tmp.write(raw if raw.endswith("\n") else f"{raw}\n")

    if removed > 0:
        tmp_path.replace(path)
    else:
        tmp_path.unlink(missing_ok=True)
    return (removed, total)


def cleanup_empty_parents(start: Path, stop_root: Path) -> None:
    current = start
    stop_root = stop_root.resolve()
    while True:
        try:
            current_resolved = current.resolve()
        except OSError:
            break
        if current_resolved == stop_root:
            break
        try:
            next(current.iterdir())
            break
        except StopIteration:
            current.rmdir()
            if current.parent == current:
                break
            current = current.parent
        except OSError:
            break


def collect_files_in_dir(root: Path, directory: Path) -> list[tuple[Path, Path]]:
    collected: list[tuple[Path, Path]] = []
    if not directory.exists():
        return collected
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            collected.append((file_path, root))
    return collected


def build_claude_plan(cutoff_epoch_s: float) -> CliCleanupPlan:
    home = Path.home()
    plan = CliCleanupPlan(key="claude", label="Claude Code")
    claude_root = home / ".claude"
    projects = claude_root / "projects"
    transcripts = claude_root / "transcripts"

    plan.file_deletes.extend(collect_old_files(projects, cutoff_epoch_s, "*.jsonl"))
    plan.file_deletes.extend(collect_old_files(transcripts, cutoff_epoch_s, "*.jsonl"))

    history_file = claude_root / "history.jsonl"
    prune = JsonlPrunePlan(path=history_file, timestamp_keys=("timestamp",), unit="ms")
    prune.preview_removed, prune.preview_total = preview_jsonl_prune(
        path=prune.path,
        timestamp_keys=prune.timestamp_keys,
        unit=prune.unit,
        cutoff_epoch_s=cutoff_epoch_s,
    )
    if prune.path.exists():
        plan.jsonl_prunes.append(prune)
    else:
        plan.notes.append(f"未找到历史文件: {prune.path}")

    plan.notes.append(f"检测目录: {projects}")
    plan.notes.append(f"检测目录: {transcripts}")
    return plan


def build_codex_plan(cutoff_epoch_s: float) -> CliCleanupPlan:
    home = Path.home()
    plan = CliCleanupPlan(key="codex", label="Codex")
    codex_root = home / ".codex"
    sessions = codex_root / "sessions"
    archived = codex_root / "archived_sessions"

    plan.file_deletes.extend(collect_old_files(sessions, cutoff_epoch_s, "*.jsonl"))
    plan.file_deletes.extend(collect_old_files(archived, cutoff_epoch_s, "*.jsonl"))

    history_file = codex_root / "history.jsonl"
    prune = JsonlPrunePlan(path=history_file, timestamp_keys=("ts",), unit="s")
    prune.preview_removed, prune.preview_total = preview_jsonl_prune(
        path=prune.path,
        timestamp_keys=prune.timestamp_keys,
        unit=prune.unit,
        cutoff_epoch_s=cutoff_epoch_s,
    )
    if prune.path.exists():
        plan.jsonl_prunes.append(prune)
    else:
        plan.notes.append(f"未找到历史文件: {prune.path}")

    plan.notes.append(f"检测目录: {sessions}")
    plan.notes.append(f"检测目录: {archived}")
    return plan


def build_gemini_plan(cutoff_epoch_s: float) -> CliCleanupPlan:
    plan = CliCleanupPlan(key="gemini", label="Gemini CLI")
    gemini_root = Path.home() / ".gemini"
    tmp_root = gemini_root / "tmp"
    history_root = gemini_root / "history"

    def include_tmp_file(file_path: Path, root: Path) -> bool:
        rel = file_path.relative_to(root)
        if not rel.parts:
            return False
        if rel.parts[0].lower() == "bin":
            return False
        if file_path.name == "seen_screen_reader_nudge.json":
            return False
        lower_parts = [part.lower() for part in rel.parts]
        if "chats" in lower_parts:
            return True
        if "checkpoints" in lower_parts:
            return True
        if file_path.name.lower() == "logs.json":
            return True
        return False

    def include_history_file(file_path: Path, _root: Path) -> bool:
        return file_path.name != ".project_root"

    plan.file_deletes.extend(collect_files_filtered(tmp_root, include_tmp_file, cutoff_epoch_s))
    plan.file_deletes.extend(collect_files_filtered(history_root, include_history_file, cutoff_epoch_s))

    plan.notes.append(f"检测目录: {tmp_root}")
    plan.notes.append(f"检测目录: {history_root}")
    return plan


def print_plan_summary(plans: list[CliCleanupPlan], cutoff: datetime) -> None:
    print_header("删除预览")
    print(f"截止时间（早于此时间会被删除）: {cutoff.astimezone().strftime('%Y-%m-%d %H:%M:%S %z')}")

    total_files = 0
    total_bytes = 0
    total_jsonl_removed = 0
    for plan in plans:
        print(f"\n[{plan.label}]")

        file_count = len(plan.file_deletes)
        file_size = 0
        for file_path, _root in plan.file_deletes:
            try:
                file_size += file_path.stat().st_size
            except OSError:
                continue
        total_files += file_count
        total_bytes += file_size

        if file_count:
            print(f"- 待删文件: {file_count} 个 ({human_size(file_size)})")
            preview = [str(x[0]) for x in plan.file_deletes[:5]]
            for item in preview:
                print(f"  {item}")
            if file_count > 5:
                print(f"  ... 其余 {file_count - 5} 个文件")
        else:
            print("- 待删文件: 0 个")

        if plan.jsonl_prunes:
            for prune in plan.jsonl_prunes:
                total_jsonl_removed += prune.preview_removed
                print(
                    f"- JSONL 剪裁: {prune.path} -> 预计删除 {prune.preview_removed}/{prune.preview_total} 行"
                )

        for note in plan.notes:
            print(f"- {note}")

    print("\n[总计]")
    print(f"- 待删文件: {total_files} 个 ({human_size(total_bytes)})")
    print(f"- 待删 JSONL 行: {total_jsonl_removed} 行")


def execute_plan(plans: list[CliCleanupPlan], cutoff_epoch_s: float) -> int:
    deleted_files = 0
    deleted_bytes = 0
    pruned_lines = 0
    failed_actions: list[str] = []

    for plan in plans:
        print(f"\n[执行] {plan.label}")

        file_total = len(plan.file_deletes)
        plan_deleted_files = 0
        if file_total > 0:
            print(f"- 文件删除任务: {file_total} 个")
        for file_path, root in plan.file_deletes:
            if not file_path.exists():
                continue
            try:
                size = file_path.stat().st_size
            except OSError:
                size = 0
            try:
                file_path.unlink()
                deleted_files += 1
                plan_deleted_files += 1
                deleted_bytes += size
                cleanup_empty_parents(file_path.parent, root)
            except OSError as e:
                failed_actions.append(f"删除文件失败: {file_path} ({e})")
            if file_total >= 50 and plan_deleted_files % 50 == 0:
                print(f"  已删除文件进度: {plan_deleted_files}/{file_total}")

        for prune in plan.jsonl_prunes:
            print(f"- 剪裁 JSONL: {prune.path}")
            try:
                removed, _total = apply_jsonl_prune(
                    path=prune.path,
                    timestamp_keys=prune.timestamp_keys,
                    unit=prune.unit,
                    cutoff_epoch_s=cutoff_epoch_s,
                )
                pruned_lines += removed
            except OSError as e:
                failed_actions.append(f"剪裁 JSONL 失败: {prune.path} ({e})")

    print_header("执行结果")
    print(f"- 已删除文件: {deleted_files} 个 ({human_size(deleted_bytes)})")
    print(f"- 已剪裁 JSONL 行: {pruned_lines} 行")

    if failed_actions:
        print(f"- 失败项: {len(failed_actions)}")
        for item in failed_actions[:10]:
            print(f"  {item}")
        if len(failed_actions) > 10:
            print(f"  ... 其余 {len(failed_actions) - 10} 个失败项")
        return 1

    print("- 所有操作完成。")
    return 0


def main() -> int:
    selected = prompt_cli_selection()
    if not selected:
        print("已取消。")
        return 0

    days = prompt_days()
    if days is None:
        print("已取消。")
        return 0

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    cutoff_epoch_s = cutoff.timestamp()

    builders = {
        "claude": build_claude_plan,
        "codex": build_codex_plan,
        "gemini": build_gemini_plan,
    }
    plans = [builders[key](cutoff_epoch_s) for key in selected]

    print_plan_summary(plans, cutoff)
    confirm = input("\n输入 DELETE 以确认删除，其他任意输入将取消: ").strip()
    if confirm != "DELETE":
        print("已取消。")
        return 0

    return execute_plan(plans, cutoff_epoch_s)


if __name__ == "__main__":
    sys.exit(main())
