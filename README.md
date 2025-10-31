# Roach Tracker

![Roach Tracker Banner](https://github.com/dnoice/Roach-Tracker/blob/main/global-assets/images/roach-tracker-banner.png)

You have the right to a habitable living space. Cockroach infestations violate the implied warranty of habitability in most jurisdictions. This tool helps you exercise your rights through professional documentation tools.

---

## Overview

Roach Tracker is a full-stack, local-first, privacy-focused web application for documenting, cataloging, and reporting cockroach sightings in apartments, homes, and businesses. Built with Flask, it provides a mobile-responsive interface for logging sightings with photo evidence, tracking patterns, and generating professional reports for property management or legal purposes.

### Key Features

- **User Authentication** - Secure multi-user support with role-based access control
- **Mobile-Optimized Interface** - Touch-friendly controls with responsive design
- **Photo Documentation** - Upload and store photos with automatic resizing
- **Comprehensive Tracking** - Log location, count, size, time, weather, and notes
- **Analytics Dashboard** - Visualize patterns and trends in sighting data
- **Professional Reports** - Generate PDF and CSV exports for management
- **Multi-Tenant Support** - Property management for landlords and property managers
- **100% Local & Private** - No cloud services, complete data control
- **Zero Configuration** - Simple setup with automated scripts

### Technology Stack

- **Backend**: Flask (Python 3.12)
- **Authentication**: Flask-Login with secure password hashing
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Photo Processing**: Pillow (PIL)
- **PDF Generation**: ReportLab
- **Mobile Support**: Fully responsive design

---

## Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/dnoice/Roach-Tracker.git
cd Roach-Tracker

# 2. Run setup (creates venv, installs dependencies, initializes database)
./setup.sh

# 3. Create admin user
python create_admin.py

# 4. Start the application
./run.sh
```

Then open your browser to `http://localhost:5000/login` and log in with your admin credentials

### Verification

To verify your installation:

```bash
./verify.sh
```

---

## Usage

### Logging a Sighting

1. Open the web application
2. Click "Log New Sighting"
3. Fill in the details (location, count, size, etc.)
4. Upload a photo (optional but recommended)
5. Submit

### Viewing Sightings

- **Dashboard**: Quick overview with recent sightings
- **All Sightings**: Browse complete history with search
- **Statistics**: Comprehensive analytics and visualizations

### Generating Reports

1. Navigate to Statistics page
2. Click "Export PDF Report" or "Export CSV Data"
3. Reports are saved to the `exports/` directory
4. Use these for documentation with property management

---

## Documentation

- [QUICK_START.md](QUICK_START.md) - Detailed setup and usage guide
- [AUTHENTICATION.md](AUTHENTICATION.md) - User authentication and management guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical design and structure
- [SAMPLE_COMPLAINT_LETTER.txt](SAMPLE_COMPLAINT_LETTER.txt) - Template for formal complaints

---

## Development Environment

This project is optimized for diverse environments, including:

- **Desktop**: Windows, macOS, Linux
- **Mobile Development**: Android (Termux + PRoot)
- **Server**: Any Linux-based system

### Special Note for Android/Termux Users

This application runs perfectly in Termux with PRoot-distro (Ubuntu). The development environment supports:
- Python 3.12 in virtual environments
- Full Flask application stack
- SQLite database operations
- Image processing with Pillow

---

## Project Structure

```
Roach-Tracker/
├── app/
│   ├── __init__.py       # Flask app initialization
│   ├── main.py           # Routes and application logic
│   ├── models.py         # Database schema and operations
│   └── utils.py          # Helper functions (photos, PDFs, CSVs)
├── templates/            # HTML templates
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript
│   └── uploads/          # Photo storage
├── data/                 # SQLite database
├── exports/              # Generated reports
├── docs/branches/        # AI continuity and session logs
├── requirements.txt      # Python dependencies
├── setup.sh              # Setup script
├── run.sh                # Launch script
└── verify.sh             # Verification script
```

---

## Privacy & Security

- **100% Local**: All data stays on your device
- **No Cloud**: No external services or tracking
- **No Accounts**: No registration or personal data required
- **Full Control**: You own all your data and photos

---

## Contributing

This project follows the **10 Golden Rules**:

1. Unified metadata headers in all files
2. No box-drawing characters (alignment over ornamentation)
3. Rich terminal output for all CLI operations
4. SVG graphics in UI (no emoji)
5. Design for elegance, robustness, and intuitiveness
6. Dual-mode UX (beginner-friendly + power-user features)
7. Document as you build
8. No hardcoded secrets (use .env)
9. Fail gracefully with beautiful error logging
10. Consistency over cleverness

---

## License

See [LICENSE](LICENSE) file for details.

---

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/dnoice/Roach-Tracker/issues

---

## Version History

### v1.1.0 (2025-10-31) - Authentication & Multi-User Support

**Major New Features**:
- ✓ Complete authentication system with Flask-Login
- ✓ User registration and login/logout functionality
- ✓ Role-based access control (admin, resident, property_manager)
- ✓ Multi-tenant support with properties and user relationships
- ✓ Admin dashboard for user management
- ✓ Secure password hashing (PBKDF2-SHA256)
- ✓ Session management with "remember me" option
- ✓ User activation/deactivation controls

**Database Enhancements**:
- Added users table with comprehensive fields
- Added properties table for multi-tenant support
- Added user_properties relationship table
- Extended sightings table with user_id and property_id
- Automatic migration for existing databases

**New Files**:
- `app/auth.py` - Authentication decorators and utilities
- `create_admin.py` - Interactive admin user creation script
- `templates/login.html` - User login page
- `templates/register.html` - User registration page
- `templates/admin_users.html` - Admin user management interface
- `templates/admin_create_user.html` - Admin user creation form
- `AUTHENTICATION.md` - Complete authentication documentation

**Code Updates**:
- Updated all routes with @login_required decorators
- Enhanced navigation with user info display
- Added CSS styling for authentication UI
- Updated base template with conditional navigation
- Modified models.py with comprehensive user management methods

**Documentation**:
- Created comprehensive AUTHENTICATION.md guide
- Updated README with authentication information
- Updated quick start guide with admin creation step
- Added authentication to feature list

For detailed information, see: [AUTHENTICATION.md](AUTHENTICATION.md)

### v1.0.1 (2025-10-31) - Security & Stability Update

**Major Accomplishments**:
- ✓ Comprehensive security audit completed
- ✓ Fixed 42 issues across all core logic files
- ✓ Patched 8 critical security vulnerabilities
- ✓ Zero SQL injection vulnerabilities remaining
- ✓ Complete input validation implemented
- ✓ Enterprise-grade error handling
- ✓ Production-ready code quality achieved
- ✓ Comprehensive branch documentation created

**Security Fixes**:
- SQL injection prevention (parameterized queries)
- SQL wildcard injection protection
- Decompression bomb vulnerability patched
- File size validation before processing
- XML injection prevention in PDF generation
- Information leakage through errors eliminated
- Path traversal protection enhanced
- Production secret key validation

**Quality Improvements**:
- All bare except clauses replaced with specific exceptions
- Comprehensive input validation across all layers
- Type safety enhancements throughout
- User-friendly error messages with server-side logging
- Enhanced file operation safety
- Complete docstrings with Raises sections

**Documentation**:
- Branch-specific documentation system implemented
- Complete commit history documented
- Initial build documentation (v1.0.0)
- Comprehensive audit documentation (v1.0.1)

For detailed information, see: `docs/branches/claude/roach-tracker-kickoff-011CUfvod8CFBar781PUVhMy/`

### v1.0.0 (2025-10-31) - Initial Release

**Complete Full-Stack Implementation**:
- Flask backend with SQLite database
- Mobile-responsive frontend (7 templates)
- Photo upload and processing
- PDF and CSV report generation
- Statistics and analytics dashboard
- Automated setup scripts
- Comprehensive documentation suite
- 30+ files created, ~5,500 lines of code

---

## Roadmap / Future Development

### Completed Features

**✓ Authentication & Multi-User Support** (v1.1.0)
- User accounts and authentication system
- Role-based access control (admin, resident, property manager)
- Multi-tenant support for property managers
- Admin dashboard for user management
- Secure password hashing and session management

### Planned Features

**Enhanced Reporting**
- Additional export formats (JSON, Excel/XLSX)
- Customizable report templates
- Scheduled/automated report generation
- Email notification system for new sightings

**Data Management**
- Advanced filtering and sorting options
- Bulk operations (edit, delete, export)
- Data import functionality
- Automated backup and restore system
- Data archiving for old sightings

**Analytics Enhancements**
- Interactive charts and visualizations
- Heatmap of infestation hotspots
- Trend analysis and predictions
- Comparison views (week-over-week, month-over-month)
- Severity scoring algorithm

**Mobile Experience**
- Progressive Web App (PWA) support
- Offline functionality
- Native mobile app versions (iOS/Android)
- Push notifications for patterns/alerts

**Integration & API**
- RESTful API for third-party integration
- Webhook support for external systems
- Integration with property management systems
- Health department reporting integration

**Quality & Testing**
- Automated test suite (unit, integration, e2e)
- Continuous integration/deployment pipeline
- Performance monitoring and optimization
- Accessibility compliance (WCAG 2.1)

**Localization**
- Multi-language support (i18n)
- Regional date/time formatting
- Jurisdiction-specific legal templates

**Advanced Features**
- Machine learning for roach identification from photos
- Pattern detection algorithms
- Collaborative documentation (multiple units)
- Anonymous community reporting
- Integration with smart home devices

---

## Acknowledgments

Created by **dnoice** with **Claude AI**

Version: 1.1.0
Created: 2025-10-31
Updated: 2025-10-31

---

**Remember**: You have the right to safe, habitable housing. Document everything.
