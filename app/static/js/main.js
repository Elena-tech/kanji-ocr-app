/**
 * Kanji OCR Camera - Frontend JavaScript
 * Vanilla JS implementation for image upload and OCR processing
 */

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const selectFileBtn = document.getElementById('selectFileBtn');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const processBtn = document.getElementById('processBtn');
const clearBtn = document.getElementById('clearBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const dictionarySection = document.getElementById('dictionarySection');
const errorMessage = document.getElementById('errorMessage');
const detectedText = document.getElementById('detectedText');
const charactersGrid = document.getElementById('charactersGrid');
const processingInfo = document.getElementById('processingInfo');
const dictionaryContent = document.getElementById('dictionaryContent');

// State
let selectedFile = null;
let ocrResults = null;

/**
 * Initialize event listeners
 */
function init() {
    // File selection button
    selectFileBtn.addEventListener('click', () => fileInput.click());

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());

    // Process button
    processBtn.addEventListener('click', processImage);

    // Clear button
    clearBtn.addEventListener('click', clearSelection);

    console.log('Kanji OCR Camera initialized');
}

/**
 * Handle drag over event
 */
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('dragover');
}

/**
 * Handle drag leave event
 */
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');
}

/**
 * Handle drop event
 */
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (isValidImageFile(file)) {
            handleFile(file);
        } else {
            showError('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WebP).');
        }
    }
}

/**
 * Handle file selection from input
 */
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

/**
 * Validate image file type
 */
function isValidImageFile(file) {
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'];
    return validTypes.includes(file.type);
}

/**
 * Handle selected file
 */
function handleFile(file) {
    if (!isValidImageFile(file)) {
        showError('Invalid file type. Please upload an image.');
        return;
    }

    selectedFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        hideError();
        hideResults();
    };
    reader.readAsDataURL(file);
}

/**
 * Clear file selection
 */
function clearSelection() {
    selectedFile = null;
    fileInput.value = '';
    imagePreview.src = '';
    uploadArea.style.display = 'block';
    previewSection.style.display = 'none';
    hideResults();
    hideError();
}

/**
 * Process image - send to backend for OCR
 */
async function processImage() {
    if (!selectedFile) {
        showError('No image selected');
        return;
    }

    // Show loading
    showLoading();
    hideError();
    hideResults();

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('image', selectedFile);

        // Send to backend
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            ocrResults = data.ocr_results;
            displayResults(data);
        } else {
            showError(data.error || 'Failed to process image');
        }
    } catch (error) {
        console.error('Error processing image:', error);
        showError('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Display OCR results
 */
function displayResults(data) {
    const results = data.ocr_results;

    // Display detected text
    detectedText.textContent = results.detected_text || 'No text detected';

    // Display characters
    displayCharacters(results.characters || []);

    // Display processing info
    displayProcessingInfo(results);

    // Show results section
    resultsSection.style.display = 'block';
}

/**
 * Display individual characters
 */
function displayCharacters(characters) {
    charactersGrid.innerHTML = '';

    characters.forEach(char => {
        const card = createCharacterCard(char);
        charactersGrid.appendChild(card);
    });
}

/**
 * Create character card element
 */
function createCharacterCard(char) {
    const card = document.createElement('div');
    card.className = 'character-card';
    card.onclick = () => lookupKanji(char.character);

    const display = document.createElement('div');
    display.className = 'character-display';
    display.textContent = char.character;

    const confidence = document.createElement('div');
    confidence.className = 'character-confidence';
    confidence.textContent = `Confidence: ${(char.confidence * 100).toFixed(1)}%`;

    const confidenceBar = document.createElement('div');
    confidenceBar.className = 'confidence-bar';

    const confidenceFill = document.createElement('div');
    confidenceFill.className = 'confidence-fill';
    confidenceFill.style.width = `${char.confidence * 100}%`;

    confidenceBar.appendChild(confidenceFill);

    card.appendChild(display);
    card.appendChild(confidence);
    card.appendChild(confidenceBar);

    return card;
}

/**
 * Display processing information
 */
function displayProcessingInfo(results) {
    processingInfo.innerHTML = `
        <strong>Processing Details:</strong><br>
        Language: ${results.language || 'Unknown'}<br>
        Processing Time: ${results.processing_time_ms || 0}ms<br>
        ${results.note ? `<em>${results.note}</em>` : ''}
    `;
}

/**
 * Look up kanji in dictionary
 */
async function lookupKanji(kanji) {
    showLoading();
    hideError();

    try {
        const response = await fetch(`/api/lookup/${encodeURIComponent(kanji)}`);
        const data = await response.json();

        if (response.ok && data.success) {
            displayDictionary(kanji, data.data);
        } else {
            showError(data.error || 'Failed to lookup kanji');
        }
    } catch (error) {
        console.error('Error looking up kanji:', error);
        showError('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Display dictionary information
 */
function displayDictionary(kanji, data) {
    dictionaryContent.innerHTML = `
        <div class="dictionary-entry">
            <div class="kanji-large">${kanji}</div>

            <div class="dictionary-field">
                <div class="dictionary-label">Meanings:</div>
                <div class="dictionary-value">${data.meanings.join(', ')}</div>
            </div>

            <div class="dictionary-field">
                <div class="dictionary-label">Kun Reading (訓読み):</div>
                <div class="dictionary-value">${data.kun_reading}</div>
            </div>

            <div class="dictionary-field">
                <div class="dictionary-label">On Reading (音読み):</div>
                <div class="dictionary-value">${data.on_reading}</div>
            </div>

            <div class="dictionary-field">
                <div class="dictionary-label">JLPT Level:</div>
                <div class="dictionary-value">${data.jlpt_level}</div>
            </div>

            <div class="dictionary-field">
                <div class="dictionary-label">Stroke Count:</div>
                <div class="dictionary-value">${data.stroke_count}</div>
            </div>

            ${data.examples && data.examples.length > 0 ? `
                <div class="dictionary-field">
                    <div class="dictionary-label">Example Words:</div>
                    <ul class="examples-list">
                        ${data.examples.map(ex => `
                            <li>
                                <span class="example-word">${ex.word}</span>
                                <span class="example-reading">(${ex.reading})</span>
                                - <span class="example-meaning">${ex.meaning}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            ` : ''}

            ${data.note ? `<p style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.875rem;"><em>${data.note}</em></p>` : ''}
        </div>
    `;

    dictionarySection.style.display = 'block';
    dictionarySection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show loading indicator
 */
function showLoading() {
    loadingIndicator.style.display = 'block';
    processBtn.disabled = true;
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    loadingIndicator.style.display = 'none';
    processBtn.disabled = false;
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
}

/**
 * Hide results sections
 */
function hideResults() {
    resultsSection.style.display = 'none';
    dictionarySection.style.display = 'none';
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', init);

// TODO: Future enhancements
// - Add camera capture using getUserMedia API
// - Add image cropping/editing before OCR
// - Add OCR result editing (correct mistakes)
// - Add history of scanned kanji
// - Add favorites/saved kanji list
// - Add export functionality (Anki, CSV)
// - Add offline support with Service Worker
