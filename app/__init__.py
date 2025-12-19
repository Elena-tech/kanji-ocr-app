"""
Flask application factory for Kanji OCR app
"""

from flask import Flask
import os


def create_app(config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)

    # Default configuration
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads'),
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif', 'webp'}
    )

    # Override with custom config if provided
    if config:
        app.config.update(config)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app
