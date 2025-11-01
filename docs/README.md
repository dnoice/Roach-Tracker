# Documentation Directory

**Directory**: `docs/`
**Purpose**: Comprehensive project documentation, guides, and branch-specific development logs
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

## Overview

The `docs/` directory serves as the central hub for all project documentation. This includes technical architecture documents, user guides, developer references, and detailed session logs for AI-assisted development branches. The documentation follows a hierarchical structure designed to serve both end-users and developers contributing to the project.

---

## Directory Structure

```
docs/
├── ARCHITECTURE.md              # System architecture and technical design
├── AUTHENTICATION.md            # Authentication system guide
├── DEVELOPMENT.md               # Developer setup and troubleshooting
├── branches/                    # Branch-specific development documentation
│   └── claude/                  # Claude AI development sessions
│       ├── roach-tracker-kickoff-011CUfvod8CFBar781PUVhMy/
│       │   ├── README.md        # Session overview
│       │   ├── INITIAL_BUILD.md # v1.0.0 build documentation
│       │   ├── AUDIT.md         # v1.0.1 security audit
│       │   ├── BANNER_UPDATE.md # Banner image update
│       │   └── COMMITS.md       # Complete commit history
│       └── roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/
│           ├── SESSION_SUMMARY.md       # Session overview
│           ├── SECURITY_ENHANCEMENTS.md # v1.2.0 security features
│           ├── FILES_MODIFIED.md        # File change log
│           └── COMMITS.md               # Complete commit history
└── README.md                    # This file
```

---

## Core Documentation Files

### `ARCHITECTURE.md` - System Architecture

**Purpose**: Technical design documentation and system architecture overview
**Audience**: Developers, system architects, security auditors
**Content**:

- **System Overview**: High-level architecture diagram and component breakdown
- **Technology Stack**: Detailed list of frameworks, libraries, and tools
- **Database Schema**: Complete ER diagram and table specifications
- **Security Architecture**: Authentication flow, authorization model, security layers
- **API Design**: Route structure, request/response formats
- **File Organization**: Directory structure and module responsibilities
- **Data Flow**: How data moves through the system from input to output
- **Deployment Architecture**: Server setup, environment configuration

**Key Topics**:
```
1. MVC Architecture (Model-View-Controller)
2. Database Design (SQLite schema, indices, relationships)
3. Security Model (Authentication, Authorization, Audit Logging)
4. Frontend Architecture (Jinja2 templates, responsive design)
5. Backend Architecture (Flask routes, business logic, utilities)
6. API Endpoints (RESTful design, HTTP methods)
7. File Storage (User uploads, exports, static assets)
8. Performance Optimizations (Database indices, caching, lazy loading)
```

**When to Read**:
- Before making major architectural changes
- When adding new features that span multiple layers
- During security audits or code reviews
- For onboarding new developers to the project

**Related Files**:
- [../app/README.md](../app/README.md) - Backend implementation details
- [../templates/README.md](../templates/README.md) - Frontend template structure
- [SECURITY_ENHANCEMENTS.md](branches/claude/roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/SECURITY_ENHANCEMENTS.md)

---

### `AUTHENTICATION.md` - Authentication Guide

**Purpose**: Complete guide to the multi-user authentication system
**Audience**: Developers, system administrators, security reviewers
**Content**:

- **Authentication Overview**: Session-based authentication with Flask-Login
- **User Model**: User table schema, roles, permissions
- **Registration Flow**: Account creation process and validation
- **Login Flow**: Authentication process, session management
- **Password Security**: Hashing (PBKDF2-SHA256), strength requirements
- **Role-Based Access Control**: Admin, resident, property_manager roles
- **Session Management**: Session cookies, "remember me" functionality
- **Admin Tools**: User management dashboard, account controls
- **Security Features**: Rate limiting, account lockout, audit logging
- **Multi-Tenant Support**: Properties and user-property relationships

**Key Features Documented**:
```
1. User Registration & Validation
   - Email validation (RFC 5322)
   - Username validation (3-32 chars, alphanumeric)
   - Password strength (8+ chars, uppercase, lowercase, digit, special)
   - Reserved username blocking

2. Authentication Security
   - PBKDF2-SHA256 password hashing
   - Rate limiting (5 attempts / 5 minutes)
   - Account lockout (15 minute duration)
   - Audit trail logging

3. Authorization & Roles
   - Admin: Full system access
   - Property Manager: Multi-property management
   - Resident: Personal sighting tracking

4. Session Management
   - Secure session cookies
   - "Remember me" option (30 day persistence)
   - Automatic session expiration
   - Session invalidation on password change
```

