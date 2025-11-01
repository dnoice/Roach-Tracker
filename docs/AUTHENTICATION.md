# Authentication & User Management

**File**: `AUTHENTICATION.md`
**Path**: `docs/AUTHENTICATION.md`
**Purpose**: Documentation for authentication system and user management
**Author**: dnoice + Claude AI
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

## Overview

Roach Tracker now includes a comprehensive authentication and user management system with role-based access control (RBAC). This enables multi-user environments, property management workflows, and secure data access.

---

## Features

### Authentication
- **Secure Password Hashing**: Uses Werkzeug's PBKDF2-SHA256 for password storage
- **Session Management**: Flask-Login for persistent user sessions
- **Remember Me**: Optional persistent login across browser sessions
- **Account Status**: Users can be activated/deactivated by admins

### User Roles

The system supports three user roles with different permission levels:

1. **Resident**
   - Log and view sightings
   - Generate reports
   - Basic access to the application

2. **Property Manager**
   - All resident permissions
   - Access to multi-property management features
   - View sightings across managed properties

3. **Administrator**
   - Full system access
   - User management (create, edit, delete, activate/deactivate)
   - Property management
   - All application features

### Multi-Tenant Support

- **Properties**: Create and manage multiple properties
- **User-Property Relationships**: Assign users to properties with relationship types:
  - Owner
  - Manager
  - Resident
- **Data Isolation**: Sightings are associated with users and properties

---

## Getting Started

### Initial Setup

#### 1. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install new dependencies
pip install -r requirements.txt
```

#### 2. Create Admin User

Run the admin creation script:

```bash
python create_admin.py
```

Follow the prompts to create your first administrator account:

```
Username (min 3 chars): admin
Email address: admin@example.com
Full name (optional): System Administrator
Password (min 8 chars): ********
Confirm password: ********
```

#### 3. Start the Application

```bash
./run.sh
```

Navigate to `http://localhost:5000/login` and log in with your admin credentials.

---

## Usage

### User Registration

New users can register at `/register`:

1. Navigate to http://localhost:5000/register
2. Fill in:
   - Username (minimum 3 characters)
   - Email address
   - Full name (optional)
   - Password (minimum 8 characters)
   - Password confirmation
3. Default role is "Resident"
4. After registration, redirect to login page

### User Login

Users can log in at `/login`:

1. Navigate to http://localhost:5000/login
2. Enter username and password
3. Optionally check "Remember me" for persistent session
4. After successful login, redirect to dashboard

### User Logout

Click "Logout" in the navigation menu or visit `/logout`.

---

## Admin User Management

### Accessing User Management

Admins can access user management at `/admin/users` (visible in navigation for admin users only).

### Creating Users

As an admin:

1. Navigate to Admin > Users
2. Click "Create New User"
3. Fill in:
   - Username
   - Email
   - Full name (optional)
   - Password
   - Role (resident, property_manager, admin)
4. Click "Create User"

### Managing Users

From the Users page, admins can:

- **View all users** with details (username, email, role, status, last login)
- **Activate/Deactivate users** - Prevents login without deleting account
- **Delete users** - Permanently removes user account
- Users cannot deactivate or delete their own account

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'resident',
    full_name TEXT,
    is_active INTEGER DEFAULT 1,
    last_login TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    CHECK (role IN ('admin', 'resident', 'property_manager'))
);
```

### Properties Table

```sql
CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    created_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### User-Property Relationships

```sql
CREATE TABLE user_properties (
    user_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,
    relationship_type TEXT NOT NULL DEFAULT 'resident',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, property_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    CHECK (relationship_type IN ('owner', 'manager', 'resident'))
);
```

### Updated Sightings Table

The `sightings` table now includes:

```sql
-- New columns
user_id INTEGER,
property_id INTEGER,

-- Foreign keys
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL
```

---

## API Reference

### Database Methods

#### User Management

```python
# Create user
user_id = db.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password',
    role='resident',
    full_name='John Doe'
)

# Get user by ID
user = db.get_user_by_id(user_id)

# Get user by username
user = db.get_user_by_username('john_doe')

# Verify credentials
user = db.verify_user_password('john_doe', 'password')

# Update user
db.update_user(user_id, {
    'email': 'newemail@example.com',
    'role': 'property_manager'
})

# Delete user
db.delete_user(user_id)

# Get all users
users = db.get_all_users()
users = db.get_all_users(role='admin')  # Filter by role
```

#### Property Management

