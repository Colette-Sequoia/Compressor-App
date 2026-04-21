# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## 📋 What You Need

- Python 3.8 or higher
- poppler-utils (for PDFs)
- ffmpeg (for videos)

## ⚡ Fast Setup

### Linux/Mac

```bash
# 1. Install dependencies
# Ubuntu/Debian:
sudo apt-get install poppler-utils ffmpeg

# macOS:
brew install poppler ffmpeg

# 2. Install Python packages
pip install -r requirements.txt

# 3. Run!
python app.py

# 4. Open browser
# Go to http://localhost:5000
```

### Windows

```powershell
# 1. Download and install:
#    - poppler: https://github.com/oschwartz10612/poppler-windows/releases/
#    - ffmpeg: https://ffmpeg.org/download.html

# 2. Install Python packages
pip install -r requirements.txt

# 3. Run!
python app.py

# 4. Open browser
# Go to http://localhost:5000
```

## 🎯 Using the App

### Auto Mode (Just Make It Smaller)

1. Upload your file(s)
2. Click "Compress Files"
3. Download!

**The app automatically picks the best compression.**

### Manual Mode (Exact Size)

1. Click "Custom Size"
2. Enter target size (e.g., "4" for 4MB)
3. Upload your file(s)
4. Click "Compress Files"
5. Download!

**You get files at or very close to your target.**

## 📦 Batch Processing

Upload multiple files at once:
- Drag and drop multiple files
- Or click and select multiple
- Watch progress for each file
- Download individually or all at once

## 🎥 Video Compression

Upload MP4, AVI, MOV, or MKV files:
- Auto mode picks best settings
- Manual mode targets specific size
- Maintains quality while reducing size

## 🐳 Docker (Alternative)

Don't want to install dependencies?

```bash
docker-compose up
```

Then open http://localhost:5000

## ❓ Common Issues

**"ffmpeg not found"**
→ Install ffmpeg (see setup above)

**"poppler not found"**
→ Install poppler-utils (see setup above)

**"Module not found"**
→ Run `pip install -r requirements.txt`

## 📖 Need More Help?

- Full docs: [README.md](README.md)
- API docs: [API.md](API.md)
- Issues: [GitHub Issues](https://github.com/yourusername/file-compressor/issues)

---

That's it! You're ready to compress files! 🎉
