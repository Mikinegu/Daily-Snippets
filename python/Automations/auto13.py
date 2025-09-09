#!/usr/bin/env python3
"""
Smart File Organizer Automation
An intelligent file organization system that automatically categorizes and organizes files
based on type, content, date, and user-defined rules.
"""

import os
import shutil
import logging
import json
import hashlib
import mimetypes
from datetime import datetime, timedelta
from pathlib import Path
import re
import threading
import time
from collections import defaultdict
import schedule
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import magic  # python-magic for better file type detection
import exifread  # for image metadata
import zipfile
import tarfile
from PIL import Image
import cv2
import numpy as np

class SmartFileOrganizer:
    def __init__(self, config_file="file_organizer_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        self.file_cache = {}
        self.duplicate_files = defaultdict(list)
        self.organization_stats = {
            'files_processed': 0,
            'files_moved': 0,
            'duplicates_found': 0,
            'errors': 0
        }
        self.observer = None
        self.running = False
        
    def load_config(self):
        """Load configuration from JSON file or create default"""
        default_config = {
            "source_directories": [
                "C:\\Users\\DELLXPS\\Downloads",
                "C:\\Users\\DELLXPS\\Desktop",
                "C:\\Users\\DELLXPS\\Documents"
            ],
            "organization_rules": {
                "images": {
                    "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
                    "folder": "Images",
                    "subfolders": {
                        "by_date": True,
                        "by_camera": True,
                        "by_resolution": True
                    }
                },
                "documents": {
                    "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
                    "folder": "Documents",
                    "subfolders": {
                        "by_type": True,
                        "by_date": True
                    }
                },
                "videos": {
                    "extensions": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm"],
                    "folder": "Videos",
                    "subfolders": {
                        "by_date": True,
                        "by_resolution": True
                    }
                },
                "audio": {
                    "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
                    "folder": "Audio",
                    "subfolders": {
                        "by_artist": True,
                        "by_genre": True
                    }
                },
                "archives": {
                    "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                    "folder": "Archives",
                    "subfolders": {
                        "by_type": True
                    }
                },
                "code": {
                    "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".go"],
                    "folder": "Code",
                    "subfolders": {
                        "by_language": True
                    }
                }
            },
            "safety_settings": {
                "create_backup": True,
                "backup_location": "C:\\Users\\DELLXPS\\Documents\\FileOrganizer_Backup",
                "max_backup_size_gb": 5,
                "confirm_before_move": False
            },
            "duplicate_detection": {
                "enabled": True,
                "method": "hash",  # hash, size, or both
                "action": "move_to_duplicates"  # move_to_duplicates, delete, or report
            },
            "auto_organize": {
                "enabled": True,
                "interval_minutes": 30,
                "watch_mode": True
            },
            "advanced_features": {
                "extract_archives": True,
                "resize_images": False,
                "compress_videos": False,
                "ocr_documents": False
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return default_config
        else:
            # Save default config
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'file_organizer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of file for duplicate detection"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def detect_file_type(self, file_path):
        """Enhanced file type detection using multiple methods"""
        file_path = Path(file_path)
        
        # Method 1: Extension-based
        extension = file_path.suffix.lower()
        
        # Method 2: MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        
        # Method 3: Magic number detection
        try:
            magic_type = magic.from_file(str(file_path), mime=True)
        except:
            magic_type = None
        
        return {
            'extension': extension,
            'mime_type': mime_type,
            'magic_type': magic_type,
            'size': file_path.stat().st_size
        }
    
    def get_image_metadata(self, image_path):
        """Extract metadata from images"""
        metadata = {}
        try:
            # EXIF data
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
                if tags:
                    metadata['exif'] = {str(tag): str(value) for tag, value in tags.items()}
            
            # PIL metadata
            with Image.open(image_path) as img:
                metadata['size'] = img.size
                metadata['format'] = img.format
                metadata['mode'] = img.mode
                
        except Exception as e:
            self.logger.warning(f"Could not extract metadata from {image_path}: {e}")
        
        return metadata
    
    def categorize_file(self, file_path):
        """Determine file category based on type and content"""
        file_info = self.detect_file_type(file_path)
        extension = file_info['extension']
        
        # Check against organization rules
        for category, rules in self.config['organization_rules'].items():
            if extension in rules['extensions']:
                return category
        
        # Default category for unknown files
        return 'misc'
    
    def create_folder_structure(self, base_path, category, file_path):
        """Create organized folder structure based on rules"""
        folder_path = Path(base_path) / self.config['organization_rules'][category]['folder']
        
        if category not in self.config['organization_rules']:
            folder_path = Path(base_path) / 'Misc'
        
        # Create subfolders based on rules
        subfolders = self.config['organization_rules'][category].get('subfolders', {})
        
        if subfolders.get('by_date'):
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
            folder_path = folder_path / file_date.strftime('%Y') / file_date.strftime('%m-%B')
        
        if subfolders.get('by_type') and category == 'documents':
            doc_type = Path(file_path).suffix[1:].upper()
            folder_path = folder_path / doc_type
        
        if subfolders.get('by_language') and category == 'code':
            lang_map = {
                '.py': 'Python', '.js': 'JavaScript', '.html': 'HTML',
                '.css': 'CSS', '.java': 'Java', '.cpp': 'C++',
                '.c': 'C', '.php': 'PHP', '.rb': 'Ruby', '.go': 'Go'
            }
            lang = lang_map.get(Path(file_path).suffix.lower(), 'Other')
            folder_path = folder_path / lang
        
        # Create the folder structure
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path
    
    def handle_duplicates(self, file_path, file_hash):
        """Handle duplicate files based on configuration"""
        if not self.config['duplicate_detection']['enabled']:
            return file_path
        
        if file_hash in self.duplicate_files:
            self.organization_stats['duplicates_found'] += 1
            action = self.config['duplicate_detection']['action']
            
            if action == 'move_to_duplicates':
                dup_folder = Path(self.config['safety_settings']['backup_location']) / 'Duplicates'
                dup_folder.mkdir(parents=True, exist_ok=True)
                return dup_folder / Path(file_path).name
            elif action == 'delete':
                self.logger.info(f"Deleting duplicate: {file_path}")
                os.remove(file_path)
                return None
        
        self.duplicate_files[file_hash].append(file_path)
        return file_path
    
    def backup_file(self, source_path, destination_path):
        """Create backup of file before moving"""
        if not self.config['safety_settings']['create_backup']:
            return True
        
        backup_dir = Path(self.config['safety_settings']['backup_location'])
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Check backup size limit
        backup_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
        max_size = self.config['safety_settings']['max_backup_size_gb'] * 1024**3
        
        if backup_size > max_size:
            self.logger.warning("Backup size limit reached. Cleaning old backups...")
            self.cleanup_old_backups(backup_dir)
        
        try:
            backup_path = backup_dir / Path(source_path).name
            shutil.copy2(source_path, backup_path)
            self.logger.info(f"Backup created: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return False
    
    def cleanup_old_backups(self, backup_dir):
        """Remove oldest backup files to stay within size limit"""
        files = [(f.stat().st_mtime, f) for f in backup_dir.rglob('*') if f.is_file()]
        files.sort(key=lambda x: x[0])  # Sort by modification time
        
        # Remove oldest 20% of files
        files_to_remove = files[:len(files)//5]
        for _, file_path in files_to_remove:
            try:
                file_path.unlink()
                self.logger.info(f"Removed old backup: {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to remove backup {file_path}: {e}")
    
    def organize_file(self, file_path):
        """Main file organization logic"""
        try:
            file_path = Path(file_path)
            if not file_path.exists() or file_path.is_dir():
                return
            
            self.organization_stats['files_processed'] += 1
            
            # Detect file type and category
            category = self.categorize_file(file_path)
            file_hash = self.get_file_hash(file_path)
            
            if not file_hash:
                self.organization_stats['errors'] += 1
                return
            
            # Handle duplicates
            original_path = file_path
            file_path = self.handle_duplicates(file_path, file_hash)
            
            if file_path is None:  # File was deleted as duplicate
                return
            
            # Create destination folder
            destination_folder = self.create_folder_structure(
                self.config['source_directories'][0], category, file_path
            )
            
            destination_path = destination_folder / file_path.name
            
            # Handle name conflicts
            counter = 1
            original_dest = destination_path
            while destination_path.exists():
                stem = original_dest.stem
                suffix = original_dest.suffix
                destination_path = destination_folder / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Create backup if enabled
            if not self.backup_file(original_path, destination_path):
                self.logger.error(f"Backup failed, skipping move: {original_path}")
                return
            
            # Move file
            shutil.move(str(original_path), str(destination_path))
            self.organization_stats['files_moved'] += 1
            
            self.logger.info(f"Moved: {original_path} -> {destination_path}")
            
            # Extract archives if enabled
            if (category == 'archives' and 
                self.config['advanced_features']['extract_archives']):
                self.extract_archive(destination_path)
            
        except Exception as e:
            self.logger.error(f"Error organizing file {file_path}: {e}")
            self.organization_stats['errors'] += 1
    
    def extract_archive(self, archive_path):
        """Extract archive files"""
        try:
            extract_dir = archive_path.parent / archive_path.stem
            extract_dir.mkdir(exist_ok=True)
            
            if archive_path.suffix.lower() in ['.zip']:
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            elif archive_path.suffix.lower() in ['.tar', '.gz', '.bz2']:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_dir)
            
            self.logger.info(f"Extracted archive: {archive_path} -> {extract_dir}")
            
            # Organize extracted files
            for extracted_file in extract_dir.rglob('*'):
                if extracted_file.is_file():
                    self.organize_file(extracted_file)
                    
        except Exception as e:
            self.logger.error(f"Failed to extract {archive_path}: {e}")
    
    def scan_directory(self, directory):
        """Scan directory for files to organize"""
        directory = Path(directory)
        if not directory.exists():
            self.logger.warning(f"Directory does not exist: {directory}")
            return
        
        self.logger.info(f"Scanning directory: {directory}")
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                self.organize_file(file_path)
    
    def generate_report(self):
        """Generate organization report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.organization_stats,
            'duplicates': len(self.duplicate_files),
            'config': self.config
        }
        
        report_file = Path("logs") / f"organization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=4)
        
        self.logger.info(f"Report generated: {report_file}")
        return report
    
    def start_watch_mode(self):
        """Start file system watching for real-time organization"""
        if not self.config['auto_organize']['watch_mode']:
            return
        
        class FileHandler(FileSystemEventHandler):
            def __init__(self, organizer):
                self.organizer = organizer
            
            def on_created(self, event):
                if not event.is_directory:
                    time.sleep(1)  # Wait for file to be fully written
                    self.organizer.organize_file(event.src_path)
        
        self.observer = Observer()
        handler = FileHandler(self)
        
        for directory in self.config['source_directories']:
            if os.path.exists(directory):
                self.observer.schedule(handler, directory, recursive=True)
                self.logger.info(f"Watching directory: {directory}")
        
        self.observer.start()
        self.running = True
    
    def stop_watch_mode(self):
        """Stop file system watching"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.running = False
    
    def run_scheduled_organization(self):
        """Run organization on schedule"""
        self.logger.info("Running scheduled file organization...")
        for directory in self.config['source_directories']:
            self.scan_directory(directory)
        self.generate_report()
    
    def start(self):
        """Start the file organizer"""
        self.logger.info("Starting Smart File Organizer...")
        
        # Initial scan
        for directory in self.config['source_directories']:
            self.scan_directory(directory)
        
        # Schedule regular organization
        if self.config['auto_organize']['enabled']:
            interval = self.config['auto_organize']['interval_minutes']
            schedule.every(interval).minutes.do(self.run_scheduled_organization)
        
        # Start watch mode
        self.start_watch_mode()
        
        # Keep running
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping file organizer...")
            self.stop_watch_mode()
            self.generate_report()

def main():
    """Main function to run the file organizer"""
    organizer = SmartFileOrganizer()
    
    print("Smart File Organizer")
    print("===================")
    print("1. Run once")
    print("2. Start continuous monitoring")
    print("3. Generate report only")
    print("4. Exit")
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == '1':
        print("Running one-time organization...")
        for directory in organizer.config['source_directories']:
            organizer.scan_directory(directory)
        organizer.generate_report()
    elif choice == '2':
        print("Starting continuous monitoring...")
        organizer.start()
    elif choice == '3':
        organizer.generate_report()
    elif choice == '4':
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
