# File Organizer Script for macOS

A Python script that automatically organizes your files by date into a clean backup structure.

## Features

- 📁 **Recursive scanning**: Automatically scans through all subdirectories and nested folders
- 📅 Organizes files by creation date into `destination/YYYY/MM/` structure
- 🎯 Supports common media file types (images, videos, audio, documents)
- 🔒 Safe mode with dry-run by default
- 🔄 Handles file name conflicts automatically
- 📂 **Copy mode**: Preserves original files while organizing (use `--copy` flag)
- ✅ **Interactive confirmation**: Shows summary and asks for confirmation before proceeding
- 🚀 Easy to use and maintain

## Supported File Types

- **Images**: jpg, jpeg, png, gif, bmp, tiff, webp, heic, heif, raw, cr2, nef, arw, dng
- **Adobe Files**: psd, ai, eps, pdf, indd, psb
- **Videos**: mp4, mov, avi, mkv, wmv, flv, webm, m4v, qt, 3gp, mpg, mpeg, m2v, mts, m2ts
- **Audio**: mp3, wav, flac, aac, ogg, wma, m4a
- **Documents**: doc, docx, pdf, txt, rtf, pages

## Usage

### Basic Usage

First, make the script executable:
```bash
chmod +x main.py
```

**Test first (dry run mode - default):**
```bash
python3 main.py -s "/path/to/your/messy/folder" -d "/path/to/destination/folder"
```

**Actually move files:**
```bash
python3 main.py -s "/path/to/your/messy/folder" -d "/path/to/destination/folder" --execute
```

**Copy files (preserve originals):**
```bash
python3 main.py -s "/path/to/your/messy/folder" -d "/path/to/destination/folder" --copy --execute
```

**Skip confirmation prompt:**
```bash
python3 main.py -s "/path/to/your/messy/folder" -d "/path/to/destination/folder" --execute --yes
```

### Advanced Options

**Custom destination directory:**
```bash
python3 main.py -s "/path/to/source" -d "/path/to/my_organized_files" --execute
```

**Force dry run (useful for testing):**
```bash
python3 main.py -s "/path/to/source" -d "/path/to/destination" --dry-run
```

**Copy files instead of moving (preserves originals):**
```bash
python3 main.py -s "/path/to/source" -d "/path/to/destination" --copy --execute
```

### Examples

1. **Organize Downloads folder:**
   ```bash
   python3 main.py -s ~/Downloads -d ~/OrganizedFiles --execute
   ```

2. **Test organization of Desktop:**
   ```bash
   python3 main.py -s ~/Desktop -d ~/OrganizedDesktop
   ```

3. **Organize with custom destination folder:**
   ```bash
   python3 main.py -s "/Volumes/External/Photos" -d "/Volumes/External/organized_photos" --execute
   ```

4. **Copy files to organize (preserve originals):**
   ```bash
   python3 main.py -s ~/Desktop -d ~/OrganizedDesktop --copy --execute
   ```

5. **Test copy mode (dry run):**
   ```bash
   python3 main.py -s "/Volumes/External/Photos" -d "/Volumes/External/organized_photos" --copy
   ```

6. **Organize deeply nested folders:**
   ```bash
   python3 main.py -s "/Users/username/messy_folder_with_many_subfolders" -d "/Users/username/organized" --execute
   ```

## How Nested Folders Work

The script **automatically scans through all subdirectories** in your source folder. For example:

**Source folder structure:**
```
messy_folder/
├── IMG_001.jpg
├── documents/
│   ├── report.pdf
│   └── old_files/
│       └── archive.doc
├── photos/
│   ├── vacation/
│   │   ├── beach.jpg
│   │   └── sunset.png
│   └── family/
│       └── birthday.heic
└── videos/
    └── clips/
        └── movie.mp4
```

**Organized output structure:**
```
destination/
├── 2024/
│   ├── 01/
│   │   ├── IMG_001.jpg
│   │   ├── beach.jpg
│   │   └── movie.mp4
│   ├── 02/
│   │   ├── report.pdf
│   │   └── sunset.png
│   └── 12/
│       ├── birthday.heic
│       └── archive.doc
```