**Code Examples**:
The document includes practical code examples for:
- Creating admin users
- Implementing role-based route protection
- Checking user permissions in templates
- Managing user sessions programmatically

**When to Read**:
- Before implementing new user-facing features
- When troubleshooting login/authentication issues
- During security audits
- When configuring multi-tenant functionality

**Related Files**:
- [../app/auth.py](../app/auth.py) - Authentication decorators
- [../app/security.py](../app/security.py) - Security logging and rate limiting
- [../app/validators.py](../app/validators.py) - Input validation functions
- [SECURITY_ENHANCEMENTS.md](branches/claude/roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/SECURITY_ENHANCEMENTS.md)

---

### `DEVELOPMENT.md` - Developer Guide

**Purpose**: Comprehensive developer setup, troubleshooting, and contribution guide
**Audience**: Developers (new contributors, maintainers)
**Content**:

- **Quick Start**: Fast setup instructions for development
- **Environment Setup**: Python version, virtual environment, dependencies
- **Database Setup**: SQLite initialization, migrations
- **Running the App**: Multiple methods (run.sh, run.py, Flask CLI)
- **Development Workflow**: Code style, testing, committing
- **Common Issues**: Troubleshooting guide with solutions
- **Testing**: Unit tests, integration tests, security tests
- **Code Quality**: Linting, type checking, documentation standards
- **Security Best Practices**: Secure coding guidelines
- **Contribution Guide**: Pull request process, code review

**Key Sections**:
```
1. Prerequisites & Installation
   - Python 3.12+
   - Virtual environment setup
   - Dependency installation (requirements.txt)
   - Database initialization

2. Running the Application
   - Development server (./run.sh)
   - Debug mode enabled
   - Hot reload on code changes
   - Custom host/port configuration

3. Development Tools
   - Code editor setup (VS Code, PyCharm)
   - Debugging with pdb/debugger
   - Database inspection tools (SQLite browser)
   - API testing (curl, Postman)

4. Testing
   - Running tests (pytest)
   - Writing new tests
   - Test coverage reporting
   - Integration testing

5. Common Issues & Solutions
   - Import errors (PYTHONPATH issues)
   - Database locked errors
   - Port already in use
   - Permission errors
   - Missing dependencies

6. Code Style
   - PEP 8 compliance
   - Type hints
   - Docstring format (Google style)
   - Comment guidelines

7. Git Workflow
   - Branch naming conventions
   - Commit message format
   - Pull request process
   - Code review checklist
```

**Troubleshooting Examples**:
```bash
# ModuleNotFoundError: No module named 'app'
# Solution: Always run from project root
cd /path/to/Roach-Tracker
python run.py

# Database is locked
# Solution: Close other connections, check for zombie processes
ps aux | grep python
kill <pid>

# Port 5000 already in use
# Solution: Use different port
python run.py --port 8000
```

**When to Read**:
- Setting up development environment for first time
- Troubleshooting build/runtime errors
- Before submitting pull requests
- When learning project coding standards

**Related Files**:
- [../README.md](../README.md) - User-facing installation guide
- [../requirements.txt](../requirements.txt) - Python dependencies
- [../setup.sh](../setup.sh) - Automated setup script
- [../verify.sh](../verify.sh) - Environment verification script

---

## Branch Documentation (`docs/branches/`)

### Purpose

The `branches/` directory maintains detailed documentation for each development branch, particularly AI-assisted development sessions with Claude. This creates an audit trail of development decisions, changes made, and rationale behind implementations.

### Structure

```
docs/branches/
└── claude/                      # Claude AI development sessions
    └── [branch-name]/           # One directory per branch
        ├── README.md            # Branch overview and summary
        ├── SESSION_SUMMARY.md   # Session goals and outcomes (or)
        ├── INITIAL_BUILD.md     # Initial implementation docs
        ├── COMMITS.md           # Complete commit history with diffs
        ├── FILES_MODIFIED.md    # File-by-file change log
        └── [FEATURE].md         # Feature-specific documentation
```

### Claude AI Session Documentation

