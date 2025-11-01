# Templates Documentation

**Directory**: `templates/`
**Purpose**: Jinja2 HTML templates for the Flask web application frontend
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

## Overview

The `templates/` directory contains all HTML templates for the Roach Tracker web application. These templates use the Jinja2 templating engine (built into Flask) to dynamically generate HTML pages with data from the backend. The templates implement a mobile-first, responsive design with comprehensive accessibility features.

---

## Template Architecture

### Template Inheritance Hierarchy

```
base.html (Base template - navigation, footer, flash messages)
├── index.html (Dashboard)
├── log_sighting.html (New sighting form)
├── view_sightings.html (Sightings list)
├── view_sighting.html (Single sighting detail)
├── edit_sighting.html (Edit sighting form)
├── statistics.html (Analytics dashboard)
├── login.html (Login page)
├── register.html (Registration page)
├── profile.html (User profile)
├── change_password.html (Password change form)
├── admin_users.html (User management dashboard)
└── admin_create_user.html (Create user form)
```

---

## Template Files

### `base.html` - Base Template

**Purpose**: Master template providing consistent layout for all pages
**Lines**: ~105 lines
**Key Features**:

**HTML Structure**:
- Semantic HTML5 markup
- Mobile-optimized viewport settings
- Progressive Web App (PWA) meta tags
- Responsive navigation bar
- Flash message container
- Footer with version info

**Navigation System**:
```jinja2
{% if current_user.is_authenticated %}
    <!-- Authenticated user navigation -->
    - Dashboard
    - Log Sighting
    - All Sightings
    - Statistics
    {% if current_user.is_admin() %}
        - Users (Admin only)
    {% endif %}
    - User Profile (displays username and role)
    - Logout
{% else %}
    <!-- Guest navigation -->
    - Login
    - Register
{% endif %}
```

**Flash Message System**:
- Auto-dismiss messages with close button
- Category-based styling (success, error, warning, info)
- Accessible with ARIA labels
- JavaScript-enabled close functionality

**Mobile Features**:
- Hamburger menu toggle for small screens
- Touch-optimized button sizes
- Responsive container widths
- Mobile-friendly spacing

**Jinja2 Blocks**:
```jinja2
{% block title %}         # Page title in <title> tag
{% block extra_head %}    # Additional <head> content (CSS, meta tags)
{% block content %}       # Main page content
{% block extra_scripts %} # Additional JavaScript at end of <body>
```

**Footer Info**:
- Application version number
- Copyright/attribution
- Privacy statement
- Contact information

---

### `index.html` - Dashboard

**Purpose**: Home page dashboard with recent sightings overview
**Template Extends**: `base.html`
**Key Features**:

**Dashboard Sections**:
1. **Welcome Header**
   - Personalized greeting with username
   - Quick action buttons (Log New Sighting, View All, Statistics)
   - Summary statistics cards (Total Sightings, This Week, This Month)

2. **Recent Sightings Table**
   - Last 10 sightings displayed
   - Columns: Date, Location, Count, Size, Actions
   - Quick view/edit/delete buttons
   - Empty state message if no sightings

3. **Quick Stats Cards**
   - Total sightings count
   - Sightings this week
   - Sightings this month
   - Most common location
   - Average sightings per day

**Responsive Design**:
- Cards stack vertically on mobile
- Table scrolls horizontally on small screens
- Touch-friendly button sizes

---

### `log_sighting.html` - New Sighting Form

**Purpose**: Form for logging new roach sightings
**Template Extends**: `base.html`
**Lines**: ~205 lines
**Key Features**:

**Form Fields**:
```html
<form method="POST" enctype="multipart/form-data">
    - Location (required, text input)
    - Count (required, number input, min=1)
    - Size (select: small, medium, large)
    - Time of Day (select: morning, afternoon, evening, night)
    - Weather (select: dry, humid, rainy, hot, cold)
    - Notes (textarea, optional)
    - Photo (file input, optional, accepts: png, jpg, jpeg, gif, webp)
    - Property (select, for property managers)
</form>
```

**Form Validation**:
- Client-side HTML5 validation (required, min, pattern)
- Server-side validation in Flask route
- Real-time feedback for file uploads
- File size limit warning (16MB max)
- Image preview before upload

