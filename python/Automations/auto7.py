"""Downloads Organizer Automation

Organize files in a folder (default: your Downloads) into categorized subfolders.
Pure standard library, supports dry-run and optional watch (polling) mode.

Examples:
  - One-off (move files):
	  python auto7.py --source "%USERPROFILE%/Downloads" --dest Organized

  - Dry-run to preview actions:
	  python auto7.py --dry-run

  - Watch every 60s and copy instead of move:
	  python auto7.py --watch --interval 60 --copy

Notes:
  - Files are categorized by extension. Unknown types go to "Other".
  - Name collisions are resolved by appending (1), (2), ... to the file name.
  - Use --recursive to also process files in subfolders (excluding the destination tree).
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple


DEFAULT_RULES: Dict[str, str] = {
	# Images
	".jpg": "Images",
	".jpeg": "Images",
	".png": "Images",
	".gif": "Images",
	".bmp": "Images",
	".tiff": "Images",
	".webp": "Images",
    
	# Videos
	".mp4": "Videos",
	".mov": "Videos",
	".avi": "Videos",
	".mkv": "Videos",
	".webm": "Videos",
    
	# Audio
	".mp3": "Audio",
	".wav": "Audio",
	".flac": "Audio",
	".aac": "Audio",
    
	# Documents
	".pdf": "Documents",
	".doc": "Documents",
	".docx": "Documents",
	".xls": "Documents",
	".xlsx": "Documents",
	".ppt": "Documents",
	".pptx": "Documents",
	".txt": "Documents",
	".rtf": "Documents",
    
	# Archives
	".zip": "Archives",
	".rar": "Archives",
	".7z": "Archives",
	".tar": "Archives",
	".gz": "Archives",
	".bz2": "Archives",
    
	# Code
	".py": "Code",
	".js": "Code",
	".ts": "Code",
	".html": "Code",
	".css": "Code",
	".json": "Code",
	".yaml": "Code",
	".yml": "Code",
	".xml": "Code",
    
	# Data
	".csv": "Data",
	".parquet": "Data",
	".xlsxm": "Data",
	".sqlite": "Data",
    
	# Installers
	".exe": "Installers",
	".msi": "Installers",
	".dmg": "Installers",
}


@dataclass
class Config:
	source: Path
	dest: Path
	recursive: bool = False
	copy_instead_of_move: bool = False
	dry_run: bool = False
	watch: bool = False
	interval: int = 30
	rules: Dict[str, str] = None  # type: ignore[assignment]

	def validate(self) -> None:
		if not self.source.exists():
			raise FileNotFoundError(f"Source folder not found: {self.source}")
		if not self.source.is_dir():
			raise NotADirectoryError(f"Source path is not a directory: {self.source}")
		if self.interval <= 0:
			raise ValueError("--interval must be > 0 seconds")
		if self.rules is None:
			self.rules = DEFAULT_RULES.copy()
		# Ensure destination exists
		self.dest.mkdir(parents=True, exist_ok=True)


def guess_category(path: Path, rules: Dict[str, str]) -> str:
	ext = path.suffix.lower()
	return rules.get(ext, "Other")


def iter_files(source: Path, recursive: bool, exclude: Path) -> Iterable[Path]:
	if recursive:
		for p in source.rglob("*"):
			if p.is_file() and not p.is_relative_to(exclude):
				yield p
	else:
		for p in source.iterdir():
			if p.is_file():
				yield p


def unique_destination(dest_dir: Path, filename: str) -> Path:
	base = Path(filename).stem
	suffix = Path(filename).suffix
	candidate = dest_dir / filename
	n = 1
	while candidate.exists():
		candidate = dest_dir / f"{base} ({n}){suffix}"
		n += 1
	return candidate


def ensure_dir(path: Path) -> None:
	path.mkdir(parents=True, exist_ok=True)


def organize_once(cfg: Config) -> Tuple[int, int]:
	moved = 0
	skipped = 0
	for file in iter_files(cfg.source, cfg.recursive, cfg.dest):
		# Skip if file already inside destination tree
		try:
			if file.is_relative_to(cfg.dest):
				continue
		except AttributeError:
			# Python < 3.9 compatibility: fallback check
			try:
				file.relative_to(cfg.dest)
				continue
			except Exception:
				pass

		category = guess_category(file, cfg.rules)
		target_dir = cfg.dest / category
		ensure_dir(target_dir)
		target = unique_destination(target_dir, file.name)

		action = "COPY" if cfg.copy_instead_of_move else "MOVE"
		print(f"{action}: {file} -> {target}")

		if cfg.dry_run:
			skipped += 1
			continue

		try:
			if cfg.copy_instead_of_move:
				shutil.copy2(file, target)
				file.unlink()
			else:
				shutil.move(str(file), str(target))
			moved += 1
		except Exception as e:
			print(f"[WARN] Failed to process {file}: {e}")
			skipped += 1
	return moved, skipped


def watch_loop(cfg: Config) -> None:
	print(f"Watching '{cfg.source}' every {cfg.interval}s. Press Ctrl+C to stop.")
	try:
		while True:
			moved, skipped = organize_once(cfg)
			if moved or skipped:
				print(f"Summary: moved={moved}, skipped={skipped}")
			time.sleep(cfg.interval)
	except KeyboardInterrupt:
		print("Stopped.")


def parse_args(argv: list[str]) -> Config:
	default_source = Path(os.path.expanduser("~/Downloads")).resolve()
	parser = argparse.ArgumentParser(description="Organize files in a folder by type.")
	parser.add_argument("--source", type=Path, default=default_source, help="Folder to organize (default: ~/Downloads)")
	parser.add_argument("--dest", type=Path, default=None, help="Destination root (default: <source>/Organized)")
	parser.add_argument("--recursive", action="store_true", help="Process files in subdirectories as well")
	parser.add_argument("--copy", dest="copy", action="store_true", help="Copy instead of move (originals removed after successful copy)")
	parser.add_argument("--dry-run", action="store_true", help="Preview actions without changing files")
	parser.add_argument("--watch", action="store_true", help="Run continuously, polling every --interval seconds")
	parser.add_argument("--interval", type=int, default=30, help="Polling interval in seconds for --watch mode")
	args = parser.parse_args(argv)

	dest = args.dest or (args.source / "Organized")
	return Config(
		source=args.source,
		dest=dest,
		recursive=args.recursive,
		copy_instead_of_move=args.copy,
		dry_run=args.dry_run,
		watch=args.watch,
		interval=args.interval,
		rules=DEFAULT_RULES.copy(),
	)


def main(argv: list[str] | None = None) -> int:
	cfg = parse_args(argv or sys.argv[1:])
	try:
		cfg.validate()
	except Exception as e:
		print(f"Invalid configuration: {e}")
		return 2

	if cfg.watch:
		watch_loop(cfg)
		return 0

	moved, skipped = organize_once(cfg)
	print(f"Done. moved={moved}, skipped={skipped}")
	return 0


if __name__ == "__main__":  # pragma: no cover
	raise SystemExit(main())

