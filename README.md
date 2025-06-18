# Ultimate File Converter

Ultimate File Converter is a desktop application built with Python and Tkinter that allows you to convert images and audio files between various formats. It features both single and batch file conversion modes, a modern dark theme, and a user-friendly graphical interface.

## Features
- Convert single or multiple files at once
- Supports popular image formats: PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF
- Supports popular audio formats: MP3, WAV, AAC, OGG, FLAC
- Batch conversion with automatic output folder creation
- Remembers window size and position
- Modern dark theme using sv-ttk

## Requirements
- Python 3.7+
- [FFmpeg](https://ffmpeg.org/) (required for audio conversions)

## Installation
1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Install FFmpeg and ensure it is in your system PATH for audio conversions.

## Usage
Run the application with:
```bash
python main.py
```

- Use the GUI to select files, choose formats, and convert.
- For batch conversions, all selected files must be of the same format.

## File Structure
- `main.py` - Application entry point
- `GUI.py` - GUI layout and logic
- `Limiter.py` - Controller for file operations and conversions
- `Conversions.py` - Supported formats and conversion rules
- `requirements.txt` - Python dependencies
- `favicon.ico` - Application icon

## Screenshots
Screenshots are available in the `Screenshots/` folder.
![Default](Screenshots/Default.png)

## License
Check out [LICENSE](LICENSE) for details.

