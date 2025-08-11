"""Basic automation script: daily folder backup & cleanup.

This script demonstrates a simple, pure-standard-library automation:

1. Compress (zip) a source directory into a timestamped archive under a backup directory.
2. Prune old backups beyond a retention window.
3. Optional (lightweight) daily scheduling loop when run with --watch.

Usage (one-off):
	python auto6.py --source ..\path\to\folder --backup ..\path\to\backups --retention-days 7

Usage (continuous daily at given hour, default 02:00):
	python auto6.py --source data --backup backups --watch --hour 2

All arguments have sensible defaults so you can also just run:
	python auto6.py

Assumptions:
	- Windows path defaults (relative to script directory) but works cross‑platform.
	- Retention applies to files following the naming pattern backup-YYYYMMDD-HHMMSS.zip

You can adapt the core `run_backup()` function for other automation tasks (e.g., exporting DB, calling APIs, etc.).
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class BackupConfig:
	source_dir: Path
	backup_dir: Path
	retention_days: int = 7
	hour: int = 2          # only used in watch mode
	minute: int = 0        # only used in watch mode

	def validate(self) -> None:
		if not self.source_dir.exists():
			raise FileNotFoundError(f"Source directory not found: {self.source_dir}")
		if not self.source_dir.is_dir():
			raise NotADirectoryError(f"Source path is not a directory: {self.source_dir}")
		self.backup_dir.mkdir(parents=True, exist_ok=True)
		if self.retention_days < 0:
			raise ValueError("retention_days must be >= 0")
		if not (0 <= self.hour < 24 and 0 <= self.minute < 60):
			raise ValueError("Hour must be 0-23 and minute 0-59")


def timestamp() -> str:
	return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def build_archive_name(backup_dir: Path) -> Path:
	return backup_dir / f"backup-{timestamp()}.zip"


def iter_files(base: Path) -> Iterable[Path]:
	for p in base.rglob("*"):
		if p.is_file():
			yield p


def create_zip(config: BackupConfig) -> Path:
	archive_path = build_archive_name(config.backup_dir)
	with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
		for file_path in iter_files(config.source_dir):
			rel = file_path.relative_to(config.source_dir)
			zf.write(file_path, arcname=rel.as_posix())
	return archive_path


def prune_old(config: BackupConfig) -> list[Path]:
	if config.retention_days == 0:
		return []  # no pruning
	cutoff = dt.datetime.now() - dt.timedelta(days=config.retention_days)
	deleted: list[Path] = []
	for f in sorted(config.backup_dir.glob("backup-*.zip")):
		# Parse timestamp segment: backup-YYYYMMDD-HHMMSS.zip
		try:
			stamp = f.stem.split("backup-")[-1]
			file_dt = dt.datetime.strptime(stamp, "%Y%m%d-%H%M%S")
		except Exception:
			# Skip unknown naming
			continue
		if file_dt < cutoff:
			try:
				f.unlink()
				deleted.append(f)
			except OSError:
				pass
	return deleted


def run_backup(config: BackupConfig) -> Path:
	config.validate()
	archive = create_zip(config)
	deleted = prune_old(config)
	print(f"Created: {archive}")
	if deleted:
		print(f"Pruned {len(deleted)} old backup(s).")
	return archive


def seconds_until(hour: int, minute: int = 0) -> int:
	now = dt.datetime.now()
	target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
	if target <= now:
		target += dt.timedelta(days=1)
	return int((target - now).total_seconds())


def watch_loop(config: BackupConfig) -> None:
	print(f"Entering watch mode: daily backup at {config.hour:02d}:{config.minute:02d} (Ctrl+C to stop)")
	while True:
		sleep_s = seconds_until(config.hour, config.minute)
		# Sleep in small chunks to allow graceful Ctrl+C
		while sleep_s > 0:
			chunk = min(300, sleep_s)
			time.sleep(chunk)
			sleep_s -= chunk
		try:
			run_backup(config)
		except Exception as e:  # log error, continue loop
			print(f"[ERROR] Backup failed: {e}")


def parse_args(argv: list[str]) -> BackupConfig:
	parser = argparse.ArgumentParser(description="Basic folder backup automation.")
	parser.add_argument("--source", type=Path, default=Path(__file__).parent.parent / "Message Encoder", help="Folder to back up (default: a sample folder).")
	parser.add_argument("--backup", type=Path, default=Path(__file__).parent / "_backups", help="Destination folder for backups.")
	parser.add_argument("--retention-days", type=int, default=7, help="Days to retain backups (default: 7). 0 = keep all.")
	parser.add_argument("--watch", action="store_true", help="Run continuously, performing backup daily at --hour:--minute.")
	parser.add_argument("--hour", type=int, default=2, help="Hour (0-23) to run when in --watch mode (default: 2).")
	parser.add_argument("--minute", type=int, default=0, help="Minute (0-59) to run when in --watch mode (default: 0).")
	args = parser.parse_args(argv)
	return BackupConfig(
		source_dir=args.source,
		backup_dir=args.backup,
		retention_days=args.retention_days,
		hour=args.hour,
		minute=args.minute,
	)


def main(argv: list[str] | None = None) -> int:
	config = parse_args(argv or sys.argv[1:])
	if any(flag in (argv or sys.argv[1:]) for flag in ("--watch",)):
		config.validate()
		try:
			watch_loop(config)
		except KeyboardInterrupt:
			print("Interrupted. Exiting.")
			return 130
		return 0
	try:
		run_backup(config)
		return 0
	except Exception as e:
		print(f"Failed: {e}")
		return 1


if __name__ == "__main__":  # pragma: no cover
	raise SystemExit(main())

