"""
Flask routes for Kanji OCR application
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta
import requests
from typing import Dict, Optional, List

bp = Blueprint('main', __name__)

# ============================================================
# Configuration Constants
# ============================================================

# Jisho API configuration
JISHO_API_BASE_URL = 'https://jisho.org/api/v1/search/words'
JISHO_API_TIMEOUT = 10  # seconds
JISHO_MAX_RESULTS = 5  # Maximum number of results to process

# Cache configuration
CACHE_TTL_SECONDS = 3600  # 1 hour cache TTL
dictionary_cache: Dict[str, dict] = {}  # In-memory cache
cache_timestamps: Dict[str, datetime] = {}  # Cache expiry tracking


def allowed_file(filename):
    """Check if uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@bp.route('/chat')
def chat():
    """Serve the Japanese chat friend page"""
    return render_template('chat.html')


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
    Look up dictionary information for a kanji character using Jisho API

    Args:
        kanji: The kanji character or word to look up

    Returns: JSON with dictionary information from Jisho API
    """
    try:
        # Fetch dictionary data from Jisho API (with caching)
        dictionary_data = fetch_jisho_dictionary(kanji)

        if dictionary_data:
            return jsonify({
                'success': True,
                'kanji': kanji,
                'data': dictionary_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No dictionary entry found for this character'
            }), 404

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


def is_cache_valid(kanji: str) -> bool:
    """
    Check if cached entry is still valid based on TTL

    Args:
        kanji: The kanji to check

    Returns:
        True if cache is valid, False otherwise
    """
    if kanji not in cache_timestamps:
        return False

    expiry_time = cache_timestamps[kanji] + timedelta(seconds=CACHE_TTL_SECONDS)
    return datetime.now() < expiry_time


def fetch_jisho_dictionary(kanji: str) -> Optional[Dict]:
    """
    Fetch dictionary information from Jisho API with caching

    Args:
        kanji: The kanji character or word to look up

    Returns:
        Dictionary information in standardized format, or None if not found
    """
    # Check cache first
    if kanji in dictionary_cache and is_cache_valid(kanji):
        current_app.logger.info(f"Cache hit for kanji: {kanji}")
        return dictionary_cache[kanji]

    # Cache miss or expired - fetch from API
    current_app.logger.info(f"Cache miss for kanji: {kanji}, fetching from Jisho API")

    try:
        # Call Jisho API
        response = requests.get(
            JISHO_API_BASE_URL,
            params={'keyword': kanji},
            timeout=JISHO_API_TIMEOUT
        )
        response.raise_for_status()

        data = response.json()

        # Parse and format the response
        formatted_data = parse_jisho_response(data, kanji)

        if formatted_data:
            # Cache the result
            dictionary_cache[kanji] = formatted_data
            cache_timestamps[kanji] = datetime.now()
            current_app.logger.info(f"Cached dictionary data for: {kanji}")

        return formatted_data

    except requests.exceptions.Timeout:
        current_app.logger.error(f"Jisho API timeout for kanji: {kanji}")
        return None
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Jisho API request error for {kanji}: {str(e)}")
        return None
    except Exception as e:
        current_app.logger.error(f"Unexpected error fetching dictionary for {kanji}: {str(e)}")
        return None


def parse_jisho_response(api_response: Dict, search_term: str) -> Optional[Dict]:
    """
    Parse Jisho API response into standardized format

    Args:
        api_response: Raw JSON response from Jisho API
        search_term: The original search term

    Returns:
        Formatted dictionary data matching frontend expectations
    """
    if not api_response.get('data') or len(api_response['data']) == 0:
        return None

    # Get the first (most relevant) result
    primary_result = api_response['data'][0]

    # Extract Japanese readings
    japanese_data = primary_result.get('japanese', [{}])[0]
    word = japanese_data.get('word', search_term)
    reading = japanese_data.get('reading', '')

    # Extract senses (meanings)
    senses = primary_result.get('senses', [])
    meanings = []
    parts_of_speech = []

    for sense in senses:
        # Get English definitions
        definitions = sense.get('english_definitions', [])
        meanings.extend(definitions)

        # Get parts of speech
        pos = sense.get('parts_of_speech', [])
        parts_of_speech.extend(pos)

    # Remove duplicates while preserving order
    meanings = list(dict.fromkeys(meanings))
    parts_of_speech = list(dict.fromkeys(parts_of_speech))

    # Extract JLPT level from tags
    jlpt_level = 'Unknown'
    tags = primary_result.get('tags', [])
    for tag in tags:
        if tag.startswith('JLPT N'):
            jlpt_level = tag.replace('JLPT ', '')
            break

    # Check for common tags
    is_common = primary_result.get('is_common', False)

    # Extract kun and on readings (if available in tags or other fields)
    # Note: Jisho API doesn't always separate kun/on readings explicitly
    # We'll use the reading field as a general reading
    kun_reading = reading if reading else '—'
    on_reading = '—'  # Jisho doesn't separate this clearly in API

    # Build examples from additional results
    examples = []
    for i, result in enumerate(api_response['data'][:JISHO_MAX_RESULTS]):
        if i == 0:
            continue  # Skip the primary result

        jp = result.get('japanese', [{}])[0]
        example_word = jp.get('word', '')
        example_reading = jp.get('reading', '')

        if example_word and example_word != word:
            # Get first meaning from senses
            example_senses = result.get('senses', [])
            example_meaning = ''
            if example_senses and example_senses[0].get('english_definitions'):
                example_meaning = example_senses[0]['english_definitions'][0]

            examples.append({
                'word': example_word,
                'reading': example_reading,
                'meaning': example_meaning
            })

    # Format the final response to match frontend expectations
    return {
        'meanings': meanings[:10],  # Limit to 10 meanings
        'kun_reading': kun_reading,
        'on_reading': on_reading,
        'jlpt_level': jlpt_level,
        'parts_of_speech': ', '.join(parts_of_speech[:5]),  # Limit to 5
        'is_common': is_common,
        'stroke_count': 0,  # Jisho API doesn't provide stroke count
        'examples': examples[:5],  # Limit to 5 examples
        'source': 'Jisho.org API'
    }


@bp.route("/api/chat", methods=["POST"])
def chat_message():
    """
    Handle chat messages from the Japanese chat friend interface
    
    Expected: JSON with "message" field
    Returns: JSON with "response" field
    
    TODO: Integrate real LLM API (OpenAI, Anthropic, etc.)
    """
    try:
        data = request.get_json()
        
        if not data or "message" not in data:
            return jsonify({
                "success": False,
                "error": "No message provided"
            }), 400
        
        user_message = data["message"]
        
        # TODO: Call LLM API here
        # For now, return a placeholder response
        bot_response = generate_placeholder_response(user_message)
        
        return jsonify({
            "success": True,
            "response": bot_response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to process chat message"
        }), 500


def generate_placeholder_response(message: str) -> str:
    """
    Generate a placeholder response for chat messages
    
    TODO: Replace with real LLM integration
    - Add OpenAI/Anthropic/etc. API calls
    - Configure system prompt for Japanese practice
    - Handle conversation context/history
    
    Args:
        message: The user's message
        
    Returns:
        A placeholder response in Japanese
    """
    # Simple placeholder responses
    responses = [
        f"こんにちは！「{message}」と言いましたね。",
        f"面白いですね！「{message}」について、もっと教えてください。",
        f"なるほど！「{message}」ですか。",
        "すみません、今はプレースホルダーモードです。LLM APIキーを設定してください。",
    ]
    
    import random
    return random.choice(responses)

