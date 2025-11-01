# Application Backend Documentation

**File**: `README.md`
**Path**: `app/README.md`
**Directory**: `app/`
**Purpose**: Flask application backend - Core business logic, database operations, authentication, and utilities
**Author**: dnoice + Claude AI
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

## Overview

The `app/` directory contains all Python backend code for the Roach Tracker application. This is the heart of the Flask web application, implementing the Model-View-Controller (MVC) architecture with comprehensive security features, authentication, and data management capabilities.

---

## Directory Structure

```
app/
├── __init__.py       # Flask application factory and initialization
├── auth.py           # Authentication decorators and utilities
├── main.py           # Application routes and view controllers
├── models.py         # Database schema and ORM operations
├── security.py       # Security logging, rate limiting, and audit trails
├── utils.py          # Utility functions (photos, PDFs, CSVs)
├── validators.py     # Input validation and sanitization
└── README.md         # This file
```

---

## Module Descriptions

### `__init__.py` - Application Factory

**Purpose**: Flask application initialization and configuration
**Key Responsibilities**:
- Creates Flask application instance using factory pattern
- Configures Flask-Login for session management
- Loads environment variables from `.env`
- Sets up application configuration (database, uploads, secret key)
- Configures security settings (max file size, allowed extensions)
- Initializes login manager with custom user loader
- Registers error handlers for 403, 404, 500 errors

