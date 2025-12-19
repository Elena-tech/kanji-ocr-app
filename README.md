# Kanji OCR Camera Application

A smart application that recognizes Japanese kanji characters from camera images and provides instant dictionary lookups with meanings, readings, and usage examples.

## Project Overview

This application aims to help Japanese language learners and readers by:
- Capturing images of Japanese text using device camera
- Recognizing kanji characters using OCR technology
- Looking up character meanings, readings (kun-yomi and on-yomi), and example words
- Providing an intuitive interface for quick kanji identification

## Tech Stack Options

### Option 1: Mobile App (React Native) - **RECOMMENDED**
**Best for:** Portable learning, real-world kanji recognition

**Pros:**
- Native camera access on iOS and Android
- Portable - use anywhere (restaurants, books, signs, etc.)
- Single codebase for both platforms
- Large ecosystem of libraries

**Tech Stack:**
- **Frontend:** React Native + Expo
- **OCR Engine:** Google ML Kit Vision API or Tesseract.js
- **Dictionary API:** Jisho API or JMDict database
- **Language:** JavaScript/TypeScript
- **Camera:** expo-camera
- **Storage:** AsyncStorage for history

**Estimated Complexity:** Medium

---

### Option 2: Web Application (Progressive Web App)
**Best for:** Cross-platform accessibility, no installation required

**Pros:**
- Works on any device with a browser
- No app store approval needed
- Easy to update and maintain
- Can be installed as PWA

**Tech Stack:**
- **Frontend:** React or Vue.js
- **OCR Engine:** Tesseract.js
- **Dictionary API:** Jisho API
- **Language:** JavaScript/TypeScript
- **Camera:** MediaDevices API (getUserMedia)
- **Storage:** IndexedDB for offline support

**Estimated Complexity:** Medium-Low

---

### Option 3: Desktop Application (Python + GUI)
**Best for:** Integration with desktop workflows, local processing

**Pros:**
- Fast local processing
- No internet required for OCR (if using local models)
- Easy to integrate with existing Python tools
- Good for development and prototyping

**Tech Stack:**
- **GUI Framework:** PyQt6 or Tkinter
- **OCR Engine:** Tesseract (pytesseract) with Japanese language pack
- **Dictionary:** Local JMDict database or Jisho API
- **Language:** Python 3.11+
- **Camera:** OpenCV (cv2)
- **Image Processing:** Pillow (PIL)

**Estimated Complexity:** Medium

---

### Option 4: Cross-Platform Desktop App (Electron)
**Best for:** Desktop users wanting native app experience

**Pros:**
- Native desktop feel with web technologies
- Cross-platform (Windows, macOS, Linux)
- Rich UI capabilities
- Large ecosystem

**Tech Stack:**
- **Framework:** Electron
- **Frontend:** React/Vue
- **OCR Engine:** Tesseract.js
- **Dictionary API:** Jisho API
- **Language:** JavaScript/TypeScript
- **Camera:** WebRTC

**Estimated Complexity:** Medium-High

## Recommended Approach: Python Desktop MVP

For rapid development and proof of concept, I recommend starting with **Option 3 (Python Desktop Application)**:

### Why Python First?
1. **Fastest to implement** - Quick prototyping and iteration
2. **Excellent OCR libraries** - Tesseract is mature and well-documented
3. **Easy testing** - Can validate OCR accuracy before committing to platform
4. **Low barrier to entry** - Pure Python, no app store requirements
5. **Path to migration** - Can later port to mobile/web once proven

## Proposed Repository Structure

```
kanji-ocr-app/
├── README.md                 # This file
├── .gitignore               # Python, IDE, OS files
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
├── docs/                    # Documentation
│   ├── setup.md            # Setup instructions
│   ├── usage.md            # User guide
│   └── api.md              # API documentation
├── src/                     # Source code
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── gui/                # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py  # Main application window
│   │   ├── camera_view.py  # Camera capture interface
│   │   └── result_view.py  # OCR results display
│   ├── ocr/                # OCR processing
│   │   ├── __init__.py
│   │   ├── processor.py    # OCR processing logic
│   │   └── preprocessor.py # Image preprocessing
│   ├── dictionary/         # Dictionary lookup
│   │   ├── __init__.py
│   │   ├── jisho_api.py   # Jisho API client
│   │   └── cache.py       # Cache for lookups
│   └── utils/              # Utilities
│       ├── __init__.py
│       ├── config.py       # Configuration
│       └── logger.py       # Logging setup
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_ocr.py
│   └── test_dictionary.py
├── assets/                  # Application assets
│   ├── icons/
│   └── sample_images/      # Test images
└── scripts/                 # Utility scripts
    ├── install_tesseract.sh
    └── download_language_pack.sh
```