**Session Directory Naming Convention**:
```
claude/[project-name]-[session-description]-[session-id]/

Examples:
- roach-tracker-kickoff-011CUfvod8CFBar781PUVhMy/
- roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/
```

**Required Files in Each Session Directory**:

1. **README.md** or **SESSION_SUMMARY.md** - Overview
   - Session date and duration
   - Session goals and objectives
   - Key accomplishments
   - Version number (if release)
   - Summary of changes
   - Testing performed
   - Known issues or future work

2. **COMMITS.md** - Complete Commit History
   - Every commit made during session
   - Full commit messages
   - Code diffs for each commit
   - Explanation of changes
   - Rationale for decisions

3. **FILES_MODIFIED.md** (optional but recommended)
   - List of all files created/modified/deleted
   - Brief description of changes per file
   - Before/after line counts
   - Purpose of each file

4. **Feature-Specific Documentation** (e.g., SECURITY_ENHANCEMENTS.md)
   - Deep dive into specific features
   - Implementation details
   - Usage examples
   - Configuration options
   - Testing recommendations

---

## Existing Session Documentation

### Session 1: `roach-tracker-kickoff-011CUfvod8CFBar781PUVhMy/`

**Date**: 2025-10-31
**Version**: v1.0.0 → v1.0.1
**Focus**: Initial application build and security audit

**Documents**:
- **README.md**: Session overview, 3 major phases documented
- **INITIAL_BUILD.md**: Complete v1.0.0 initial build (30+ files, ~5,500 LOC)
- **AUDIT.md**: Security audit fixing 42 issues across all core logic
- **BANNER_UPDATE.md**: Addition of GitHub banner image
- **COMMITS.md**: 69 commits with full history and diffs

**Major Accomplishments**:
- ✓ Complete full-stack application from scratch
- ✓ Mobile-responsive frontend (7 templates)
- ✓ SQLite database with CRUD operations
- ✓ Photo upload and processing
- ✓ PDF and CSV report generation
- ✓ Security audit: 42 fixes, zero SQL injection vulnerabilities
- ✓ Comprehensive documentation suite

**Key Files Created**:
```
app/__init__.py, app/main.py, app/models.py, app/utils.py
templates/*.html (7 templates)
static/css/style.css, static/js/main.js
setup.sh, run.sh, verify.sh
requirements.txt, .env.example
README.md, QUICK_START.md
```

---

### Session 2: `roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/`

**Date**: 2025-10-31
**Version**: v1.1.0 → v1.2.0
**Focus**: Authentication system and security enhancements

**Documents**:
- **SESSION_SUMMARY.md**: Session overview and goals
- **SECURITY_ENHANCEMENTS.md**: 600+ line comprehensive security documentation
- **FILES_MODIFIED.md**: Detailed log of all file changes
- **COMMITS.md**: Complete commit history for session

**Major Accomplishments**:
- ✓ Multi-user authentication with Flask-Login
- ✓ Role-based access control (admin, resident, property_manager)
- ✓ Rate limiting and account lockout (5 attempts/5min, 15min lockout)
- ✓ Security event logging with audit trail
- ✓ Input validation module (RFC 5322 email, strong passwords)
- ✓ User management dashboard (admin only)
- ✓ 11 database performance indices
- ✓ Enhanced error handlers (403, 404, 500)

**Key Files Created**:
```
app/auth.py - Authentication decorators
app/security.py - Security logging and rate limiting
app/validators.py - Input validation functions
create_admin.py - Admin user creation script
templates/login.html, templates/register.html
templates/admin_users.html, templates/admin_create_user.html
templates/profile.html, templates/change_password.html
docs/AUTHENTICATION.md - Complete auth guide
docs/DEVELOPMENT.md - Developer guide
```

**Security Features Added**:
- Password hashing: PBKDF2-SHA256
- Rate limiting: In-memory with IP tracking
- Account lockout: After 5 failed attempts
- Audit logging: All security events to database
- Input validation: Email, username, password strength
- Reserved username blocking: admin, root, system, etc.

---

## Documentation Standards

### Writing Style Guidelines

**For Technical Documentation**:
- **Clear and Concise**: Short sentences, active voice
- **Code Examples**: Provide working examples with comments
- **Step-by-Step**: Number sequential steps
- **Visual Aids**: Use diagrams, tables, code blocks
- **Searchable**: Include keywords and technical terms
- **Up-to-Date**: Update docs when code changes