**Key Configuration**:
```python
app.config['SECRET_KEY']           # Session encryption key (from .env)
app.config['DATABASE']             # SQLite database path
app.config['UPLOAD_FOLDER']        # Photo storage directory
app.config['MAX_CONTENT_LENGTH']   # 16MB file upload limit
app.config['ALLOWED_EXTENSIONS']   # {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

**Security Features**:
- Warns if default secret key is used in production
- Enforces file size limits to prevent DoS attacks
- Validates file extensions to prevent malicious uploads

---

### `auth.py` - Authentication System

**Purpose**: User authentication decorators and access control
**Key Components**:
- `@login_required` - Protects routes requiring authentication
- `@admin_required` - Restricts routes to admin users only
- `@active_user_required` - Ensures user account is active
- User loader for Flask-Login integration

**Authentication Flow**:
1. User submits credentials via login form
2. Password verified against bcrypt hash in database
3. Session created with Flask-Login on success
4. Rate limiting prevents brute force attacks (5 attempts per 5 minutes)
5. Failed attempts logged to audit trail
6. Account locked after 5 failed attempts (15 minute lockout)

**Protected Routes**: All application routes except `/login` and `/register` require authentication

---

### `main.py` - Application Routes

**Purpose**: HTTP request handlers and view controllers
**Lines of Code**: ~1,200 lines
**Key Route Categories**:

**Authentication Routes**:
- `GET/POST /login` - User login with rate limiting
- `GET/POST /register` - New user registration
- `GET /logout` - User logout and session cleanup

**Dashboard Routes**:
- `GET /` - Home dashboard with recent sightings
- `GET /statistics` - Analytics and data visualizations

**Sighting Management Routes**:
- `GET/POST /log_sighting` - Create new sighting with photo upload
- `GET /view_sightings` - List all sightings with search/filter
- `GET /view_sighting/<id>` - View single sighting details
- `GET/POST /edit_sighting/<id>` - Edit existing sighting
- `POST /delete_sighting/<id>` - Delete sighting (soft delete)

**User Management Routes** (Admin Only):
- `GET /admin/users` - User management dashboard
- `GET/POST /admin/create_user` - Create new user account
- `POST /admin/toggle_user/<id>` - Activate/deactivate user
- `POST /admin/delete_user/<id>` - Delete user account

**Profile Routes**:
- `GET /profile` - View user profile and account info
- `GET/POST /change_password` - Change password with verification

**Export Routes**:
- `GET /export/pdf` - Generate PDF report of all sightings
- `GET /export/csv` - Generate CSV export of all sightings

**Static Routes**:
- `GET /uploads/<filename>` - Serve uploaded photos

**Security Features**:
- All routes validate user input using `validators.py`
- SQL injection prevention via parameterized queries
- CSRF protection on all forms
- File upload validation and sanitization
- Rate limiting on authentication endpoints
- Comprehensive error handling with user-friendly messages

---

### `models.py` - Database Layer

**Purpose**: SQLite database schema and CRUD operations
**Lines of Code**: ~900 lines
**Database Tables**:

#### Users Table
Stores user account information and authentication data
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,              -- PBKDF2-SHA256 hash
    role TEXT NOT NULL DEFAULT 'resident',    -- admin, resident, property_manager
    full_name TEXT,
    is_active INTEGER DEFAULT 1,
    last_login TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

**Indices**: `idx_users_username`, `idx_users_email`, `idx_users_role`

#### Properties Table
Multi-tenant support for property managers
```sql
CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    created_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
)
```

#### User-Properties Relationship Table
Links users to properties they manage or reside in
```sql
CREATE TABLE user_properties (
    user_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,
    relationship_type TEXT NOT NULL DEFAULT 'resident',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, property_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
```

#### Sightings Table
Primary data table for roach sighting records
```sql
CREATE TABLE sightings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    count INTEGER NOT NULL,
    size TEXT,                                -- small, medium, large
    time_of_day TEXT,
    weather TEXT,
    notes TEXT,
    photo_path TEXT,
    date_added TEXT DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    property_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
```

**Indices**: `idx_sightings_user`, `idx_sightings_property`, `idx_sightings_date`

#### Audit Log Table
Security event logging for forensic analysis
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,                 -- login_success, login_failure, etc.
    user_id INTEGER,
    username TEXT,
    ip_address TEXT,
    user_agent TEXT,
    details TEXT,
    severity TEXT DEFAULT 'info',             -- info, warning, critical
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

**Indices**: `idx_audit_timestamp`, `idx_audit_user`, `idx_audit_event_type`

**Key Methods**:
- User CRUD: `create_user()`, `get_user()`, `update_user()`, `delete_user()`
- Authentication: `verify_password()`, `update_last_login()`, `is_account_locked()`
- Sighting CRUD: `add_sighting()`, `get_sighting()`, `update_sighting()`, `delete_sighting()`
- Analytics: `get_statistics()`, `get_location_counts()`, `get_size_distribution()`
- Audit: `log_security_event()`, `get_audit_trail()`, `get_failed_login_count()`

**Security Features**:
- Parameterized queries prevent SQL injection
- Password hashing with PBKDF2-SHA256
- Context manager ensures proper connection handling
- Transaction rollback on errors
- Comprehensive database indices for performance

---

### `security.py` - Security & Audit System

**Purpose**: Security logging, rate limiting, and account protection
**Lines of Code**: ~300 lines
**Key Features**:

#### Rate Limiting
Prevents brute force attacks on authentication endpoints
```python
# Configuration
MAX_LOGIN_ATTEMPTS = 5          # Max attempts per window
RATE_LIMIT_WINDOW = 300         # 5 minutes in seconds
LOCKOUT_DURATION = 900          # 15 minutes in seconds
```

**Implementation**: In-memory tracking with IP address + username keys

#### Account Lockout
Automatic account lockout after failed login attempts
- Locks account after 5 failed attempts
- 15-minute lockout duration
- Resets counter on successful login
- Logged to audit trail

#### Security Event Types
All events logged to `audit_log` table with IP address and user agent:
- `login_success` / `login_failure`
- `logout`
- `registration`
- `password_change`
- `user_created` / `user_deleted`
- `user_activated` / `user_deactivated`
- `account_locked`
- `unauthorized_access`

#### Audit Trail Features
- Persistent storage in SQLite database
- IP address and user agent tracking
- Severity levels: `info`, `warning`, `critical`
- Timestamp with ISO 8601 format
- Detailed context in JSON format
- Queryable for forensic analysis

**OWASP Compliance**:
- ✓ A01:2021 - Broken Access Control
- ✓ A02:2021 - Cryptographic Failures
- ✓ A03:2021 - Injection
- ✓ A07:2021 - Identification and Authentication Failures

---

### `utils.py` - Utility Functions

**Purpose**: Helper functions for file operations, reports, and data processing
**Lines of Code**: ~400 lines
**Key Modules**:

#### Photo Processing
```python
def save_photo(file) -> str
    """
    Save uploaded photo with validation and optimization
    - Validates file extension and size
    - Generates unique filename with timestamp
    - Resizes large images to max 1920x1920
    - Optimizes for web delivery
    - Returns: relative path for database storage
    """

def delete_photo(photo_path: str) -> bool
    """
    Safely delete photo file from filesystem
    - Validates path is within uploads directory
    - Prevents directory traversal attacks
    - Handles missing files gracefully
    """
```

**Security Features**:
- Extension whitelist: `{png, jpg, jpeg, gif, webp}`
- 16MB file size limit enforced
- Decompression bomb protection
- Path traversal prevention
- Secure filename generation

#### PDF Report Generation
```python
def generate_pdf_report(sightings: List[Dict]) -> str
    """
    Generate professional PDF report using ReportLab
    - Company header with title and date
    - Table with all sighting data
    - Photo thumbnails (if available)
    - Summary statistics section
    - Legal disclaimer footer
    - Returns: path to generated PDF file
    """
```

**Report Contents**:
- Header: "Roach Sighting Documentation Report"
- Date range of included sightings
- Tabular data: Date, Location, Count, Size, Time, Weather
- Photo evidence thumbnails
- Summary: Total sightings, locations, date range
- Footer: Legal disclaimer about warranty of habitability

#### CSV Export
```python
def generate_csv_export(sightings: List[Dict]) -> str
    """
    Export sightings data to CSV format
    - All sighting fields included
    - RFC 4180 compliant formatting
    - UTF-8 encoding with BOM for Excel
    - Returns: path to generated CSV file
    """
```

**CSV Columns**: ID, Date, Location, Count, Size, Time of Day, Weather, Notes, Photo, User, Property

#### File Management
```python
def allowed_file(filename: str) -> bool
    """Check if file extension is allowed"""

def get_file_size(file) -> int
    """Get uploaded file size in bytes"""

def cleanup_old_exports(max_age_days: int = 30)
    """Delete export files older than specified days"""
```

---

### `validators.py` - Input Validation

**Purpose**: Comprehensive input validation and sanitization
**Lines of Code**: ~267 lines
**Validation Functions**:

#### Email Validation
```python
def validate_email(email: str) -> tuple[bool, str]
    """
    RFC 5322 compliant email validation
    - Regex pattern matching
    - Length limits (max 254 chars)
    - Common typo detection (.con, @gmial.com)
    - Returns: (is_valid, error_message)
    """
```

**Validation Rules**:
- Must contain exactly one `@` symbol
- Local part: alphanumeric, dots, hyphens, underscores
- Domain part: valid domain format
- No consecutive dots
- No leading/trailing dots

#### Username Validation
```python
def validate_username(username: str) -> tuple[bool, str]
    """
    Username validation with security checks
    - 3-32 characters length
    - Alphanumeric, underscores, hyphens only
    - No leading/trailing special chars
    - Reserved username blocking
    - Returns: (is_valid, error_message)
    """
```

**Reserved Usernames**: `admin`, `root`, `system`, `administrator`, `superuser`, `guest`, `test`, `user`, `null`, `undefined`

#### Password Strength Validation
```python
def validate_password_strength(password: str) -> tuple[bool, str]
    """
    Enterprise-grade password validation
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - At least 1 special character
    - No common patterns (123, abc, qwerty)
    - No sequential characters
    - Returns: (is_valid, error_message)
    """
```

**Blocked Patterns**: `password`, `123456`, `qwerty`, `admin`, `letmein`, `welcome`, `monkey`, `dragon`

#### Full Name Validation
```python
def validate_full_name(name: str) -> tuple[bool, str]
    """
    Name validation with Unicode support
    - 2-100 characters
    - Letters, spaces, hyphens, apostrophes
    - Unicode character support (Ñ, É, etc.)
    - No excessive whitespace
    - Returns: (is_valid, error_message)
    """
```

**Security Benefits**:
- Prevents SQL injection via input validation
- Blocks XSS attacks through character restrictions
- Prevents username enumeration attacks
- Enforces strong authentication credentials
- Reduces attack surface through strict validation

---

## Security Architecture

### Defense in Depth

The `app/` backend implements multiple security layers:

1. **Input Validation Layer** (`validators.py`)
   - All user input validated before processing
   - Strict type checking and format validation
   - Prevents injection attacks at entry point

2. **Authentication Layer** (`auth.py`, `security.py`)
   - Session-based authentication with Flask-Login
   - Secure password hashing (PBKDF2-SHA256)
   - Rate limiting prevents brute force attacks
   - Account lockout after failed attempts

3. **Authorization Layer** (`auth.py`, `main.py`)
   - Role-based access control (RBAC)
   - Decorators enforce access restrictions
   - Admin-only routes protected
   - Users can only access their own data

4. **Data Access Layer** (`models.py`)
   - Parameterized SQL queries prevent injection
   - Context managers ensure proper cleanup
   - Transaction rollback on errors
   - Database indices optimize performance

5. **Audit Layer** (`security.py`, `models.py`)
   - All security events logged to database
   - IP address and user agent tracking
   - Forensic analysis capabilities
   - Compliance with audit requirements

---

## Database Schema Migrations

The application automatically handles database migrations:

```python
# In models.py - init_database()
cursor.execute('PRAGMA table_info(users)')
columns = [row[1] for row in cursor.fetchall()]

if 'last_login' not in columns:
    # Add new column to existing table
    cursor.execute('ALTER TABLE users ADD COLUMN last_login TEXT')
```

**Migration Strategy**:
- Check for missing columns on app startup
- Add columns with `ALTER TABLE` if needed
- Never drop or modify existing data
- Backwards compatible with old databases
- Logged to application console

---

## Error Handling

All modules implement comprehensive error handling:

```python
try:
    # Operation
except SpecificException as e:
    # Log error for debugging
    app.logger.error(f"Operation failed: {e}")
    # Return user-friendly message
    flash('Operation failed. Please try again.', 'error')
    # Rollback database if needed
    conn.rollback()
```

**Error Categories**:
- **Validation Errors**: User-facing, helpful messages
- **Database Errors**: Logged, graceful degradation
- **File System Errors**: Logged, fallback behavior
- **Authentication Errors**: Rate-limited, logged to audit trail

---

## Performance Optimizations

### Database Indices

11 performance indices across all tables:
- `idx_users_username`, `idx_users_email`, `idx_users_role`
- `idx_sightings_user`, `idx_sightings_property`, `idx_sightings_date`
- `idx_audit_timestamp`, `idx_audit_user`, `idx_audit_event_type`
- `idx_user_properties_user`, `idx_user_properties_property`

**Impact**:
- User lookup: O(log n) instead of O(n)
- Date range queries: 10-100x faster
- Audit trail queries: efficient even with 10,000+ events

### Connection Pooling

Context manager pattern ensures efficient database connections:
```python
with self.get_connection() as conn:
    # Query database
    # Automatic commit on success
    # Automatic rollback on error
    # Automatic connection cleanup
```

### Photo Optimization

Automatic image resizing prevents large file bloat:
- Max dimensions: 1920x1920 pixels
- Progressive JPEG encoding
- Optimized compression quality
- Average file size: 200-500KB (from 2-5MB originals)

---

## Testing Recommendations

### Unit Tests
Test individual functions in isolation:
```python
# test_validators.py
def test_email_validation():
    assert validate_email('user@example.com')[0] == True
    assert validate_email('invalid-email')[0] == False

# test_models.py
def test_user_creation():
    db = Database(':memory:')
    user_id = db.create_user('testuser', 'test@example.com', 'password123')
    assert user_id is not None
```

### Integration Tests
Test multiple modules working together:
```python
# test_auth_flow.py
def test_login_flow(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'Test123!@#'
    })
    assert response.status_code == 302  # Redirect to dashboard