## Implementation Plan

### Phase 1: Core OCR Functionality (Week 1)
- [x] Set up project structure
- [ ] Install and configure Tesseract OCR
- [ ] Implement basic image capture/upload
- [ ] Implement OCR processing for Japanese text
- [ ] Create simple CLI interface for testing

### Phase 2: GUI Development (Week 2)
- [ ] Design main application window
- [ ] Implement camera view with capture button
- [ ] Add image preview and crop functionality
- [ ] Display OCR results with character highlighting

### Phase 3: Dictionary Integration (Week 3)
- [ ] Integrate Jisho API or JMDict database
- [ ] Implement kanji lookup functionality
- [ ] Display meanings, readings, and stroke order
- [ ] Add cache for offline/fast lookups

### Phase 4: Enhancement & Polish (Week 4)
- [ ] Add search history
- [ ] Implement favorites/saved kanji list
- [ ] Add export functionality (Anki, CSV)
- [ ] Improve OCR accuracy with preprocessing
- [ ] Add error handling and user feedback

### Phase 5: Optional - Platform Migration
- [ ] Evaluate user feedback
- [ ] Consider mobile app (React Native)
- [ ] Or web app (PWA) version
- [ ] Maintain feature parity

## Key Dependencies

### Python Desktop Version
```
pytesseract>=0.3.10          # OCR engine wrapper
opencv-python>=4.8.0         # Image capture and processing
Pillow>=10.0.0               # Image manipulation
PyQt6>=6.5.0                 # GUI framework (or tkinter - built-in)
requests>=2.31.0             # API calls to Jisho
beautifulsoup4>=4.12.0       # HTML parsing if needed
```

### System Requirements
- **Tesseract OCR** 5.0+ with Japanese language pack (jpn.traineddata)
- **Python** 3.11+
- **Camera** or ability to upload images

## Data Sources

### OCR Engine
- **Tesseract OCR**: Open-source, supports Japanese (jpn, jpn_vert)
  - Download: https://github.com/tesseract-ocr/tesseract
  - Language packs: https://github.com/tesseract-ocr/tessdata

### Dictionary APIs
1. **Jisho API** (Recommended)
   - Free, no API key required
   - Endpoint: `https://jisho.org/api/v1/search/words?keyword={kanji}`
   - Rich data: meanings, readings, JLPT level, frequency

2. **JMDict** (Alternative - Offline)
   - Free, downloadable XML/JSON
   - Comprehensive Japanese-English dictionary
   - Requires local database setup

3. **Kanji Alive API**
   - Kanji details including stroke order
   - Free with attribution

## Questions for User Decision

Before we proceed with implementation, please decide:

### 1. Platform Preference
- **A) Desktop App (Python)** - Fastest development, great for MVP ✓ RECOMMENDED
- **B) Mobile App (React Native)** - Most practical for real-world use
- **C) Web App (PWA)** - Most accessible, works everywhere
- **D) Cross-platform Electron** - Desktop with web tech

### 2. Dictionary Preference
- **A) Jisho API** - Online, rich data, requires internet ✓ RECOMMENDED
- **B) JMDict Local** - Offline, requires setup
- **C) Both** - Best of both worlds

### 3. Advanced Features (Priority)
Which features are most important?
- **A) Accuracy** - Best OCR recognition, even if slower
- **B) Speed** - Fast recognition, acceptable accuracy
- **C) Offline capability** - Works without internet
- **D) Learning tools** - Flashcards, history, export to Anki

### 4. User Experience
- **A) Simple** - Just show kanji and meaning
- **B) Detailed** - Include readings, examples, stroke order, JLPT level
- **C) Educational** - Add study features, quizzes, progress tracking

## Next Steps

1. **User decides on platform and features** (see questions above)
2. **Set up development environment** (install Tesseract, Python dependencies)
3. **Create initial prototype** with basic OCR
4. **Iterate based on testing** and user feedback
5. **Add dictionary integration**
6. **Polish and deploy**

## License

MIT License - Free to use and modify

## Contributing

This is a learning project. Contributions welcome!

---

**Project Status:** 🚀 Planning Phase

**Created:** December 19, 2025