**Markdown Formatting**:
```markdown
# H1 - Document Title (only one per document)
## H2 - Major Section
### H3 - Subsection
#### H4 - Sub-subsection

**Bold** for emphasis
*Italic* for technical terms on first use
`code` for inline code, commands, filenames

Code blocks with language specification:
```python
def example():
    pass
```

Tables for structured data:
| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |

Lists:
- Unordered lists for non-sequential items
1. Ordered lists for sequential steps
```

### File Naming Conventions

**Format**: `UPPERCASE_DESCRIPTION.md`

**Examples**:
- `ARCHITECTURE.md` ✓
- `AUTHENTICATION.md` ✓
- `DEVELOPMENT.md` ✓
- `SESSION_SUMMARY.md` ✓
- `SECURITY_ENHANCEMENTS.md` ✓

**Avoid**:
- `architecture.md` ✗ (lowercase, not visible in directory listings)
- `auth docs.md` ✗ (spaces)
- `dev-guide.md` ✗ (lowercase, hyphens for underscores)

### Document Header Format

Every markdown document should begin with a standard header:

```markdown
# Document Title

**File**: `DOCUMENT_NAME.md`
**Path**: `docs/DOCUMENT_NAME.md`
**Purpose**: Brief description of document purpose
**Audience**: Who should read this (developers, users, admins)
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

## Overview

[First paragraph of content]
```

### Code Block Best Practices

**Language Tags** (for syntax highlighting):
```markdown
```python      # Python code
```bash        # Shell commands
```javascript  # JavaScript
```sql         # SQL queries
```html        # HTML markup
```css         # CSS styles
```json        # JSON data
```markdown    # Markdown examples
```text        # Plain text, logs
```
```

**Include Comments**:
```python
# Good: Commented code
def calculate_total(items):
    """Calculate sum of item prices"""
    return sum(item.price for item in items)

# Bad: No comments
def calc(i):
    return sum(x.p for x in i)
```

**Show Expected Output**:
```bash
# Command
python run.py

# Expected Output:
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

---

## Adding New Documentation

### Process for New Documents

**Step 1**: Identify documentation need
- New feature requiring user guide?
- Complex system needing architecture doc?
- Branch-specific development log?

**Step 2**: Choose appropriate location
```
docs/                         # General project documentation
docs/branches/claude/         # AI session logs
[component]/README.md         # Component-specific docs
```

**Step 3**: Create document with standard header
```markdown
# Document Title

**File**: `DOCUMENT_NAME.md`
**Purpose**: Why this document exists
**Audience**: Who should read it
**Version**: 1.2.0
**Created**: 2025-11-01
**Updated**: 2025-11-01
```

**Step 4**: Write content following standards
- Use clear headings hierarchy
- Include code examples
- Add step-by-step instructions
- Provide troubleshooting section
- Link to related documents

**Step 5**: Link from relevant locations
```markdown
# In README.md
- [New Feature Guide](docs/NEW_FEATURE.md) - How to use the new feature

# In related docs
See also: [NEW_FEATURE.md](NEW_FEATURE.md)
```

**Step 6**: Commit with descriptive message
```bash
git add docs/NEW_FEATURE.md
git commit -m "Add documentation for new feature X"
```

### Documentation Checklist

Before committing new documentation:

- [ ] Standard header included (file, path, purpose, audience, version, dates)
- [ ] Proper heading hierarchy (H1 → H2 → H3, no skipping levels)
- [ ] Code blocks have language tags for syntax highlighting
- [ ] Examples are tested and working
- [ ] Links to related documents included
- [ ] Spelling and grammar checked
- [ ] Markdown renders correctly (preview in VS Code, GitHub)
- [ ] File named according to conventions (UPPERCASE_DESCRIPTION.md)
- [ ] Linked from main README or parent document

---

## Documentation Maintenance

### Keeping Docs Up-to-Date

**When Code Changes**:
1. Update relevant documentation immediately (not later!)
2. Change version number and "Updated" date
3. Add note about what changed (if significant)
4. Review related docs for impact

**Quarterly Review** (every 3 months):
1. Read through all docs for accuracy
2. Update outdated examples or screenshots
3. Remove references to deprecated features
4. Add documentation for undocumented features
5. Check all links are valid
6. Update version numbers

**After Major Releases**:
1. Create release documentation (CHANGELOG, MIGRATION_GUIDE)
2. Update main README with new features
3. Add session documentation if AI-assisted
4. Update architecture docs if structure changed
5. Review and update API documentation

### Documentation Versioning

**Version Numbers in Docs**:
```markdown
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

