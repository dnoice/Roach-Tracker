"""
File: __init__.py
Path: app/__init__.py
Purpose: Flask application initialization and configuration
Author: dnoice + Claude AI
Version: 1.1.0
Created: 2025-10-31
Updated: 2025-10-31
"""

from flask import Flask
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask-Login
login_manager = LoginManager()


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
    secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Warn if using default secret key (security check)
    if secret_key == 'dev-secret-key-change-in-production' and os.getenv('FLASK_ENV') == 'production':
        import warnings
        warnings.warn(
            'Using default SECRET_KEY in production! Set a secure SECRET_KEY in .env',
            SecurityWarning,
            stacklevel=2
        )

    app.config['SECRET_KEY'] = secret_key
    app.config['DATABASE'] = os.getenv('DATABASE_PATH', 'data/roach_tracker.db')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Ensure required directories exist
    db_dir = os.path.dirname(app.config['DATABASE'])
    if db_dir:  # Only create if there's actually a directory component
        os.makedirs(db_dir, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('exports', exist_ok=True)

    # Configure Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        from app.models import Database, User
        db = Database(app.config['DATABASE'])
        try:
            user_data = db.get_user_by_id(int(user_id))
            if user_data and user_data.get('is_active'):
                return User(user_data)
        except (ValueError, TypeError):
            pass
        return None

    # Import and register routes
    from app.main import register_routes
    register_routes(app)

    return app