**User Experience**:
- Auto-focus on first field
- Tab order optimized for keyboard navigation
- Clear field labels and placeholders
- Helpful tooltips and hints
- Success message on submission
- Redirect to view new sighting after creation

**Accessibility**:
- ARIA labels on all form controls
- Proper label-input associations
- Error messages announced to screen readers
- Keyboard-accessible file input

---

### `view_sightings.html` - Sightings List

**Purpose**: Browse and search all sightings
**Template Extends**: `base.html`
**Lines**: ~148 lines
**Key Features**:

**Search and Filter**:
```html
<form method="GET">
    - Search by location (text input)
    - Filter by size (select dropdown)
    - Filter by date range (date inputs)
    - Sort by: Date, Location, Count (select)
    - Sort order: Ascending/Descending
</form>
```

**Data Table**:
- Columns: Date, Location, Count, Size, Time, Photo Indicator, Actions
- Sortable columns (click to sort)
- Pagination (20 per page)
- Photo thumbnail preview on hover
- Quick action buttons (View, Edit, Delete)

**Bulk Actions** (Future):
- Select multiple sightings
- Bulk delete/export
- Bulk edit properties

**Empty State**:
- Friendly message when no sightings found
- Call-to-action button to log first sighting
- Search tips if filtered results are empty

**Performance**:
- Lazy load photo thumbnails
- Paginated results prevent long load times
- Efficient SQL queries with indices

---

### `view_sighting.html` - Sighting Detail

**Purpose**: View detailed information for a single sighting
**Template Extends**: `base.html`
**Lines**: ~127 lines
**Key Features**:

**Detail View Layout**:
```
+--------------------------+
|  Photo (if available)    |
+--------------------------+
|  Location: Kitchen       |
|  Count: 3 roaches        |
|  Size: Medium            |
|  Time: Night             |
|  Weather: Humid          |
|  Date: 2025-10-31 10:30  |
|  Notes: Near sink...     |
+--------------------------+
|  [Edit] [Delete] [Back]  |
+--------------------------+
```

**Photo Display**:
- Full-size image with zoom capability
- Lightbox modal for enlarged view
- Download original photo button
- Photo metadata (size, dimensions, date)

**Action Buttons**:
- Edit sighting (navigates to edit form)
- Delete sighting (with confirmation modal)
- Back to all sightings
- Export this sighting (PDF/CSV)

**Related Data**:
- User who logged the sighting
- Property associated (if multi-tenant)
- Timestamps (created, last updated)

---

### `edit_sighting.html` - Edit Sighting Form

**Purpose**: Edit existing sighting information
**Template Extends**: `base.html`
**Lines**: ~258 lines
**Key Features**:

**Pre-populated Form**:
- All fields filled with existing data
- Current photo displayed with option to replace
- Original values shown for reference
- Validation same as log_sighting.html

**Photo Management**:
- Display current photo thumbnail
- Option to replace photo (upload new)
- Option to remove photo (checkbox)
- Preview new photo before saving

**Change Tracking**:
- Highlight modified fields (future enhancement)
- Confirmation before discarding changes
- Timestamps show when last edited

**Security**:
- Users can only edit their own sightings
- Admins can edit all sightings
- CSRF token protection on form

---

### `statistics.html` - Analytics Dashboard

**Purpose**: Visualize sighting data with charts and statistics
**Template Extends**: `base.html`
**Lines**: ~254 lines
**Key Features**:

**Statistics Sections**:

1. **Summary Cards**
   - Total sightings
   - Unique locations
   - Date range (first to last sighting)
   - Average per week/month

2. **Location Analysis**
   - Most common locations (bar chart)
   - Location frequency table
   - Percentage breakdown

3. **Size Distribution**
   - Pie chart of small/medium/large
   - Count and percentage per size

4. **Time Pattern Analysis**
   - Sightings by time of day (bar chart)
   - Morning/afternoon/evening/night breakdown

5. **Weather Correlation**
   - Sightings by weather condition
   - Identify patterns (e.g., more in humid weather)

6. **Trend Over Time**
   - Line chart of sightings per week/month
   - Identify increasing/decreasing trends

