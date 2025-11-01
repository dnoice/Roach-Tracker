# Development Guide

**File**: DEVELOPMENT.md
**Purpose**: Guide for developers working on Roach Tracker
**Author**: dnoice + Claude AI
**Version**: 1.0.0
**Created**: 2025-10-31
**Updated**: 2025-10-31

---

## Project Structure

```
Roach-Tracker/
├── app/                      # Main application package
│   ├── __init__.py          # Flask app factory
│   ├── main.py              # Route definitions (DO NOT run directly!)
│   ├── models.py            # Database models and operations
│   ├── auth.py              # Authentication decorators
│   ├── security.py          # Security logging and rate limiting
│   ├── validators.py        # Input validation utilities
│   └── utils.py             # Helper functions
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── profile.html        # User profile
│   └── ...                 # Other templates
├── static/                  # Static files
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript
│   └── uploads/            # Photo uploads
├── data/                    # SQLite database
│   └── roach_tracker.db    # Main database
├── exports/                 # Generated reports
├── run.py                   # Application entry point ⭐
├── create_admin.py          # Admin user creation script
├── check_setup.py           # Environment verification script
├── setup.sh                 # Setup script
├── run.sh                   # Run script (wrapper for run.py)
├── verify.sh                # Verification script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (created by setup)
└── README.md               # Main documentation
```

---

## Important: Module Import Structure

### ✅ Correct Usage

The application is designed as a **Python package** that must be imported, not run directly.

```bash
# Run from project root
cd Roach-Tracker

# Method 1: Using entry point (recommended)
python run.py

# Method 2: Using shell script
./run.sh

# Method 3: Using Flask CLI
export FLASK_APP=app
flask run
```

### ❌ Common Mistakes

```bash
# DON'T run modules directly
python app/main.py        # Will fail with import errors
python app/__init__.py    # Will fail with import errors
python app/models.py      # Will fail with import errors

# DON'T run from wrong directory
cd app
python main.py           # Wrong directory!
```

### Why This Matters

Python's import system requires:
1. The package root (`Roach-Tracker/`) must be in Python's path
2. Modules are imported as `from app import ...`
3. Running `python app/main.py` tries to import from a non-existent `app` package

---

## Development Workflow

### Initial Setup

```bash
# 1. Clone repository
git clone https://github.com/dnoice/Roach-Tracker.git
cd Roach-Tracker

# 2. Run setup (creates venv, installs dependencies)
./setup.sh

# 3. Verify environment
python check_setup.py

# 4. Create admin user
python create_admin.py

# 5. Run application
python run.py
```

### Making Changes

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 2. Make your changes to code

# 3. Test imports work
python -c "from app import create_app; print('OK')"

# 4. Run application
python run.py --debug

# 5. Run in background for testing
python run.py &

