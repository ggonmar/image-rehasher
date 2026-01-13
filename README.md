# Image Rehasher

A media processing tool that modifies images and videos with subtle changes to create new versions while preserving metadata.

## Overview

This script processes media files (images and videos) by:
1. **Applying minimal visual transformations** to alter the file hash
2. **Preserving original metadata** (EXIF, tags, etc.)
3. **Randomizing timestamps** slightly (100-200ms offset)

This is useful for creating new file versions while maintaining the original media's metadata integrity.

## Requirements

- Python 3.x
- `PIL` (Pillow) - for image processing
- `ffmpeg` - for video re-encoding
- `exiftool` - for metadata manipulation

Install dependencies:
```bash
pip install Pillow
```

Ensure `ffmpeg` and `exiftool` are installed and available in your PATH.

## Usage

1. Place media files in the `input/` folder
2. Run the script:
   ```bash
   python media_rehasher.py
   ```
3. Processed files appear in the `output/` folder with `_new` suffix

## Supported Formats

**Images:** `.jpg`, `.jpeg`, `.png`, `.heic`

**Videos:** `.mp4`, `.mov`, `.avi`, `.mkv`

## How It Works

### Images
- Upscales by 0.1% then crops back to original size
- Saves with 100% quality and optimization
- Copies all EXIF metadata
- Shifts all dates by 100-200ms randomly

### Videos
- Re-encodes using H.264 codec (CRF 18, fast preset)
- Keeps audio stream unchanged
- Copies all metadata from original
- Shifts all dates by 100-200ms randomly

## Output

Files are saved to `output/` with the naming pattern:
```
original_filename_new.extension
```

## Notes

- The visual changes are minimal and often imperceptible
- All original metadata is preserved and transferred
- Timestamps are slightly randomized to ensure different file hashes
- Progress is printed to console during processing
