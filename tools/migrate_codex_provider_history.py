from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import tomllib
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConfigStatus:
    path: Path
    active_provider: str | None = None
    provider_keys: list[str] = field(default_factory=list)
    target_defined: bool = False
    sqlite_home: Path | None = None


@dataclass
class RolloutReport:
    files_scanned: int = 0
    files_needing_update: int = 0
    files_updated: int = 0
    session_meta_rewritten: int = 0
    provider_counts_before: Counter[str] = field(default_factory=Counter)
    provider_counts_after: Counter[str] = field(default_factory=Counter)


@dataclass
class SqliteReport:
    path: Path | None = None
    rows_needing_update: int = 0
    rows_updated: int = 0
    provider_counts_before: list[tuple[str | None, int]] = field(default_factory=list)
    provider_counts_after: list[tuple[str | None, int]] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='迁移 Codex chat history 的 model_provider，修复 provider key 变更后历史无法正确加载的问题。',
    )
    parser.add_argument(
        '--codex-home',
        type=Path,
        default=default_codex_home(),
        help='Codex 数据目录，默认读取 CODEX_HOME 或 ~/.codex',
    )
    parser.add_argument(
        '--target-provider',
        default='custom',
        help='迁移后的目标 provider key，默认 custom',
    )
    parser.add_argument(
        '--keep-provider',
        action='append',
        default=None,
        help='保留不迁移的 provider key，可重复传入；默认保留 openai 和目标 provider',
    )
    parser.add_argument(
        '--state-db',
        type=Path,
        default=None,
        help='显式指定 state_*.sqlite 路径；默认自动发现',
    )
    parser.add_argument(
        '--backup-dir',
        type=Path,
        default=None,
        help='执行写入时，将变更前文件备份到该目录',
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='执行真实写入；默认仅预览',
    )
    return parser.parse_args()


def default_codex_home() -> Path:
    env_value = os.environ.get('CODEX_HOME')
    if env_value:
        return Path(env_value).expanduser()
    return Path.home() / '.codex'


def inspect_config(config_path: Path, target_provider: str) -> ConfigStatus:
    status = ConfigStatus(path=config_path)
    if not config_path.exists():
        return status
    data = tomllib.loads(config_path.read_text(encoding='utf-8'))
    active_provider = data.get('model_provider')
    if isinstance(active_provider, str) and active_provider.strip():
        status.active_provider = active_provider
    providers = data.get('model_providers')
    if isinstance(providers, dict):
        status.provider_keys = sorted(str(key) for key in providers.keys())
        status.target_defined = target_provider in providers
    sqlite_home = data.get('sqlite_home')
    if isinstance(sqlite_home, str) and sqlite_home.strip():
        status.sqlite_home = Path(sqlite_home).expanduser()
    return status


def resolve_sqlite_home_env() -> Path | None:
    raw = os.environ.get('CODEX_SQLITE_HOME')
    if raw is None:
        return None
    trimmed = raw.strip()
    if not trimmed:
        return None
    path = Path(trimmed).expanduser()
    if path.is_absolute():
        return path
    return Path.cwd() / path


def iter_state_db_candidates(sqlite_home: Path) -> list[tuple[int, float, Path]]:
    version_pattern = re.compile(r'^state_(\d+)\.sqlite$')
    candidates: list[tuple[int, float, Path]] = []
    if not sqlite_home.exists():
        return candidates
    for path in sqlite_home.glob('state_*.sqlite'):
        match = version_pattern.match(path.name)
        if not match:
            continue
        candidates.append((int(match.group(1)), path.stat().st_mtime, path))
    return candidates


def resolve_state_db(codex_home: Path, config_status: ConfigStatus, explicit_path: Path | None) -> Path | None:
    if explicit_path is not None:
        return explicit_path
    search_roots: list[Path] = []
    for root in (config_status.sqlite_home, resolve_sqlite_home_env(), codex_home):
        if root is None:
            continue
        if any(existing == root for existing in search_roots):
            continue
        search_roots.append(root)
    for root in search_roots:
        candidates = iter_state_db_candidates(root)
        if not candidates:
            continue
        candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return candidates[0][2]
    return None


def iter_rollout_files(codex_home: Path) -> list[Path]:
    files: list[Path] = []
    for relative_dir in ('sessions', 'archived_sessions'):
        root = codex_home / relative_dir
        if not root.exists():
            continue
        files.extend(sorted(root.rglob('*.jsonl')))
    return files


def ensure_backup_root(backup_root: Path | None) -> Path | None:
    if backup_root is None:
        return None
    backup_root.mkdir(parents=True, exist_ok=True)
    return backup_root


def backup_file(src: Path, codex_home: Path, backup_root: Path | None) -> None:
    if backup_root is None:
        return
    relative_path = src.relative_to(codex_home)
    destination = backup_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copy2(src, destination)