**Export Options**:
```html
<div class="export-buttons">
    <a href="{{ url_for('export_pdf') }}" class="btn btn-primary">
        Export PDF Report
    </a>
    <a href="{{ url_for('export_csv') }}" class="btn btn-secondary">
        Export CSV Data
    </a>
</div>
```

**Data Visualization**:
- Charts rendered with HTML/CSS (no external libraries)
- Accessible data tables alongside charts
- Print-friendly layout
- Responsive charts for mobile

---

### `login.html` - Login Page

**Purpose**: User authentication page
**Template Extends**: `base.html`
**Lines**: ~132 lines
**Key Features**:

**Login Form**:
```html
<form method="POST">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <input type="checkbox" name="remember"> Remember Me
    <button type="submit">Login</button>
</form>
```

**Security Features**:
- CSRF token protection
- Rate limiting (5 attempts per 5 minutes)
- Account lockout after failed attempts
- Secure password field (no autocomplete on public devices)
- Warning message for failed attempts

**User Experience**:
- Auto-focus username field
- Enter key submits form
- "Remember me" option for trusted devices
- Password visibility toggle
- Link to registration page
- Forgot password link (future)

**Error Handling**:
- Clear error messages for:
  - Invalid username/password
  - Account locked
  - Rate limit exceeded
  - Account inactive
  - Server errors

---

### `register.html` - Registration Page

**Purpose**: New user registration form
**Template Extends**: `base.html`
**Lines**: ~172 lines
**Key Features**:

**Registration Form**:
```html
<form method="POST">
    <input type="text" name="username" required>
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <input type="password" name="confirm_password" required>
    <input type="text" name="full_name">
    <button type="submit">Register</button>
</form>
```

**Password Requirements Display**:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character
- Real-time validation feedback

**Client-Side Validation**:
- Username length and format
- Email format (RFC 5322)
- Password strength meter
- Password confirmation match
- Reserved username blocking

**Server-Side Validation**:
- All client-side rules enforced
- Duplicate username/email detection
- SQL injection prevention
- XSS protection

**User Experience**:
- Progressive disclosure of requirements
- Green checkmarks for met requirements
- Red X for unmet requirements
- Helpful error messages
- Link to login page for existing users

---

### `profile.html` - User Profile

**Purpose**: Display user account information
**Template Extends**: `base.html`
**Lines**: ~148 lines
**Key Features**:

**Profile Information Display**:
```
Username: johndoe
Email: john@example.com
Full Name: John Doe
Role: Resident (badge display)
Account Status: Active (green badge)
Member Since: 2025-10-31
Last Login: 2025-11-01 10:30 AM
```

**Role Badges**:
- Admin: Red badge with crown icon
- Property Manager: Blue badge
- Resident: Green badge

**Account Statistics**:
- Total sightings logged
- Total photos uploaded
- Reports generated
- Account age (days since registration)

**Action Buttons**:
- Change Password (navigates to change_password.html)
- Edit Profile (future feature)
- Download My Data (GDPR compliance, future)
- Delete Account (with confirmation, future)

---

### `change_password.html` - Password Change Form

**Purpose**: Allow users to change their password
**Template Extends**: `base.html`
**Lines**: ~151 lines
**Key Features**:

**Password Change Form**:
```html
<form method="POST">
    <input type="password" name="current_password" required>
    <input type="password" name="new_password" required>
    <input type="password" name="confirm_password" required>
    <button type="submit">Change Password</button>
</form>
```

**Security Requirements**:
- Current password verification (prevents unauthorized changes)
- New password must meet strength requirements
- New password must differ from current
- Confirmation must match new password
- Rate limiting on password change attempts

**User Feedback**:
- Password strength meter for new password
- Real-time validation of requirements
- Success message on change
- Security event logged to audit trail
- User sessions invalidated (re-login required)

---

### `admin_users.html` - User Management Dashboard

**Purpose**: Admin interface for managing user accounts
**Template Extends**: `base.html`
**Lines**: ~209 lines
**Access**: Admin role only
**Key Features**:

**User List Table**:
```
+----+----------+------------------+--------+--------+-------------+
| ID | Username | Email            | Role   | Status | Actions     |
+----+----------+------------------+--------+--------+-------------+
| 1  | admin    | admin@email.com  | Admin  | Active | [Edit] [Del]|
| 2  | johndoe  | john@email.com   | Res.   | Active | [Edit] [Del]|
+----+----------+------------------+--------+--------+-------------+
```

**Filters and Search**:
- Search by username or email
- Filter by role (All, Admin, Resident, Property Manager)
- Filter by status (All, Active, Inactive)
- Sort by: Username, Email, Role, Created Date

**User Actions**:
- View user details
- Edit user (change role, email, name)
- Activate/Deactivate account
- Delete user (with confirmation)
- Reset password (future)
- View user's sightings

**Bulk Actions**:
- Select multiple users
- Bulk activate/deactivate
- Bulk role change
- Bulk delete (with confirmation)

**Create New User**:
- Button navigates to admin_create_user.html
- Admins can create users without email verification

**Statistics**:
- Total users count
- Active users count
- Users by role breakdown
- New users this week/month

---

### `admin_create_user.html` - Create User Form (Admin)

**Purpose**: Admin interface for creating new user accounts
**Template Extends**: `base.html`
**Lines**: ~182 lines
**Access**: Admin role only
**Key Features**:

**Create User Form**:
```html
<form method="POST">
    <input type="text" name="username" required>
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <input type="password" name="confirm_password" required>
    <input type="text" name="full_name">
    <select name="role" required>
        <option value="resident">Resident</option>
        <option value="property_manager">Property Manager</option>
        <option value="admin">Admin</option>
    </select>
    <input type="checkbox" name="is_active" checked> Active Account
    <button type="submit">Create User</button>
</form>
```

**Admin Privileges**:
- Can assign any role (including admin)
- Can create inactive accounts
- Can set initial password
- Can bypass email verification
- Automatically logged to audit trail

**Validation**:
- All standard registration validations apply
- Additional check: prevent creating duplicate admin unnecessarily
- Warns if creating another admin account

**Post-Creation**:
- Success message with username
- Option to create another user
- Option to view all users
- Security event logged

---

## Jinja2 Template Features

### Template Syntax

**Variables**:
```jinja2
{{ variable }}                    # Output variable
{{ user.username }}               # Access object property
{{ sightings|length }}            # Apply filter
```

**Control Structures**:
```jinja2
{% if condition %}                # Conditional
{% elif other_condition %}
{% else %}
{% endif %}

{% for item in items %}           # Loop
{% endfor %}

{% block content %}               # Template block
{% endblock %}
```

**Template Inheritance**:
```jinja2
{% extends "base.html" %}         # Extend base template
{% block content %}               # Override block
    <h1>My Page</h1>
{% endblock %}
```

**Includes**:
```jinja2
{% include "partials/header.html" %}  # Include partial template
```

**URL Generation**:
```jinja2
{{ url_for('index') }}                           # Generate URL for route
{{ url_for('view_sighting', id=sighting.id) }}   # With parameters
{{ url_for('static', filename='css/style.css') }} # Static files
```

**Filters**:
```jinja2
{{ text|upper }}                  # Uppercase
{{ text|lower }}                  # Lowercase
{{ items|length }}                # Length/count
{{ date|strftime('%Y-%m-%d') }}   # Date formatting
{{ text|escape }}                 # HTML escape (auto by default)
{{ text|safe }}                   # Mark as safe HTML (use cautiously)
```

---

## Template Variables Reference

### Global Variables (Available in all templates via base.html)

```python
current_user              # Logged-in user object (Flask-Login)
├── .username            # Username string
├── .email               # Email string
├── .full_name           # Full name string
├── .role                # Role string (admin, resident, property_manager)
├── .is_active           # Boolean active status
├── .is_authenticated    # Boolean (True if logged in)
├── .is_admin()          # Method: returns True if admin role
└── .last_login          # Last login datetime

request                   # Flask request object
├── .method              # HTTP method (GET, POST, etc.)
├── .url                 # Full request URL
├── .path                # URL path
├── .args                # Query string parameters
└── .form                # POST form data

session                   # Flask session object (encrypted cookies)
get_flashed_messages()    # Retrieve flash messages
url_for()                 # Generate URLs for routes
```