## Version History

### v1.2.0 (2025-10-31)
- Added authentication section
- Updated security best practices
- New code examples for role-based access

### v1.1.0 (2025-10-31)
- Initial documentation
```

**Git Tags for Documentation Releases**:
```bash
# Tag documentation along with code releases
git tag -a v1.2.0 -m "Release v1.2.0 with authentication and security enhancements"
git push origin v1.2.0
```

---

## Finding Documentation

### Documentation Index

**User-Facing Documentation**:
- [Main README](../README.md) - Project overview, installation, usage
- [QUICK_START.md](../QUICK_START.md) - Fast setup guide (if exists)
- [SAMPLE_COMPLAINT_LETTER.txt](../SAMPLE_COMPLAINT_LETTER.txt) - Template for complaints

**Technical Documentation**:
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
- [AUTHENTICATION.md](AUTHENTICATION.md) - Auth system guide

**Component Documentation** (see component directories):
- [app/README.md](../app/README.md) - Backend Python application
- [templates/README.md](../templates/README.md) - Frontend HTML templates
- [static/README.md](../static/README.md) - CSS, JavaScript, uploads
- [exports/README.md](../exports/README.md) - PDF/CSV exports
- [global-assets/images/README.md](../global-assets/images/README.md) - Brand images

**Development Logs**:
- [branches/claude/roach-tracker-kickoff-011CUfvod8CFBar781PUVhMy/](branches/claude/roach-tracker-kickoff-011CUfvod8CFBar781PUVhMy/) - Session 1
- [branches/claude/roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/](branches/claude/roach-development-session-two-011CUg7jBTWttm3WXuHyGjig/) - Session 2

### Search Tips

**Find by Topic**:
```bash
# Search all markdown files for keyword
grep -r "authentication" docs/*.md

# Find files containing "security"
grep -l "security" docs/**/*.md

# Search case-insensitive
grep -ri "database" docs/
```

**Find by File Type**:
```bash
# All markdown files
find docs/ -name "*.md"

# READMEs only
find docs/ -name "README.md"

# Session documentation
find docs/branches/claude/ -type f -name "*.md"
```

---

## Related Documentation

- [Main README](../README.md) - Project overview
- [Component READMEs](../README.md#project-structure) - See individual component directories
- [SAMPLE_COMPLAINT_LETTER.txt](../SAMPLE_COMPLAINT_LETTER.txt) - Legal template

---

## Contributing to Documentation

### How to Contribute

1. **Identify Gap**: Find missing or outdated documentation
2. **Discuss**: Open GitHub issue to discuss proposed changes
3. **Write**: Create or update documentation following standards
4. **Review**: Self-review using documentation checklist
5. **Submit**: Create pull request with clear description
6. **Revise**: Address review comments
7. **Merge**: Documentation merged and published

### Documentation Pull Request Template

```markdown
## Documentation Change

**Type**: [New Documentation | Update | Fix | Removal]
**Files**:
- docs/NEW_FILE.md (new)
- docs/EXISTING_FILE.md (updated)

**Changes**:
- Added section on X
- Updated Y to reflect current implementation
- Fixed broken links to Z

**Checklist**:
- [ ] Standard header included
- [ ] Examples tested and working
- [ ] Links verified
- [ ] Spelling/grammar checked
- [ ] Markdown renders correctly
- [ ] Follows style guidelines
```

---

## Contact & Support

For documentation issues, questions, or suggestions:
- GitHub Issues: https://github.com/dnoice/Roach-Tracker/issues
- Label: `documentation`
- Main README: [../README.md](../README.md)

---

## Version History

### v1.2.0 (2025-11-01)
- Added comprehensive docs/README.md (this file)
- Documented all component directories
- Standardized documentation format across project

### v1.1.0 (2025-10-31)
- Added AUTHENTICATION.md
- Added DEVELOPMENT.md
- Created session 2 documentation

### v1.0.1 (2025-10-31)
- Created ARCHITECTURE.md
- Created session 1 documentation
- Established branch documentation structure

### v1.0.0 (2025-10-31)
- Initial docs directory creation
- Main README created

---

**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01
**Author**: dnoice + Claude AI