# 6. Check syntax
python -m py_compile app/*.py

# 7. Deactivate when done
deactivate
```

### Adding New Routes

Edit `app/main.py` within the `register_routes()` function:

```python
def register_routes(app):
    # ... existing code ...

    @app.route('/new-route')
    @login_required  # Add authentication if needed
    def new_view():
        """Your new view function."""
        return render_template('new_template.html')
```

### Adding New Models

Edit `app/models.py` within the `Database` class:

```python
class Database:
    # ... existing code ...

    def new_method(self, param: str) -> int:
        """
        Description of what this method does.

        Args:
            param: Description

        Returns:
            int: Description

        Raises:
            ValueError: Description
        """
        # Your code here
```

---

## Entry Points Explained

### `run.py` (Primary Entry Point)

```python
# Full-featured entry point with CLI options
python run.py --host 0.0.0.0 --port 8000 --debug
```

**Features**:
- Command-line argument parsing
- Environment variable support
- Debug mode toggle
- Graceful error handling
- Startup information display

### `run.sh` (Shell Script Wrapper)

```bash
# Activates venv and runs application
./run.sh
```

**Features**:
- Automatic venv activation
- Environment variable loading
- Configuration validation
- User-friendly output

### Flask CLI

```bash
# Standard Flask command-line interface
export FLASK_APP=app
flask run
```

**Features**:
- Standard Flask tooling
- Development server
- Debug mode support

---

## Testing

### Manual Testing

```bash
# 1. Start application
python run.py --debug

# 2. Test in browser
open http://localhost:5000

# 3. Test API endpoints
curl http://localhost:5000/login
```

### Import Testing

```bash
# Test all imports work
python -c "from app import create_app; create_app()"
python -c "from app.models import Database"
python -c "from app.auth import admin_required"
python -c "from app.security import log_security_event"
python -c "from app.validators import validate_email"
```

### Database Testing

```bash
# Check database
sqlite3 data/roach_tracker.db ".tables"
sqlite3 data/roach_tracker.db "SELECT * FROM users"
sqlite3 data/roach_tracker.db "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 10"
```

---

## Debugging

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solutions**:
```bash
# 1. Check you're in the right directory
pwd  # Should show .../Roach-Tracker

# 2. Check you're running from project root
ls  # Should see app/, templates/, run.py

# 3. Don't run modules directly
python run.py  # ✓ Correct
python app/main.py  # ✗ Wrong
```

### Flask Not Found

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solutions**:
```bash
# 1. Run setup
./setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies manually
pip install -r requirements.txt
```

### Database Errors

**Problem**: `sqlite3.OperationalError: no such table`

**Solutions**:
```bash
# 1. Delete database and restart
rm data/roach_tracker.db
python run.py  # Will recreate tables

# 2. Check migrations ran
python -c "from app.models import Database; Database('data/roach_tracker.db')"
```

---

## Code Style

### Python Style

- Follow PEP 8
- Use type hints
- Write comprehensive docstrings
- Handle exceptions specifically

```python
def example_function(param: str) -> int:
    """
    Brief description.

    Args:
        param: Parameter description

    Returns:
        int: Return value description

    Raises:
        ValueError: When validation fails
    """
    if not param:
        raise ValueError("Parameter required")
    return len(param)
```

### Import Order

```python
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Third-party
from flask import Flask, render_template
from flask_login import login_required

# 3. Local
from app.models import Database
from app.auth import admin_required
```

---

## Environment Variables

### `.env` File

```bash
# Flask configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_PATH=data/roach_tracker.db

# Server
HOST=0.0.0.0
PORT=5000

# File uploads
UPLOAD_FOLDER=static/uploads
```

### Loading Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('SECRET_KEY', 'default-value')
```

---

## Production Deployment

### Security Checklist

- [ ] Generate strong `SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Use HTTPS
- [ ] Configure firewall
- [ ] Set up log rotation
- [ ] Configure backup
- [ ] Review security settings

### Running in Production

```bash
# Using gunicorn (recommended)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Using run.py
python run.py --no-debug --host 0.0.0.0 --port 5000
```

---

## Troubleshooting Common Issues

### Issue: "This file should not be run directly"

**Cause**: Trying to run `app/main.py` or other modules directly

**Solution**: Use the proper entry point
```bash
python run.py  # From project root
```

### Issue: Import errors when running tests

**Cause**: Not in project root or venv not activated

**Solution**:
```bash
cd Roach-Tracker  # Go to project root
source venv/bin/activate  # Activate venv
python run.py  # Run
```

### Issue: Rate limiting triggering during development

**Cause**: Multiple failed login attempts

**Solution**: Restart application to reset rate limiter (in-memory)

---

## Contributing

### Before Submitting

1. Test all entry points work
2. Verify imports from project root
3. Run syntax check: `python -m py_compile app/*.py`
4. Check code follows style guide
5. Update documentation

### Golden Rules

1. Unified metadata headers in all files
2. No box-drawing characters
3. Rich terminal output
4. SVG graphics in UI (no emoji)
5. Design for elegance and robustness
6. Dual-mode UX (beginner + power user)
7. Document as you build
8. No hardcoded secrets
9. Fail gracefully with beautiful logging
10. Consistency over cleverness

---

## Resources

- **Main Docs**: README.md
- **Authentication**: AUTHENTICATION.md
- **Security**: SECURITY_ENHANCEMENTS.md
- **Architecture**: ARCHITECTURE.md
- **Flask Docs**: https://flask.palletsprojects.com/
- **Flask-Login**: https://flask-login.readthedocs.io/

---

**Last Updated**: 2025-10-31
**Maintainers**: dnoice + Claude AI