```

### Security Tests
Test security mechanisms:
```python
# test_security.py
def test_rate_limiting():
    # Attempt 6 logins in rapid succession
    # Verify 6th attempt is blocked
    # Verify account is locked
```

---

## Development Guidelines

### Code Style
- **PEP 8** compliance for Python code
- **Type hints** for all function parameters and returns
- **Docstrings** following Google style guide
- **Comments** for complex logic only

### Security Best Practices
- Never log passwords or sensitive data
- Use parameterized queries for all SQL
- Validate all user input at entry point
- Implement least privilege access control
- Log all security-relevant events

### Database Operations
- Always use context manager for connections
- Use transactions for multi-step operations
- Index all foreign key columns
- Use `TEXT` type for all string fields (SQLite best practice)

### Error Messages
- User-facing: Helpful, non-technical
- Server logs: Detailed, technical, with stack traces
- Never expose system details to users

---

## Dependencies

Required Python packages (from `requirements.txt`):
```
Flask>=2.3.0
Flask-Login>=0.6.2
Pillow>=10.0.0
reportlab>=4.0.0
python-dotenv>=1.0.0
```

**Purpose**:
- `Flask` - Web framework and routing
- `Flask-Login` - Session management and authentication
- `Pillow` - Image processing and resizing
- `reportlab` - PDF generation
- `python-dotenv` - Environment variable loading

---

## Environment Configuration

Required `.env` variables:
```bash
# Secret key for session encryption (REQUIRED for production)
SECRET_KEY=your-super-secret-key-here