**The script finds files no matter how deeply nested they are!**

## Interactive Confirmation

When you run the script with `--execute`, it will show you a summary and ask for confirmation:

```
✅ Found 247 files to organize (3.2 GB)
✅ Sufficient space available (45.8 GB)
--------------------------------------------------
📋 OPERATION SUMMARY
==================================================
Operation: MOVE
Source: /Users/username/Downloads
Destination: /Users/username/organized
Files to process: 247
Total size: 3.2 GB
Mode: Move files (originals will be moved to destination)
==================================================
Files will be organized by creation date into: destination/YYYY/MM/
==================================================
Do you want to proceed? [y/N]: y
```

**Skip confirmation with `--yes` flag:**
```bash
python3 main.py -s source -d dest --execute --yes
```

## Operation Summary

After completion, you'll see a detailed summary:

```
============================================================
📊 OPERATION SUMMARY
============================================================
Status: COMPLETED
Operation: MOVE
Source: /Users/username/Downloads
Destination: /Users/username/organized
------------------------------------------------------------
✅ Successfully processed: 247 files
⏭️  Skipped: 15 files
📁 Total files found: 262

📂 Files organized into: /Users/username/organized/YYYY/MM/ structure
📦 Files moved from: /Users/username/Downloads

🎉 Organization complete!
============================================================
```

## Safety Features

- **Dry run by default**: The script shows what it would do without actually processing files
- **Interactive confirmation**: Shows detailed summary and asks for confirmation before proceeding
- **Copy mode**: Use `--copy` to preserve original files while organizing
- **Disk space checking**: Automatically checks available space before starting (prevents partial failures)
- **Conflict handling**: If a file with the same name exists, it adds a number (e.g., `photo_1.jpg`)
- **Error handling**: Continues processing other files if one fails
- **Detailed logging**: Shows exactly what files are being processed

## Command Line Options

- `--source` or `-s`: Path to the directory you want to organize (required)
- `--destination` or `-d`: Path to the destination directory for organized files (required)
- `--execute` or `-e`: Actually process files (without this, it's just a dry run)
- `--dry-run` or `-n`: Force dry run mode (for testing)
- `--copy` or `-c`: Copy files instead of moving them (preserves original files)
- `--yes` or `-y`: Skip confirmation prompt and proceed automatically

## Tips

1. **Always test first**: Run without `--execute` to see what would happen
2. **Use absolute paths**: Like `/Users/yourusername/Downloads` instead of `~/Downloads`
3. **External drives**: The script works with external drives and network locations
4. **Undo**: If you need to undo, you can manually move files back or write a reverse script (copy mode makes this unnecessary)
5. **Both paths required**: You must specify both source (`-s`) and destination (`-d`) directories
6. **Copy vs Move**: Use `--copy` to preserve original files, or move them by default (saves space)
7. **Nested folders**: The script automatically finds files in all subdirectories, no matter how deep
8. **Disk space**: The script checks available space before starting - copy mode needs full space, move mode needs much less

## Troubleshooting

- **Permission errors**: Make sure you have read/write access to both source and destination
- **Python not found**: Use `python3` instead of `python`
- **File dates**: The script uses creation date on macOS, modification date as fallback

### Insufficient Disk Space

The script automatically checks disk space before starting:

**If there's not enough space, you'll see:**
```
❌ INSUFFICIENT DISK SPACE!
   Required: 15.2 GB
   Available: 8.1 GB
   Shortfall: 7.1 GB

💡 Tips:
   - Use move mode instead of copy (removes --copy flag)
   - Free up space on destination drive
   - Use a different destination with more space
```

**Solutions:**
1. **Use move mode**: `python3 main.py -s source -d dest --execute` (no `--copy`)
2. **Free up space**: Delete unnecessary files on destination drive
3. **Different destination**: Use a drive with more space
4. **Process in batches**: Organize smaller folders separately

## Requirements

- macOS (tested on macOS 10.15+)
- Python 3.6+ (comes pre-installed on macOS)
- No additional packages required (uses only built-in Python libraries)

## License

This script is provided as-is. Use at your own risk. Always backup important files before running! 