def rewrite_rollout_file(
    path: Path,
    codex_home: Path,
    target_provider: str,
    keep_providers: set[str],
    apply: bool,
    backup_root: Path | None,
    report: RolloutReport,
) -> None:
    original_text = path.read_text(encoding='utf-8')
    newline_at_end = original_text.endswith('\n')
    original_lines = original_text.splitlines()
    rewritten_lines: list[str] = []
    file_changed = False

    for line_number, line in enumerate(original_lines, start=1):
        if not line.strip():
            rewritten_lines.append(line)
            continue

        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'无法解析 JSONL: {path}:{line_number}: {exc}') from exc

        if isinstance(payload, dict) and payload.get('type') == 'session_meta':
            session_meta = payload.get('payload')
            if not isinstance(session_meta, dict):
                raise ValueError(f'session_meta payload 非对象: {path}:{line_number}')
            provider_value = session_meta.get('model_provider')
            provider_key = provider_value if isinstance(provider_value, str) and provider_value else '<missing>'
            report.provider_counts_before[provider_key] += 1
            simulated_provider = provider_key
            if isinstance(provider_value, str) and provider_value not in keep_providers:
                session_meta['model_provider'] = target_provider
                payload['payload'] = session_meta
                report.session_meta_rewritten += 1
                simulated_provider = target_provider
                file_changed = True
            report.provider_counts_after[simulated_provider] += 1
            line = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))

        rewritten_lines.append(line)

    report.files_scanned += 1
    if not file_changed:
        return

    report.files_needing_update += 1
    if not apply:
        return

    backup_file(path, codex_home, backup_root)
    rewritten_text = '\n'.join(rewritten_lines)
    if newline_at_end:
        rewritten_text += '\n'
    path.write_text(rewritten_text, encoding='utf-8')
    report.files_updated += 1


def migrate_rollouts(
    codex_home: Path,
    target_provider: str,
    keep_providers: set[str],
    apply: bool,
    backup_root: Path | None,
) -> RolloutReport:
    report = RolloutReport()
    for path in iter_rollout_files(codex_home):
        rewrite_rollout_file(
            path=path,
            codex_home=codex_home,
            target_provider=target_provider,
            keep_providers=keep_providers,
            apply=apply,
            backup_root=backup_root,
            report=report,
        )
    return report


def backup_sqlite_bundle(db_path: Path, backup_root: Path | None) -> None:
    if backup_root is None:
        return
    sqlite_root = backup_root / 'sqlite'
    sqlite_root.mkdir(parents=True, exist_ok=True)
    for suffix in ('', '-wal', '-shm'):
        current_path = Path(str(db_path) + suffix)
        if current_path.exists():
            destination = sqlite_root / current_path.name
            if not destination.exists():
                shutil.copy2(current_path, destination)


def fetch_sqlite_provider_counts(conn: sqlite3.Connection) -> list[tuple[str | None, int]]:
    rows = conn.execute(
        'SELECT model_provider, COUNT(*) FROM threads GROUP BY model_provider ORDER BY COUNT(*) DESC, model_provider ASC'
    ).fetchall()
    result: list[tuple[str | None, int]] = []
    for provider_value, count in rows:
        provider_key = provider_value if isinstance(provider_value, str) or provider_value is None else str(provider_value)
        result.append((provider_key, int(count)))
    return result


def simulate_sqlite_counts(
    provider_counts_before: list[tuple[str | None, int]],
    target_provider: str,
    keep_providers: set[str],
) -> list[tuple[str | None, int]]:
    counter: Counter[str | None] = Counter()
    for provider_key, count in provider_counts_before:
        if provider_key is None:
            final_provider = None
        elif provider_key in keep_providers:
            final_provider = provider_key
        else:
            final_provider = target_provider
        counter[final_provider] += count
    return sorted(counter.items(), key=lambda item: (-item[1], '' if item[0] is None else item[0]))


def migrate_sqlite(
    db_path: Path | None,
    target_provider: str,
    keep_providers: set[str],
    apply: bool,
    backup_root: Path | None,
) -> SqliteReport:
    report = SqliteReport(path=db_path)
    if db_path is None or not db_path.exists():
        return report

    connection = sqlite3.connect(db_path)
    try:
        report.provider_counts_before = fetch_sqlite_provider_counts(connection)
        filter_placeholders = ', '.join('?' for _ in keep_providers)
        filter_sql = f'model_provider IS NOT NULL AND model_provider NOT IN ({filter_placeholders})'
        filter_params = tuple(sorted(keep_providers))
        report.rows_needing_update = int(
            connection.execute(f'SELECT COUNT(*) FROM threads WHERE {filter_sql}', filter_params).fetchone()[0]
        )

        if apply and report.rows_needing_update > 0:
            backup_sqlite_bundle(db_path, backup_root)
            connection.execute('BEGIN IMMEDIATE')
            connection.execute(
                f'UPDATE threads SET model_provider = ? WHERE {filter_sql}',
                (target_provider, *filter_params),
            )
            report.rows_updated = connection.total_changes
            connection.commit()
            connection.execute('PRAGMA wal_checkpoint(TRUNCATE)')

        report.provider_counts_after = (
            fetch_sqlite_provider_counts(connection)
            if apply
            else simulate_sqlite_counts(report.provider_counts_before, target_provider, keep_providers)
        )
    finally:
        connection.close()

    return report


