"""Simple Backup & Cleanup Automation

Purpose:
	Automate backing up selected source folders into a dated backup directory
	while cleaning up old backups. Safe by default (dry-run) unless --apply
	flag is provided.

Features:
	- JSON config file (auto5_config.json) specifying sources & settings
	- Creates dated backup folder (YYYY-MM-DD)
	- Copies only new / changed files (hash + size/mtime heuristic)
	- Maintains manifest.json with file metadata & last backup date
	- Cleans backups older than max_age_days
	- Dry-run mode (default) prints planned actions without changing disk
	- Optional --since DAYS to override default max_age_days retention check
	- Verbose logging option

Usage (from this script directory):
	python auto5.py --init-config          # create default config then exit
	python auto5.py                        # show what would happen (dry-run)
	python auto5.py --apply                # perform backup & cleanup
	python auto5.py --apply --verbose      # with extra logs
	python auto5.py --apply --since 10     # treat anything older than 10 days as expired

Config file example (auto5_config.json):
{
  "sources": ["../Emoji translator", "../Sudoko solver"],
  "backup_dir": "../../backups",
  "max_age_days": 30,
  "hash_method": "md5",
  "exclude_patterns": ["__pycache__", ".git", ".DS_Store"]
}

You can edit the config after initialization. Relative paths are resolved
relative to this script's directory.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import logging
import os
from pathlib import Path
import shutil
import sys
from typing import Dict, List, Optional, Set


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_NAME = "auto5_config.json"


def log_setup(verbose: bool) -> None:
	level = logging.DEBUG if verbose else logging.INFO
	logging.basicConfig(
		level=level,
		format="[%(levelname)s] %(message)s",
		handlers=[logging.StreamHandler(sys.stdout)],
	)


def load_config(path: Path) -> dict:
	if not path.exists():
		raise FileNotFoundError(
			f"Config file '{path}' not found. Run with --init-config to create one."
		)
	with path.open("r", encoding="utf-8") as f:
		data = json.load(f)
	# Basic validation & defaults
	data.setdefault("sources", [])
	data.setdefault("backup_dir", str(SCRIPT_DIR.parent / "backups"))
	data.setdefault("max_age_days", 30)
	data.setdefault("hash_method", "md5")
	data.setdefault("exclude_patterns", ["__pycache__", ".git", ".DS_Store"])
	return data


def init_config(path: Path) -> None:
	if path.exists():
		logging.info("Config already exists at %s", path)
		return
	# Try to auto-suggest interesting source folders (siblings inside python directory)
	python_dir = SCRIPT_DIR.parent.parent / "python"
	suggestions: List[str] = []
	if python_dir.exists():
		for p in python_dir.iterdir():
			if p.is_dir() and p.name not in {"Automations"}:
				suggestions.append(str(p.relative_to(SCRIPT_DIR)))
			if len(suggestions) >= 5:
				break
	config = {
		"sources": suggestions or [".."],
		"backup_dir": str((SCRIPT_DIR / "../../backups").resolve()),
		"max_age_days": 30,
		"hash_method": "md5",
		"exclude_patterns": ["__pycache__", ".git", ".DS_Store"],
	}
	with path.open("w", encoding="utf-8") as f:
		json.dump(config, f, indent=2)
	logging.info("Created default config at %s", path)
	logging.info("Edit the file to customize sources before running backups.")


def compute_hash(file_path: Path, method: str = "md5", chunk_size: int = 65536) -> str:
	h = hashlib.new(method)
	with file_path.open("rb") as f:
		while True:
			chunk = f.read(chunk_size)
			if not chunk:
				break
			h.update(chunk)
	return h.hexdigest()


def load_manifest(backup_dir: Path) -> dict:
	manifest_file = backup_dir / "manifest.json"
	if manifest_file.exists():
		try:
			with manifest_file.open("r", encoding="utf-8") as f:
				return json.load(f)
		except Exception as e:  # noqa: BLE001
			logging.warning("Failed to load manifest (%s). Starting new.", e)
	return {"files": {}}  # structure: {"files": {rel_path: {hash, size, mtime, last_backup}}}


def save_manifest(backup_dir: Path, manifest: dict, dry_run: bool) -> None:
	if dry_run:
		logging.debug("Dry-run: skipping manifest save (%d entries)", len(manifest.get("files", {})))
		return
	manifest_file = backup_dir / "manifest.json"
	with manifest_file.open("w", encoding="utf-8") as f:
		json.dump(manifest, f, indent=2)
	logging.debug("Manifest saved (%s)", manifest_file)


def should_exclude(path: Path, exclude_patterns: List[str]) -> bool:
	name = path.name
	return any(pat in name for pat in exclude_patterns)


def gather_files(sources: List[Path], exclude_patterns: List[str], backup_dir: Path) -> List[Path]:
	files: List[Path] = []
	for src in sources:
		if not src.exists():
			logging.warning("Source missing: %s", src)
			continue
		for root, dirs, filenames in os.walk(src):
			root_path = Path(root)
			# Prune dirs in-place
			dirs[:] = [d for d in dirs if not should_exclude(root_path / d, exclude_patterns)]
			for fn in filenames:
				fp = root_path / fn
				if should_exclude(fp, exclude_patterns):
					continue
				# avoid backing up backup_dir itself
				try:
					fp.relative_to(backup_dir)
					# if relative_to succeeds, it's inside backup_dir – skip
					continue
				except ValueError:
					pass
				if fp.is_file():
					files.append(fp)
	return files


def relative_to_common(path: Path, base_paths: List[Path]) -> str:
	for base in base_paths:
		try:
			return str(path.relative_to(base))
		except ValueError:
			continue
	return path.name  # fallback


def cleanup_old_backups(backup_dir: Path, max_age_days: int, today: dt.date, dry_run: bool, override_since: Optional[int]) -> List[Path]:
	removed: List[Path] = []
	days_threshold = override_since or max_age_days
	for child in backup_dir.iterdir():
		if not child.is_dir():
			continue
		try:
			folder_date = dt.datetime.strptime(child.name, "%Y-%m-%d").date()
		except ValueError:
			continue
		age = (today - folder_date).days
		if age > days_threshold:
			logging.info("Will remove old backup %s (age %d days)", child, age)
			removed.append(child)
			if not dry_run:
				shutil.rmtree(child, ignore_errors=True)
	return removed


def perform_backup(
	config: dict,
	dry_run: bool,
	verbose: bool,
	override_since: Optional[int],
) -> None:
	hash_method = config["hash_method"]
	backup_dir = (Path(config["backup_dir"]).expanduser().resolve())
	sources = [Path(s).expanduser().resolve() if not Path(s).is_absolute() else Path(s) for s in config["sources"]]
	exclude_patterns = config.get("exclude_patterns", [])
	max_age_days = int(config["max_age_days"])

	backup_dir.mkdir(parents=True, exist_ok=True)
	today = dt.date.today()
	today_folder = backup_dir / today.strftime("%Y-%m-%d")
	if not dry_run:
		today_folder.mkdir(exist_ok=True)

	manifest = load_manifest(backup_dir)
	manifest_files: Dict[str, dict] = manifest.setdefault("files", {})

	all_files = gather_files(sources, exclude_patterns, backup_dir)
	logging.info("Discovered %d candidate files", len(all_files))

	copied = 0
	skipped = 0
	for f in all_files:
		rel = relative_to_common(f, sources)
		stat = f.stat()
		key = rel.replace("\\", "/")
		existing = manifest_files.get(key)
		needs_copy = False
		if not existing:
			needs_copy = True
			reason = "new"
		else:
			# Quick check by size/mtime first
			if existing.get("size") != stat.st_size or existing.get("mtime") != int(stat.st_mtime):
				needs_copy = True
				reason = "changed"
			else:
				reason = "unchanged"
		if needs_copy:
			file_hash = compute_hash(f, method=hash_method)
			if existing and existing.get("hash") == file_hash:
				# Hash same means false positive from mtime/size difference
				needs_copy = False
				reason = "hash-same"
		if needs_copy:
			dest = today_folder / rel
			if not dry_run:
				dest.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(f, dest)
			logging.info("Backup %s (%s) -> %s", rel, reason, dest)
			manifest_files[key] = {
				"hash": file_hash,
				"size": stat.st_size,
				"mtime": int(stat.st_mtime),
				"last_backup": today.isoformat(),
			}
			copied += 1
		else:
			logging.debug("Skip %s (%s)", rel, reason)
			skipped += 1

	removed = cleanup_old_backups(backup_dir, max_age_days, today, dry_run, override_since)
	save_manifest(backup_dir, manifest, dry_run)

	logging.info(
		"Summary: copied=%d skipped=%d removed_old=%d dry_run=%s", copied, skipped, len(removed), dry_run
	)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Simple backup & cleanup automation")
	parser.add_argument("--config", type=str, default=DEFAULT_CONFIG_NAME, help="Path to config JSON")
	parser.add_argument("--apply", action="store_true", help="Actually perform actions (disable dry-run)")
	parser.add_argument("--init-config", action="store_true", help="Initialize a default config then exit")
	parser.add_argument("--verbose", action="store_true", help="Verbose logging (debug level)")
	parser.add_argument(
		"--since",
		type=int,
		default=None,
		help="Override retention threshold in days for cleanup (temporary override)",
	)
	return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
	args = parse_args(argv)
	log_setup(args.verbose)
	config_path = (Path(args.config) if Path(args.config).is_absolute() else SCRIPT_DIR / args.config).resolve()

	if args.init_config:
		init_config(config_path)
		return 0

	try:
		config = load_config(config_path)
	except FileNotFoundError as e:
		logging.error(str(e))
		return 1

	dry_run = not args.apply
	if dry_run:
		logging.info("Running in dry-run mode. Use --apply to make changes.")
	perform_backup(config, dry_run=dry_run, verbose=args.verbose, override_since=args.since)
	return 0


if __name__ == "__main__":  # pragma: no cover
	raise SystemExit(main())