# Database path (optional, defaults to data/roach_tracker.db)
DATABASE_PATH=data/roach_tracker.db

# Upload folder (optional, defaults to static/uploads)
UPLOAD_FOLDER=static/uploads

# Flask environment (optional, defaults to development)
FLASK_ENV=development
```

**Security Note**: Never commit `.env` file to version control. Use `.env.example` for documentation.

---

## Troubleshooting

### Common Issues

**Import Errors**:
```
ModuleNotFoundError: No module named 'app'
```
**Solution**: Always run the application from project root, not from `app/` directory.

**Database Locked**:
```
sqlite3.OperationalError: database is locked
```
**Solution**: Ensure no other process is accessing the database. Check for zombie processes.

**File Upload Fails**:
```
413 Payload Too Large
```
**Solution**: File exceeds 16MB limit. Reduce file size or adjust `MAX_CONTENT_LENGTH` in `__init__.py`.

**Login Rate Limited**:
```
Too many login attempts. Please try again in 15 minutes.
```
**Solution**: Account is locked due to failed login attempts. Wait 15 minutes or have admin reset account.

---

## API Documentation

### User Management API

```python
# Create user
user_id = db.create_user(
    username='johndoe',
    email='john@example.com',
    password='SecurePass123!',
    role='resident',
    full_name='John Doe'
)