def format_counts(counts: Counter[str] | list[tuple[str | None, int]]) -> list[str]:
    merged: Counter[str] = Counter()
    if isinstance(counts, Counter):
        for provider, count in counts.items():
            label = provider if provider else '<missing>'
            merged[label] += count
    else:
        for provider, count in counts:
            label = provider if isinstance(provider, str) and provider else '<missing>'
            merged[label] += count
    items = sorted(merged.items(), key=lambda item: (-item[1], item[0]))
    if not items:
        return ['- 无']
    return [f'- {provider}: {count}' for provider, count in items]


def print_summary(
    apply: bool,
    codex_home: Path,
    target_provider: str,
    keep_providers: set[str],
    backup_root: Path | None,
    config_status: ConfigStatus,
    rollout_report: RolloutReport,
    sqlite_report: SqliteReport,
) -> None:
    mode = '执行写入' if apply else '预览'
    print(f'模式: {mode}')
    print(f'Codex Home: {codex_home}')
    print(f'目标 provider: {target_provider}')
    print(f'保留 provider: {", ".join(sorted(keep_providers))}')
    if backup_root is not None:
        print(f'备份目录: {backup_root}')

    print('\n配置检查')
    print(f'- config.toml: {config_status.path}')
    print(f'- 当前 model_provider: {config_status.active_provider or "<missing>"}')
    print(f'- 目标 provider 已定义: {"yes" if config_status.target_defined else "no"}')
    if config_status.provider_keys:
        print(f'- 已定义 providers: {", ".join(config_status.provider_keys)}')
    if config_status.active_provider != target_provider:
        print('- 警告: config.toml 的 model_provider 与目标 provider 不一致；仅迁移历史不会自动修正配置。')
    if not config_status.target_defined:
        print('- 提示: config.toml 中未在 model_providers 下定义目标 provider；如果目标是内建 provider，这可能是正常现象，否则 Codex 仍可能无法按目标 bucket 加载历史。')

    print('\nrollout 扫描')
    print(f'- 扫描文件数: {rollout_report.files_scanned}')
    print(f'- 需要迁移文件数: {rollout_report.files_needing_update}')
    print(f'- 已改写文件数: {rollout_report.files_updated}')
    print(f'- 改写 session_meta 数: {rollout_report.session_meta_rewritten}')
    print('- 迁移前 provider 分布:')
    for line in format_counts(rollout_report.provider_counts_before):
        print(f'  {line}')
    print('- 迁移后 provider 分布:')
    for line in format_counts(rollout_report.provider_counts_after):
        print(f'  {line}')

    print('\nSQLite 索引')
    print(f'- state db: {sqlite_report.path or "<not found>"}')
    print(f'- 需要更新行数: {sqlite_report.rows_needing_update}')
    print(f'- 已更新行数: {sqlite_report.rows_updated}')
    print('- 迁移前 provider 分布:')
    for line in format_counts(sqlite_report.provider_counts_before):
        print(f'  {line}')
    print('- 迁移后 provider 分布:')
    for line in format_counts(sqlite_report.provider_counts_after):
        print(f'  {line}')

    if not apply:
        print('\n当前为预览模式；追加 --apply 才会真正写入。')


def main() -> int:
    args = parse_args()
    codex_home = args.codex_home.expanduser().resolve()
    backup_root = ensure_backup_root(args.backup_dir.expanduser().resolve() if args.backup_dir else None)
    keep_providers = set(args.keep_provider or ['openai'])
    keep_providers.add(args.target_provider)

    config_status = inspect_config(codex_home / 'config.toml', args.target_provider)
    rollout_report = migrate_rollouts(
        codex_home=codex_home,
        target_provider=args.target_provider,
        keep_providers=keep_providers,
        apply=args.apply,
        backup_root=backup_root,
    )
    sqlite_report = migrate_sqlite(
        db_path=resolve_state_db(
            codex_home,
            config_status,
            args.state_db.expanduser().resolve() if args.state_db else None,
        ),
        target_provider=args.target_provider,
        keep_providers=keep_providers,
        apply=args.apply,
        backup_root=backup_root,
    )
    print_summary(
        apply=args.apply,
        codex_home=codex_home,
        target_provider=args.target_provider,
        keep_providers=keep_providers,
        backup_root=backup_root,
        config_status=config_status,
        rollout_report=rollout_report,
        sqlite_report=sqlite_report,
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
