"""
Flask routes for Kanji OCR application
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

bp = Blueprint('main', __name__)


def allowed_file(filename):
    """Check if uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'kanji-ocr-api',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })


@bp.route('/api/upload', methods=['POST'])
def upload_image():
    """
    Handle image upload for OCR processing

    Expected: multipart/form-data with 'image' file
    Returns: JSON with OCR results

    TODO: Integrate real Tesseract OCR
    """
    # Validate request
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image file provided'
        }), 400

    file = request.files['image']

    # Validate filename
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'Invalid file type. Allowed: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}'
        }), 400

    try:
        # Save uploaded file with unique name
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # TODO: Perform actual OCR processing here
        # For now, return stubbed data
        ocr_results = perform_ocr_stub(filepath)

        return jsonify({
            'success': True,
            'filename': original_filename,
            'ocr_results': ocr_results,
            'message': 'Image processed successfully (using stub data)'
        })

    except Exception as e:
        current_app.logger.error(f"Error processing upload: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to process image'
        }), 500


@bp.route('/api/lookup/<kanji>', methods=['GET'])
def lookup_kanji(kanji):
    """
    Look up dictionary information for a kanji character

    Args:
        kanji: The kanji character to look up

    Returns: JSON with dictionary information

    TODO: Integrate real dictionary API (Jisho or JMDict)
    """
    try:
        # TODO: Call real dictionary API
        # For now, return stubbed data
        dictionary_data = get_dictionary_stub(kanji)

        return jsonify({
            'success': True,
            'kanji': kanji,
            'data': dictionary_data
        })

    except Exception as e:
        current_app.logger.error(f"Error looking up kanji {kanji}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to lookup kanji'
        }), 500


def perform_ocr_stub(filepath):
    """
    Stub function for OCR processing

    TODO: Replace with real Tesseract OCR implementation
    - Install pytesseract
    - Load Japanese language pack (jpn.traineddata)
    - Preprocess image (grayscale, contrast, etc.)
    - Run OCR with Japanese language mode
    - Parse and return recognized characters

    Args:
        filepath: Path to the uploaded image

    Returns:
        List of recognized kanji with confidence scores
    """
    # Stubbed kanji recognition results
    return {
        'detected_text': '日本語',
        'characters': [
            {
                'character': '日',
                'confidence': 0.95,
                'position': {'x': 10, 'y': 20, 'width': 50, 'height': 50}
            },
            {
                'character': '本',
                'confidence': 0.92,
                'position': {'x': 70, 'y': 20, 'width': 50, 'height': 50}
            },
            {
                'character': '語',
                'confidence': 0.89,
                'position': {'x': 130, 'y': 20, 'width': 50, 'height': 50}
            }
        ],
        'language': 'Japanese',
        'processing_time_ms': 123,
        'note': 'This is stubbed OCR data. Real Tesseract integration pending.'
    }


def get_dictionary_stub(kanji):
    """
    Stub function for dictionary lookup

    TODO: Replace with real dictionary API integration
    - Option 1: Jisho API (https://jisho.org/api/v1/search/words?keyword={kanji})
    - Option 2: Local JMDict database
    - Include: meanings, readings (kun-yomi, on-yomi), JLPT level, examples

    Args:
        kanji: The kanji character to look up

    Returns:
        Dictionary information for the kanji
    """
    # Stubbed dictionary data
    stub_data = {
        '日': {
            'meanings': ['sun', 'day'],
            'kun_reading': 'ひ, か',
            'on_reading': 'ニチ, ジツ',
            'jlpt_level': 'N5',
            'stroke_count': 4,
            'examples': [
                {'word': '日本', 'reading': 'にほん', 'meaning': 'Japan'},
                {'word': '毎日', 'reading': 'まいにち', 'meaning': 'every day'}
            ]
        },
        '本': {
            'meanings': ['book', 'origin', 'main'],
            'kun_reading': 'もと',
            'on_reading': 'ホン',
            'jlpt_level': 'N5',
            'stroke_count': 5,
            'examples': [
                {'word': '日本', 'reading': 'にほん', 'meaning': 'Japan'},
                {'word': '本当', 'reading': 'ほんとう', 'meaning': 'truth, really'}
            ]
        },
        '語': {
            'meanings': ['language', 'word'],
            'kun_reading': 'かたる, かたらう',
            'on_reading': 'ゴ',
            'jlpt_level': 'N4',
            'stroke_count': 14,
            'examples': [
                {'word': '日本語', 'reading': 'にほんご', 'meaning': 'Japanese language'},
                {'word': '英語', 'reading': 'えいご', 'meaning': 'English language'}
            ]
        }
    }

    # Return stub data for known kanji, or generic data for unknown
    if kanji in stub_data:
        return stub_data[kanji]
    else:
        return {
            'meanings': ['(Dictionary lookup pending)'],
            'kun_reading': '—',
            'on_reading': '—',
            'jlpt_level': 'Unknown',
            'stroke_count': 0,
            'examples': [],
            'note': 'This is stubbed dictionary data. Real API integration pending.'
        }
