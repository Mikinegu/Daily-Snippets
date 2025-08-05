import os
import shutil
import time
from pathlib import Path
from datetime import datetime
import logging

class FileOrganizer:
    def __init__(self, source_directory="."):
        self.source_directory = Path(source_directory)
        self.organized_directory = self.source_directory / "Organized_Files"
        
        # Define file categories and their extensions
        self.categories = {
            "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
            "Documents": ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            "Videos": ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v'],
            "Audio": ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            "Code": ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go'],
            "Executables": ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
            "Others": []
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('file_organizer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_category_folders(self):
        """Create folders for each category if they don't exist"""
        for category in self.categories.keys():
            category_path = self.organized_directory / category
            category_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created/verified folder: {category_path}")
    
    def get_file_category(self, file_extension):
        """Determine which category a file belongs to based on its extension"""
        file_extension = file_extension.lower()
        
        for category, extensions in self.categories.items():
            if file_extension in extensions:
                return category
        
        return "Others"
    
    def organize_files(self):
        """Main function to organize files"""
        self.logger.info(f"Starting file organization in: {self.source_directory}")
        
        # Create the main organized directory
        self.organized_directory.mkdir(exist_ok=True)
        
        # Create category folders
        self.create_category_folders()
        
        # Track statistics
        stats = {category: 0 for category in self.categories.keys()}
        total_files = 0
        skipped_files = 0
        
        # Process each file in the source directory
        for file_path in self.source_directory.iterdir():
            if file_path.is_file() and file_path.name != "file_organizer.log":
                total_files += 1
                
                # Skip the organized directory itself
                if file_path.parent == self.organized_directory:
                    continue
                
                file_extension = file_path.suffix
                category = self.get_file_category(file_extension)
                
                # Create destination path
                destination = self.organized_directory / category / file_path.name
                
                # Handle duplicate filenames
                counter = 1
                original_destination = destination
                while destination.exists():
                    name_without_ext = original_destination.stem
                    ext = original_destination.suffix
                    destination = original_destination.parent / f"{name_without_ext}_{counter}{ext}"
                    counter += 1
                
                try:
                    # Move the file
                    shutil.move(str(file_path), str(destination))
                    stats[category] += 1
                    self.logger.info(f"Moved: {file_path.name} -> {category}/")
                    
                except Exception as e:
                    self.logger.error(f"Error moving {file_path.name}: {e}")
                    skipped_files += 1
        
        # Print summary
        self.logger.info("\n" + "="*50)
        self.logger.info("ORGANIZATION COMPLETE!")
        self.logger.info("="*50)
        self.logger.info(f"Total files processed: {total_files}")
        self.logger.info(f"Files organized: {total_files - skipped_files}")
        self.logger.info(f"Files skipped: {skipped_files}")
        self.logger.info("\nFiles by category:")
        
        for category, count in stats.items():
            if count > 0:
                self.logger.info(f"  {category}: {count} files")
        
        self.logger.info(f"\nOrganized files are in: {self.organized_directory}")

def main():
    """Main function to run the file organizer"""
    print("🧹 File Organizer Automation")
    print("=" * 40)
    
    # Get source directory from user or use current directory
    source_dir = input("Enter directory path to organize (or press Enter for current directory): ").strip()
    if not source_dir:
        source_dir = "."
    
    # Validate directory exists
    if not os.path.exists(source_dir):
        print(f"❌ Error: Directory '{source_dir}' does not exist!")
        return
    
    # Create and run organizer
    organizer = FileOrganizer(source_dir)
    
    print(f"\n📁 Organizing files in: {os.path.abspath(source_dir)}")
    print("⏳ Please wait...")
    
    try:
        organizer.organize_files()
        print("\n✅ File organization completed successfully!")
        print(f"📂 Check the 'Organized_Files' folder for your sorted files.")
        
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
