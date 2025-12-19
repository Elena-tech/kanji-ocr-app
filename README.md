# Kanji OCR Camera Application

A production-ready web application that recognizes Japanese kanji characters from uploaded images and provides instant dictionary lookups with meanings, readings, and usage examples.

🚀 **Status:** MVP Complete - Ready for local testing

## Features

- 📸 **Image Upload** - Drag & drop or select images for OCR processing
- 🔍 **Kanji Recognition** - OCR processing with confidence scores (stubbed, ready for Tesseract integration)
- 📖 **Dictionary Lookup** - Instant kanji definitions with readings and examples
- 🎨 **Clean UI** - Responsive, modern interface built with vanilla JavaScript
- ⚡ **Lightweight** - No heavy frameworks, fast loading times

## Tech Stack

### Backend
- **Flask 3.0+** - Lightweight Python web framework
- **Python 3.11+** - Modern Python with type hints
- **Future:** Tesseract OCR for real kanji recognition

### Frontend
- **Vanilla HTML/CSS/JavaScript** - No frameworks, pure web technologies
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Future:** getUserMedia API for camera capture

### APIs & Services (Planned)
- **Jisho API** - Japanese dictionary lookups
- **Tesseract OCR** - Japanese character recognition with jpn.traineddata

## Project Structure

```
kanji-ocr-app/
├── app/                      # Flask application
│   ├── __init__.py          # Application factory
│   ├── routes.py            # API routes and view handlers
│   ├── static/              # Static assets
│   │   ├── css/
│   │   │   └── styles.css   # Application styles
│   │   ├── js/
│   │   │   └── main.js      # Frontend JavaScript
│   │   └── images/          # Static images
│   └── templates/
│       └── index.html       # Main application page
├── uploads/                  # Uploaded images (gitignored)
├── run.py                   # Development server entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Elena-tech/kanji-ocr-app.git
   cd kanji-ocr-app
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

### Running the Application

**Option 1: Using Flask CLI (Recommended)**
```bash
flask run
```

**Option 2: Using Python directly**
```bash
python run.py
```

The application will start on **http://127.0.0.1:5000**

Open your browser and navigate to the URL to use the application.

## API Endpoints

### Main Routes

- **GET /** - Main application page
- **GET /health** - Health check endpoint (returns JSON status)

### OCR & Dictionary API

- **POST /api/upload** - Upload image for OCR processing
  - Accepts: multipart/form-data with 'image' file
  - Returns: JSON with OCR results
  - Max file size: 16MB
  - Allowed formats: PNG, JPG, JPEG, GIF, WebP

- **GET /api/lookup/{kanji}** - Look up kanji in dictionary
  - Returns: JSON with meanings, readings, examples
  - Currently stubbed - real API integration pending

## Current Implementation Status

### ✅ Completed

- [x] Flask backend with application factory pattern
- [x] File upload handling with validation
- [x] RESTful API structure
- [x] Responsive frontend UI with drag-and-drop
- [x] Image preview and processing workflow
- [x] OCR results display with character cards
- [x] Dictionary lookup interface
- [x] Error handling and user feedback
- [x] Loading states and animations
- [x] Project structure and organization

### 🚧 Using Stubs (TODOs)

- [ ] **Real OCR Integration** - Currently using stubbed data
  - TODO: Install Tesseract OCR
  - TODO: Install pytesseract Python wrapper
  - TODO: Download Japanese language pack (jpn.traineddata)
  - TODO: Implement image preprocessing
  - TODO: Integrate OCR processing in `routes.py:perform_ocr_stub()`

- [ ] **Dictionary API Integration** - Currently using stubbed data
  - TODO: Integrate Jisho API or JMDict
  - TODO: Add API rate limiting
  - TODO: Implement caching for lookups
  - TODO: Replace stub in `routes.py:get_dictionary_stub()`

### 🔮 Future Enhancements

- [ ] Camera capture using getUserMedia API
- [ ] Image cropping/editing before OCR
- [ ] OCR result editing (correct mistakes)
- [ ] Search history and favorites
- [ ] Export functionality (Anki, CSV)
- [ ] Offline support with Service Worker (PWA)
- [ ] User accounts and cloud sync
- [ ] Mobile app version (React Native)
- [ ] Stroke order diagrams
- [ ] Example sentences with audio

## Development

### Adding Real OCR Support

1. **Install Tesseract OCR**
   ```bash
   # macOS
   brew install tesseract tesseract-lang

   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-jpn

   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Uncomment OCR dependencies in requirements.txt**
   ```bash
   pip install pytesseract Pillow opencv-python numpy
   ```

3. **Update `app/routes.py`**
   - Replace `perform_ocr_stub()` with real Tesseract implementation
   - Add image preprocessing (grayscale, contrast enhancement)
   - Configure Tesseract for Japanese (jpn mode)

### Adding Dictionary API

1. **Uncomment requests in requirements.txt**
   ```bash
   pip install requests
   ```

2. **Update `app/routes.py`**
   - Replace `get_dictionary_stub()` with Jisho API calls
   - Add caching to reduce API calls
   - Handle API errors gracefully

## Testing

### Manual Testing

1. Start the application
2. Upload a test image (or use sample images)
3. Verify OCR results display (currently stubbed)
4. Click on kanji characters to see dictionary info
5. Check error handling with invalid files

### API Testing

```bash
# Health check
curl http://127.0.0.1:5000/health

# Upload test (replace with actual image path)
curl -X POST -F "image=@test.jpg" http://127.0.0.1:5000/api/upload

# Dictionary lookup
curl http://127.0.0.1:5000/api/lookup/日
```

## Deployment Considerations

### Questions for Production Deployment

1. **Platform Choice**
   - Heroku (easy, free tier available)
   - AWS/GCP/Azure (more control, scalable)
   - DigitalOcean/Linode (simple VPS)
   - Vercel/Netlify (static frontend + serverless functions)

2. **Database**
   - Currently file-based (uploads folder)
   - Consider PostgreSQL for user data
   - Redis for caching dictionary lookups

3. **Storage**
   - Local filesystem (current, simple)
   - AWS S3 (scalable, recommended for production)
   - Cloudinary (image optimization)

4. **OCR Processing**
   - Synchronous (current, simple but blocking)
   - Async with Celery (better UX, more complex)
   - External service (Google Vision API, AWS Textract)

5. **Security**
   - Add CSRF protection
   - Implement rate limiting
   - Add user authentication (if needed)
   - Use HTTPS in production
   - Secure file upload validation

### Recommended Next Steps

1. ✅ **Done:** Basic web app structure
2. **Next:** Integrate real Tesseract OCR
3. **Then:** Add Jisho API integration
4. **After:** Deploy to Heroku/cloud platform
5. **Finally:** Add advanced features (camera, PWA, etc.)

## Contributing

This is a learning project. Feel free to fork and experiment!

## License

MIT License - Free to use and modify

---

**Project Status:** 🟢 MVP Complete - Ready for OCR/API integration

**Created:** December 19, 2025
**Last Updated:** December 19, 2025
