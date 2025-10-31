"""
File: __init__.py
Path: app/__init__.py
Purpose: Flask application initialization and configuration
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31
"""

from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    """
    Create and configure the Flask application instance.

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DATABASE'] = os.getenv('DATABASE_PATH', 'data/roach_tracker.db')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Ensure required directories exist
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('exports', exist_ok=True)

    # Import and register routes
    from app.main import register_routes
    register_routes(app)

    return app
