#!/usr/bin/env python3
"""
File Organization Script for macOS
Organizes files by date into destination/YYYY/MM/ structure
Supports both moving and copying files (preserving originals)
"""

import os
import shutil
import datetime
from pathlib import Path
import argparse
import sys


class FileOrganizer:
    def __init__(self, source_dir, backup_dir="backup", dry_run=False, copy_mode=False, skip_confirm=False):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.dry_run = dry_run
        self.copy_mode = copy_mode
        self.skip_confirm = skip_confirm
        self.processed_files = 0
        self.skipped_files = 0
        
        # Supported file extensions (case-insensitive)
        self.supported_extensions = {
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp',
            '.heic', '.heif', '.raw', '.cr2', '.nef', '.arw', '.dng',
            # Adobe files
            '.psd', '.ai', '.eps', '.pdf', '.indd', '.psb',
            # Videos
            '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v',
            '.qt', '.3gp', '.mpg', '.mpeg', '.m2v', '.mts', '.m2ts',
            # Audio
            '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
            # Documents (optional)
            '.doc', '.docx', '.pdf', '.txt', '.rtf', '.pages'
        }
    
    def get_file_date(self, file_path):
        """Get the creation date of a file, fallback to modification date"""
        try:
            # Try to get creation date (birth time on macOS)
            stat = file_path.stat()
            if hasattr(stat, 'st_birthtime'):
                # macOS has birth time
                timestamp = stat.st_birthtime
            else:
                # Fallback to modification time
                timestamp = stat.st_mtime
            
            return datetime.datetime.fromtimestamp(timestamp)
        except Exception as e:
            print(f"Warning: Could not get date for {file_path}: {e}")
            return datetime.datetime.now()
    
    def is_supported_file(self, file_path):
        """Check if file extension is supported"""
        return file_path.suffix.lower() in self.supported_extensions
    
    def get_available_space(self, path):
        """Get available disk space in bytes"""
        try:
            stat = os.statvfs(path)
            return stat.f_bavail * stat.f_frsize
        except Exception as e:
            print(f"Warning: Could not check disk space for {path}: {e}")
            return float('inf')  # Return infinite space if can't check
    
    def calculate_total_size(self):
        """Calculate total size of files to be processed"""
        total_size = 0
        file_count = 0
        
        print("Calculating total size of files to organize...")
        
        for file_path in self.source_dir.rglob('*'):
            if file_path.is_file() and self.is_supported_file(file_path):
                try:
                    size = file_path.stat().st_size
                    total_size += size
                    file_count += 1
                except Exception as e:
                    print(f"Warning: Could not get size for {file_path}: {e}")
        
        return total_size, file_count
    
    def confirm_operation(self, file_count, total_size, format_size_func):
        """Ask user for confirmation before proceeding"""
        print("📋 OPERATION SUMMARY")
        print("=" * 50)
        
        operation = "COPY" if self.copy_mode else "MOVE"
        print(f"Operation: {operation}")
        print(f"Source: {self.source_dir}")
        print(f"Destination: {self.backup_dir}")
        print(f"Files to process: {file_count}")
        print(f"Total size: {format_size_func(total_size)}")
        
        if self.copy_mode:
            print(f"Mode: Copy files (originals will be preserved)")
        else:
            print(f"Mode: Move files (originals will be moved to destination)")
        
        print("=" * 50)
        print("Files will be organized by creation date into: destination/YYYY/MM/")
        print("=" * 50)
        
        while True:
            try:
                response = input("Do you want to proceed? [y/N]: ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no', '']:
                    return False
                else:
                    print("Please enter 'y' for Yes or 'n' for No.")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                return False
    
    def print_final_summary(self):
        """Print comprehensive summary of the operation"""
        print("\n" + "=" * 60)
        print("📊 OPERATION SUMMARY")
        print("=" * 60)
        
        operation = "COPY" if self.copy_mode else "MOVE"
        status = "DRY RUN" if self.dry_run else "COMPLETED"
        
        print(f"Status: {status}")
        print(f"Operation: {operation}")
        print(f"Source: {self.source_dir}")
        print(f"Destination: {self.backup_dir}")
        print("-" * 60)
        print(f"✅ Successfully processed: {self.processed_files} files")
        print(f"⏭️  Skipped: {self.skipped_files} files")
        print(f"📁 Total files found: {self.processed_files + self.skipped_files}")
        
        if self.processed_files > 0:
            print(f"\n📂 Files organized into: {self.backup_dir}/YYYY/MM/ structure")
            
            if self.copy_mode and not self.dry_run:
                print(f"💾 Original files preserved in: {self.source_dir}")
            elif not self.copy_mode and not self.dry_run:
                print(f"📦 Files moved from: {self.source_dir}")
        
        if self.dry_run:
            operation = "copy" if self.copy_mode else "move"
            print(f"\n🔄 This was a dry run. Use --execute to actually {operation} files.")
        else:
            print(f"\n🎉 Organization complete!")
        
        print("=" * 60)
    
    def create_destination_structure(self, date_obj):
        """Create destination/YYYY/MM/ directory structure"""
        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        
        destination_path = self.backup_dir / year / month
        
        if not self.dry_run:
            destination_path.mkdir(parents=True, exist_ok=True)
        
        return destination_path
    
    def process_file(self, source_file, destination_dir):
        """Copy or move file to destination directory with conflict handling"""
        destination_file = destination_dir / source_file.name
        
        # Handle file name conflicts
        counter = 1
        original_stem = source_file.stem
        original_suffix = source_file.suffix
        
        while destination_file.exists():
            new_name = f"{original_stem}_{counter}{original_suffix}"
            destination_file = destination_dir / new_name
            counter += 1
        
        operation = "copy" if self.copy_mode else "move"
        
        if self.dry_run:
            print(f"[DRY RUN] Would {operation}: {source_file} -> {destination_file}")
        else:
            try:
                if self.copy_mode:
                    shutil.copy2(str(source_file), str(destination_file))
                    print(f"Copied: {source_file.name} -> {destination_file}")
                else:
                    shutil.move(str(source_file), str(destination_file))
                    print(f"Moved: {source_file.name} -> {destination_file}")
            except Exception as e:
                error_msg = str(e)
                if "No space left on device" in error_msg or "not enough space" in error_msg.lower():
                    print(f"💾 DISK FULL! Cannot {operation} {source_file.name}")
                    print(f"   Error: {e}")
                    print(f"   💡 Free up space on destination drive or use a different destination")
                else:
                    print(f"Error {operation}ing {source_file}: {e}")
                return False
        
        return True
    
    def organize_files(self):
        """Main function to organize files recursively through all subdirectories"""
        if not self.source_dir.exists():
            print(f"Error: Source directory '{self.source_dir}' does not exist.")
            return
        
        if self.dry_run:
            operation = "copied" if self.copy_mode else "moved"
            print(f"=== DRY RUN MODE - No files will be {operation} ===")
        
        operation_mode = "COPY" if self.copy_mode else "MOVE"
        print(f"Operation mode: {operation_mode}")
        print(f"Scanning directory: {self.source_dir}")
        print(f"Destination directory: {self.backup_dir}")
        print(f"Supported extensions: {', '.join(sorted(self.supported_extensions))}")
        print("-" * 50)
        
        # Check disk space before processing (only for copy mode or if destination is different drive)
        if self.copy_mode or not self.dry_run:
            total_size, file_count = self.calculate_total_size()
            
            if total_size > 0:
                # Convert bytes to human readable format
                def format_size(size_bytes):
                    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                        if size_bytes < 1024.0:
                            return f"{size_bytes:.1f} {unit}"
                        size_bytes /= 1024.0
                    return f"{size_bytes:.1f} PB"
                
                print(f"Found {file_count} files to organize ({format_size(total_size)})")
                
                # Check available space only for copy mode or if not dry run
                if not self.dry_run:
                    available_space = self.get_available_space(self.backup_dir)
                    
                    if self.copy_mode:
                        # Copy mode needs full space
                        required_space = total_size
                    else:
                        # Move mode might need some temporary space, but much less
                        required_space = total_size * 0.1  # 10% buffer for move operations
                    
                    if available_space < required_space:
                        print(f"❌ INSUFFICIENT DISK SPACE!")
                        print(f"   Required: {format_size(required_space)}")
                        print(f"   Available: {format_size(available_space)}")
                        print(f"   Shortfall: {format_size(required_space - available_space)}")
                        
                        if self.copy_mode:
                            print(f"\n💡 Tips:")
                            print(f"   - Use move mode instead of copy (removes --copy flag)")
                            print(f"   - Free up space on destination drive")
                            print(f"   - Use a different destination with more space")
                        else:
                            print(f"\n💡 Tips:")
                            print(f"   - Free up space on destination drive")
                            print(f"   - Use a different destination with more space")
                        
                        return
                    else:
                        print(f"✅ Sufficient space available ({format_size(available_space)})")
                
                print("-" * 50)
                
                # Ask for confirmation before proceeding (skip for dry run or if skip_confirm is True)
                if not self.dry_run and not self.skip_confirm:
                    if not self.confirm_operation(file_count, total_size, format_size):
                        print("Operation cancelled by user.")
                        return
        
        # Walk through all files recursively (including all subdirectories)
        for file_path in self.source_dir.rglob('*'):
            if file_path.is_file():
                if self.is_supported_file(file_path):
                    # Get file date
                    file_date = self.get_file_date(file_path)
                    
                    # Create destination directory structure
                    destination_path = self.create_destination_structure(file_date)
                    
                    # Process the file (copy or move)
                    if self.process_file(file_path, destination_path):
                        self.processed_files += 1
                    else:
                        self.skipped_files += 1
                else:
                    print(f"Skipping unsupported file: {file_path.name}")
                    self.skipped_files += 1
        
        # Print summary
        self.print_final_summary()


def main():
    parser = argparse.ArgumentParser(description="Organize files by date into destination structure")
    parser.add_argument("-s", "--source", required=True, help="Source directory to scan")
    parser.add_argument("-d", "--destination", required=True, help="Destination directory for organized files")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Show what would be done without processing files")
    parser.add_argument("-e", "--execute", action="store_true", help="Actually process files (opposite of dry-run)")
    parser.add_argument("-c", "--copy", action="store_true", help="Copy files instead of moving them (preserves originals)")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt and proceed automatically")
    
    args = parser.parse_args()
    
    # Default to dry run unless --execute is specified
    dry_run = not args.execute
    
    if dry_run:
        operation = "copy" if args.copy else "move"
        print(f"Running in DRY RUN mode. Use --execute to actually {operation} files.")
    
    organizer = FileOrganizer(
        source_dir=args.source,
        backup_dir=args.destination,
        dry_run=dry_run,
        copy_mode=args.copy,
        skip_confirm=args.yes
    )
    
    organizer.organize_files()


if __name__ == "__main__":
    main() 