### Template-Specific Variables

**index.html**:
```python
recent_sightings         # List of recent sighting dicts
statistics              # Dict with summary stats
```

**view_sightings.html**:
```python
sightings               # List of sighting dicts
total_count             # Total number of sightings
page                    # Current page number
per_page                # Items per page
```

**view_sighting.html** / **edit_sighting.html**:
```python
sighting                # Single sighting dict
├── .id                 # Sighting ID
├── .location           # Location string
├── .count              # Roach count
├── .size               # Size (small/medium/large)
├── .time_of_day        # Time string
├── .weather            # Weather string
├── .notes              # Notes text
├── .photo_path         # Photo file path
├── .date_added         # Datetime
├── .user_id            # Owner user ID
└── .property_id        # Property ID
```

**statistics.html**:
```python
statistics              # Comprehensive stats dict
├── .total_sightings    # Total count
├── .locations          # List of (location, count) tuples
├── .sizes              # Dict of size distribution
├── .times              # Dict of time distribution
├── .weather            # Dict of weather distribution
└── .trend_data         # List of (date, count) for chart
```

**admin_users.html**:
```python
users                   # List of user dicts
filters                 # Current filter settings
total_users             # Total user count
active_users            # Active user count
```

---

## Form Security

### CSRF Protection

All forms include CSRF token:
```jinja2
<form method="POST">
    {{ csrf_token() }}    <!-- CSRF token field (automatic in Flask-WTF) -->
    <!-- OR manually: -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <!-- form fields -->
</form>
```

**How it works**:
1. Server generates unique token per session
2. Token embedded in form as hidden field
3. Token sent with form submission
4. Server validates token matches session
5. Request rejected if token invalid/missing

### Input Sanitization

**Auto-Escaping**:
Jinja2 auto-escapes all variables by default:
```jinja2
{{ user_input }}              <!-- Automatically HTML-escaped -->
{{ user_input|safe }}         <!-- Disable escaping (dangerous!) -->
```

**XSS Prevention**:
- Never use `|safe` filter on user input
- Never use `|safe` on data from database
- Only use `|safe` on trusted, developer-controlled content

**SQL Injection Prevention**:
- Templates don't execute SQL directly
- All queries parameterized in Python backend
- No raw SQL in templates

---

## Responsive Design

### Mobile-First Approach

All templates designed mobile-first with progressive enhancement:

**Breakpoints**:
```css
/* Mobile (default): < 768px */
/* Tablet: 768px - 1024px */
/* Desktop: > 1024px */
```

**Responsive Patterns**:
1. **Navigation**: Hamburger menu on mobile, full navbar on desktop
2. **Cards**: Stack vertically on mobile, grid on desktop
3. **Tables**: Horizontal scroll on mobile, full table on desktop
4. **Forms**: Full-width inputs on mobile, multi-column on desktop
5. **Images**: Scale to container width on all devices