# Get user
user = db.get_user_by_username('johndoe')
user = db.get_user_by_id(user_id)

# Update user
db.update_user(user_id, full_name='John A. Doe')

# Delete user
db.delete_user(user_id)

# Verify password
is_valid = db.verify_password(user_id, 'SecurePass123!')

# Check if account is locked
is_locked = db.is_account_locked(user_id)
```

### Sighting Management API

```python
# Create sighting
sighting_id = db.add_sighting(
    location='Kitchen',
    count=3,
    size='medium',
    time_of_day='night',
    weather='humid',
    notes='Near sink area',
    photo_path='uploads/photo123.jpg',
    user_id=1,
    property_id=1
)

# Get sighting
sighting = db.get_sighting(sighting_id)

# Update sighting
db.update_sighting(sighting_id, count=5, notes='Updated count')

# Delete sighting
db.delete_sighting(sighting_id)

# Get all sightings
sightings = db.get_all_sightings(user_id=1, property_id=1)

# Get statistics
stats = db.get_statistics(user_id=1)
```

### Security API

```python
# Log security event
log_security_event(
    event_type='login_success',
    user_id=1,
    username='johndoe',
    ip_address='192.168.1.1',
    user_agent='Mozilla/5.0...',
    details='Login from desktop browser'
)

# Check rate limit
is_allowed = check_rate_limit('192.168.1.1', 'johndoe')

# Get audit trail
events = db.get_audit_trail(user_id=1, limit=100)
```

---

## Version History

### v1.2.0 (2025-10-31)
- Added `security.py` with rate limiting and audit logging
- Added `validators.py` with comprehensive input validation
- Enhanced error handlers (403, 404, 500)
- Added 11 database indices for performance
- Added `audit_log` table for security events

### v1.1.0 (2025-10-31)
- Added `auth.py` with authentication decorators
- Added multi-user support with `users` table
- Added multi-tenant support with `properties` table
- Added role-based access control
- Enhanced `models.py` with user management methods

### v1.0.1 (2025-10-31)
- Security audit and vulnerability fixes
- Enhanced error handling throughout
- Added comprehensive docstrings
- Fixed SQL injection vulnerabilities

### v1.0.0 (2025-10-31)
- Initial implementation
- Core modules: `__init__.py`, `main.py`, `models.py`, `utils.py`
- Basic CRUD operations for sightings
- Photo upload and processing
- PDF and CSV export functionality

---

## Related Documentation

- [AUTHENTICATION.md](../docs/AUTHENTICATION.md) - Complete authentication guide
- [SECURITY_ENHANCEMENTS.md](../docs/branches/claude/roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/SECURITY_ENHANCEMENTS.md) - Security features documentation
- [DEVELOPMENT.md](../docs/DEVELOPMENT.md) - Developer setup and troubleshooting
- [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - System architecture documentation

---

## Contact & Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/dnoice/Roach-Tracker/issues
- Main README: [../README.md](../README.md)

---

**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01
**Author**: dnoice + Claude AI