```python
# Create property
property_id = db.create_property(
    name='Sunset Apartments',
    created_by=user_id,
    address='123 Main St'
)

# Get property
property = db.get_property(property_id)

# Assign user to property
db.assign_user_to_property(
    user_id=user_id,
    property_id=property_id,
    relationship_type='resident'
)

# Get user's properties
properties = db.get_user_properties(user_id)

# Get property's users
users = db.get_property_users(property_id)
```

### Authentication Decorators

```python
from flask_login import login_required
from app.auth import admin_required, property_manager_required

# Require any authenticated user
@app.route('/protected')
@login_required
def protected_view():
    pass

# Require admin role
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    pass

# Require property manager or admin
@app.route('/properties')
@property_manager_required
def properties_view():
    pass
```

---

## Security Features

### Password Security
- **Hashing**: PBKDF2-SHA256 with salt
- **Minimum Length**: 8 characters enforced
- **No Plain Text Storage**: Passwords are never stored in plain text

### Session Security
- **SECRET_KEY**: Configurable via environment variable
- **Session Cookies**: HTTP-only, secure in production
- **Remember Me**: Optional persistent sessions

### Input Validation
- **Username**: Minimum 3 characters, unique
- **Email**: Format validation, unique
- **Password**: Minimum 8 characters
- **Role**: Restricted to valid values

### Account Protection
- **Self-Protection**: Users cannot deactivate or delete own account
- **Active Status**: Inactive accounts cannot log in
- **Last Login**: Tracking for security auditing

---

## Migration from v1.0.0

Existing databases will be automatically migrated when the application starts:

1. **Automatic Migration**: The `init_database()` method detects existing `sightings` table
2. **Column Addition**: Adds `user_id` and `property_id` columns if missing
3. **Data Preservation**: All existing sightings remain intact
4. **NULL Values**: Existing sightings will have NULL `user_id` (no owner)

### Post-Migration Steps

1. Create admin user: `python create_admin.py`
2. Restart application: `./run.sh`
3. Log in and create additional users as needed

---

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Required: Secret key for session encryption
SECRET_KEY=your-super-secret-key-change-this-in-production

# Optional: Database path
DATABASE_PATH=data/roach_tracker.db
```

### Production Deployment

For production environments:

1. **Generate Strong SECRET_KEY**:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Set in .env**:
   ```bash
   SECRET_KEY=your-generated-secret-key-here
   FLASK_ENV=production
   ```

3. **HTTPS**: Use HTTPS for secure cookie transmission
4. **Firewall**: Restrict admin routes to authorized networks

---

## Troubleshooting

### Cannot Create Admin User

**Error**: "Username already exists" or "Email already exists"

**Solution**: Check existing users:
```python
python
>>> from app.models import Database
>>> db = Database('data/roach_tracker.db')
>>> users = db.get_all_users()
>>> for u in users:
...     print(f"{u['id']}: {u['username']} ({u['email']})")
```

### Forgot Admin Password

**Solution**: Reset via database or create new admin:
```python
python
>>> from app.models import Database
>>> db = Database('data/roach_tracker.db')
>>> db.update_user_password(1, 'new_password')  # User ID 1
```

### Users Cannot Log In

**Possible Causes**:
1. **Inactive Account**: Admin may have deactivated account
2. **Wrong Credentials**: Verify username/password
3. **Database Issues**: Check database file permissions

**Solution**: Check user status:
```python
python
>>> from app.models import Database
>>> db = Database('data/roach_tracker.db')
>>> user = db.get_user_by_username('username')
>>> print(user['is_active'])  # Should be 1
```

---

## Future Enhancements

Planned features for future versions:

- Password reset via email
- Two-factor authentication (2FA)
- OAuth integration (Google, GitHub)
- User profile pages
- Password strength requirements
- Account lockout after failed attempts
- Audit logging for admin actions
- Bulk user import/export
- Property dashboard for managers
- Role permissions customization

---

## Security Best Practices

1. **Strong Passwords**: Encourage users to use strong, unique passwords
2. **Regular Updates**: Keep dependencies updated
3. **Environment Variables**: Never commit `.env` to version control
4. **HTTPS**: Use HTTPS in production
5. **Backup**: Regularly backup the database
6. **Access Control**: Limit admin access to trusted users
7. **Monitoring**: Monitor login attempts and user activity
8. **Deactivate**: Deactivate unused accounts rather than immediate deletion

---

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/dnoice/Roach-Tracker/issues

---

**Version**: 1.1.0
**Last Updated**: 2025-10-31
**Contributors**: dnoice + Claude AI
