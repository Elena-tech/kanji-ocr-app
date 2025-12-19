/**
 * Japanese Chat Friend - Frontend JavaScript
 * Handles real-time chat interactions with the AI language partner
 */

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const errorMessage = document.getElementById('errorMessage');
const chatStatus = document.getElementById('chatStatus');

// State
let isProcessing = false;

/**
 * Initialize chat functionality
 */
function init() {
    // Send button click
    sendButton.addEventListener('click', sendMessage);

    // Enter key to send (Shift+Enter for new line)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea as user types
    messageInput.addEventListener('input', autoResizeTextarea);

    console.log('Japanese Chat Friend initialized');
}

/**
 * Auto-resize textarea based on content
 */
function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = messageInput.scrollHeight + 'px';
}

/**
 * Send message to the chat API
 */
async function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    if (isProcessing) {
        return;
    }

    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Add user message to chat
    addUserMessage(message);

    // Show processing state
    isProcessing = true;
    sendButton.disabled = true;
    const typingIndicator = showTypingIndicator();

    try {
        // Call backend API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Remove typing indicator
        typingIndicator.remove();

        if (response.ok && data.success) {
            // Add bot response to chat
            addBotMessage(data.response);
        } else {
            showError(data.error || 'Failed to get response');
        }

    } catch (error) {
        console.error('Error sending message:', error);
        typingIndicator.remove();
        showError('Network error. Please try again.');
    } finally {
        isProcessing = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

/**
 * Add user message to chat
 */
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';

    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${escapeHtml(text)}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
        <div class="message-avatar">👤</div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add bot message to chat
 */
function addBotMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(text)}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typingIndicator';

    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    chatMessages.appendChild(typingDiv);
    scrollToBottom();

    return typingDiv;
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Get current time formatted
 */
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
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

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', init);

// TODO: Future enhancements
// - Add conversation history persistence
// - Add message editing/deletion
// - Add export chat functionality
// - Add voice input/output
// - Add translation toggle
// - Add grammar correction highlights
// - Add vocabulary learning mode
