# 📦 File Compressor

A powerful web application for compressing files with smart auto-compression and manual target sizing.

![Version](https://img.shields.io/badge/version-2.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### 🎯 Two Compression Modes
- **Auto Mode** - Smart compression that automatically chooses optimal file size
- **Manual Mode** - Set exact target file size (e.g., "compress to exactly 4MB")

### 📦 File Support
- **PDFs** - Compress documents while maintaining quality
- **Images** - JPG, PNG, GIF, BMP, TIFF, WebP
- **Videos** - MP4, AVI, MOV, MKV with quality presets
- **Archives** - ZIP file optimization

### 🚀 Advanced Features
- **Batch Processing** - Upload and compress multiple files at once
- **Real-time Progress** - Live progress bars for each file
- **User Accounts** - Track compression history and statistics
- **REST API** - Integrate with your applications
- **Parallel Processing** - Compress multiple files simultaneously

### 🎨 Modern Interface
- Beautiful, responsive design
- Drag-and-drop support
- Before/after statistics
- Compression history tracking

## 🚀 Quick Start

### Installation

**1. Install system dependencies:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y poppler-utils ffmpeg

# macOS
brew install poppler ffmpeg

# Windows: Download and install
# - poppler: https://github.com/oschwartz10612/poppler-windows/releases/
# - ffmpeg: https://ffmpeg.org/download.html
```

**2. Install Python packages:**

```bash
pip install -r requirements.txt
```

**3. Run the application:**

```bash
python app.py
```

**4. Open your browser:**

Navigate to `http://localhost:5000`

## 💡 Usage

### Auto Mode (Recommended)

Perfect for when you just want files smaller:

1. Click "Auto Compress" (default mode)
2. Upload one or multiple files
3. Click "Compress Files"
4. Download compressed versions

The app automatically:
- Analyzes file types
- Chooses optimal compression
- Balances quality vs. size
- Achieves 40-70% reduction typically

### Manual Mode

Perfect for specific size requirements:

1. Click "Custom Size"
2. Enter target size in MB (e.g., "4" for 4MB)
3. Upload your file(s)
4. Click "Compress Files"
5. Get files at or near your target size

**Use cases:**
- Email attachment limits (e.g., 10MB max → set to 9MB)
- Platform requirements (e.g., "must be under 5MB")
- Storage optimization (e.g., compress 100MB folder to 30MB)

## 📊 Examples

### Example 1: Email Attachment

**Problem:** PDF is 12MB, email limit is 10MB

**Solution:**
```
1. Select "Custom Size"
2. Enter "9" as target
3. Upload PDF
4. Get 9MB compressed PDF
```

### Example 2: Photo Album

**Problem:** 50 vacation photos, 200MB total

**Solution:**
```
1. Select "Auto Compress"
2. Upload all 50 photos at once
3. Watch progress for each file
4. Download 50MB compressed album (75% savings)
```

### Example 3: Marketing Video

**Problem:** 150MB video too large for website

**Solution:**
```
1. Select "Auto Compress"
2. Upload video
3. Get web-optimized 35MB version
4. Maintains visual quality
```

## 🔌 API Usage

### Compress Files

```bash
curl -X POST http://localhost:5000/compress \
  -F "files=@document.pdf" \
  -F "files=@photo.jpg" \
  -F "mode=auto" \
  -F "quality=85"
```

### Check Progress

```bash
curl http://localhost:5000/status/<task_id>
```

### Download Result

```bash
curl http://localhost:5000/download/<task_id> -o compressed.pdf
```

See [API.md](API.md) for complete API documentation.

## 🐳 Docker Deployment

```bash
# Build and run
docker build -t file-compressor .
docker run -p 5000:5000 file-compressor

# Or use docker-compose
docker-compose up
```

## ☁️ Cloud Deployment

### Heroku

```bash
# Create Aptfile for dependencies
echo -e "poppler-utils\nffmpeg" > Aptfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Railway / Render

Both platforms support automatic deployment - just connect your GitHub repo and deploy!

## 🔐 User Accounts (Optional)

Create an account to:
- Track compression history
- View statistics and savings
- Access past compressions
- Save preferences

**Note:** Files are NOT permanently stored. Only metadata (filename, sizes, dates) is saved.

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```env
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=524288000  # 500MB
DEBUG=False
```

### Compression Defaults

Edit `app.py` to adjust compression ratios:

```python
# Auto mode compression targets
PDF_REDUCTION = 0.4      # 60% reduction
IMAGE_REDUCTION = 0.5    # 50% reduction
VIDEO_REDUCTION = 0.6    # 40% reduction
```

## 📁 Project Structure

```
file-compressor/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── setup.sh              # Automated setup script
├── README.md             # This file
├── API.md                # API documentation
├── CONTRIBUTING.md       # Contribution guidelines
└── LICENSE               # MIT License
```

## 🛠️ Development

### Run Tests

```bash
python test.py
```

### Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with debug mode
export FLASK_ENV=development
python app.py
```

## 🔒 Security

- Files processed in temporary directory
- Automatic cleanup after compression
- Password hashing (SHA-256)
- Session-based authentication
- No permanent file storage

**For production:**
- Use proper database (PostgreSQL, MySQL)
- Implement rate limiting
- Add CAPTCHA
- Enable HTTPS
- Use environment variables for secrets

## 📈 Performance

- Parallel processing for batch uploads
- Efficient memory management
- Optimized compression algorithms
- Handles files up to 500MB

## 🐛 Troubleshooting

### "ffmpeg not found"
```bash
# Install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg
```

### "poppler not found"
```bash
# Install poppler
# Ubuntu: sudo apt-get install poppler-utils
# macOS: brew install poppler
```

### Module import errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Credits

Built with:
- Flask - Web framework
- FFmpeg - Video processing
- Pillow - Image manipulation
- pdf2image - PDF rendering
- img2pdf - PDF creation

## 📧 Support

- 📖 [Full Documentation](README.md)
- 🔌 [API Docs](API.md)
- 🐛 [Report Bug](https://github.com/yourusername/file-compressor/issues)
- 💡 [Request Feature](https://github.com/yourusername/file-compressor/issues)

---

Made with ❤️ - Happy Compressing! 🚀
