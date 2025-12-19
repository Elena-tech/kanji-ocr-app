#!/usr/bin/env python3
"""
Development server entry point for Kanji OCR app
Run with: python run.py or flask run
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Development server configuration
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