**Viewport Meta Tag**:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
```

---

## Accessibility Features

### WCAG 2.1 Compliance

**Semantic HTML**:
- Proper heading hierarchy (`<h1>` to `<h6>`)
- Semantic elements (`<nav>`, `<main>`, `<footer>`, `<article>`)
- Lists for navigation and data
- Tables for tabular data with proper headers

**ARIA Labels**:
```html
<button aria-label="Toggle navigation">
<input aria-describedby="username-help">
<div role="alert">Error message</div>
```

**Keyboard Navigation**:
- All interactive elements keyboard accessible
- Logical tab order
- Focus visible styles
- Skip navigation links

**Color Contrast**:
- WCAG AA compliant contrast ratios
- Text: minimum 4.5:1
- Large text: minimum 3:1
- Buttons and links clearly distinguishable

**Form Labels**:
```html
<label for="location">Location:</label>
<input type="text" id="location" name="location">
```

**Alt Text**:
```html
<img src="{{ photo_path }}" alt="Roach sighting in {{ location }}">
```

---

## Performance Optimizations

### Template Rendering

**Caching**:
- Template compilation cached by Flask
- Static files served with cache headers
- Browser caching enabled for CSS/JS

**Lazy Loading**:
```html
<img src="placeholder.jpg" data-src="{{ photo_path }}" loading="lazy">
```

**Pagination**:
- Large datasets paginated (20 items per page)
- Prevents rendering hundreds of rows
- Improves page load time significantly

**Minification** (Production):
- HTML minified by Flask-Minify (optional)
- Removes whitespace and comments
- Reduces page size by 20-30%

---

## Development Guidelines

### Template Best Practices

1. **Keep Logic Minimal**:
   - Complex logic belongs in Python backend
   - Templates should only display data
   - Use template filters for simple formatting

2. **Use Template Inheritance**:
   - All pages extend `base.html`
   - Consistent navigation and footer
   - DRY principle (Don't Repeat Yourself)

3. **Organize Blocks Logically**:
   - `{% block title %}` for page title
   - `{% block content %}` for main content
   - `{% block extra_scripts %}` for page-specific JavaScript

4. **Escape User Input**:
   - Never use `|safe` on user-generated content
   - Always validate and sanitize in backend
   - Trust Jinja2's auto-escaping

5. **Mobile-First**:
   - Design for mobile screens first
   - Progressive enhancement for larger screens
   - Test on real devices

6. **Accessibility First**:
   - Use semantic HTML
   - Include ARIA labels where needed
   - Ensure keyboard navigation works
   - Test with screen readers

---

## Testing Recommendations

### Manual Testing

**Browser Testing**:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Android)

**Viewport Testing**:
- 320px (iPhone SE)
- 375px (iPhone 12/13)
- 768px (iPad portrait)
- 1024px (iPad landscape)
- 1920px (Desktop)

**Accessibility Testing**:
- NVDA screen reader (Windows)
- VoiceOver (macOS/iOS)
- Keyboard-only navigation
- Color contrast analyzers
- WAVE accessibility checker

### Automated Testing

**Template Syntax**:
```python
# test_templates.py
def test_template_renders():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Roach Tracker' in response.data
```

**HTML Validation**:
- W3C HTML Validator
- Check for syntax errors
- Ensure proper nesting

---

## Common Issues & Solutions

### Template Not Found

**Error**: `jinja2.exceptions.TemplateNotFound: index.html`
**Solution**: Ensure templates directory is at project root, not inside `app/`

### Variable Undefined

**Error**: `jinja2.exceptions.UndefinedError: 'sighting' is undefined`
**Solution**: Ensure variable passed from Flask route:
```python
return render_template('view_sighting.html', sighting=sighting)
```

### URL Not Found

**Error**: `werkzeug.routing.BuildError: Could not build url for endpoint 'index'`
**Solution**: Ensure route exists in `app/main.py` with correct name

### Form Not Submitting

**Issue**: Form submits but data not processed
**Solution**:
- Check `method="POST"` on form
- Ensure `name` attributes on all inputs
- Verify route accepts POST: `@app.route('/login', methods=['GET', 'POST'])`

### Images Not Loading

**Issue**: Photos show broken image icon
**Solution**:
- Verify `static/uploads/` directory exists
- Check file permissions (readable by web server)
- Ensure correct path in database
- Use `url_for('static', filename='uploads/' + photo_path)`

---

## Related Documentation

- [Static Assets README](../static/README.md) - CSS and JavaScript documentation
- [Application Backend README](../app/README.md) - Flask routes and logic
- [Main README](../README.md) - Project overview

---

## Version History

### v1.2.0 (2025-10-31)
- Added `profile.html` - User profile page
- Added `change_password.html` - Password change form
- Enhanced error handlers (403, 404, 500 templates)
- Improved accessibility with ARIA labels
- Mobile navigation improvements

### v1.1.0 (2025-10-31)
- Added `login.html` - User login page
- Added `register.html` - User registration
- Added `admin_users.html` - User management dashboard
- Added `admin_create_user.html` - Admin user creation form
- Updated `base.html` with authentication-aware navigation
- Added role badges and user info display

### v1.0.0 (2025-10-31)
- Initial template implementation
- Created `base.html` master template
- Created sighting templates (log, view, edit)
- Created `statistics.html` analytics page
- Mobile-responsive design
- Flash message system

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
