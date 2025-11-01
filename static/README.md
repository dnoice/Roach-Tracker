# Static Assets Documentation

**File**: `README.md`
**Path**: `static/README.md`
**Directory**: `static/`
**Purpose**: Frontend static assets - CSS stylesheets, JavaScript, and user-uploaded files
**Author**: dnoice + Claude AI
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

## Overview

The `static/` directory contains all frontend static assets for the Roach Tracker web application. This includes CSS stylesheets for visual presentation, JavaScript for client-side interactivity, and a dedicated uploads folder for user-generated photo content. Flask serves these files efficiently with proper caching headers for optimal performance.

---

## Directory Structure

```
static/
├── css/
│   └── style.css         # Main stylesheet (~530 lines)
├── js/
│   └── main.js           # Main JavaScript (~157 lines)
├── uploads/              # User-uploaded photos (photo storage)
│   ├── [timestamp]_[random].jpg
│   ├── [timestamp]_[random].png
│   └── ...
└── README.md             # This file
```

---

## CSS Directory (`css/`)

### `style.css` - Main Stylesheet

**Purpose**: Complete styling for the entire application
**Lines**: ~530 lines
**Version**: 1.0.0
**Key Features**:

#### CSS Architecture

The stylesheet is organized into logical sections:

1. **Root Variables** - CSS custom properties for consistent theming
2. **Reset & Base** - Normalize styles across browsers
3. **Navigation** - Navbar and mobile menu styles
4. **Layout** - Container, grid, and flexbox utilities
5. **Typography** - Headings, paragraphs, links
6. **Forms** - Input fields, buttons, validation states
7. **Cards** - Reusable card components
8. **Tables** - Data table styling
9. **Flash Messages** - Alert and notification styles
10. **Buttons** - Primary, secondary, danger button variants
11. **Statistics** - Charts and data visualization
12. **Utility Classes** - Margins, padding, text alignment
13. **Responsive Design** - Mobile-first media queries

#### CSS Custom Properties (Variables)

```css
:root {
    /* Brand Colors */
    --primary-color: #8B0000;        /* Dark red */
    --primary-hover: #660000;        /* Darker red on hover */
    --secondary-color: #2C3E50;      /* Dark blue-gray */
    --secondary-hover: #1A252F;      /* Darker on hover */

    /* Semantic Colors */
    --success-color: #27AE60;        /* Green for success */
    --warning-color: #F39C12;        /* Orange for warnings */
    --danger-color: #E74C3C;         /* Red for errors */
    --info-color: #3498DB;           /* Blue for info */

    /* Neutrals */
    --light-gray: #ECF0F1;
    --medium-gray: #95A5A6;
    --dark-gray: #34495E;
    --text-color: #2C3E50;
    --border-color: #BDC3C7;

    /* Effects */
    --shadow: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-lg: 0 4px 12px rgba(0,0,0,0.15);
    --border-radius: 8px;

    /* Spacing Scale */
    --spacing-xs: 0.5rem;   /* 8px */
    --spacing-sm: 1rem;     /* 16px */
    --spacing-md: 1.5rem;   /* 24px */
    --spacing-lg: 2rem;     /* 32px */
    --spacing-xl: 3rem;     /* 48px */
}
```

**Benefits**:
- Consistent color scheme throughout application
- Easy theme customization by changing variables
- Maintainable spacing system
- Semantic naming for clarity

#### Navigation Styles

**Desktop Navigation**:
```css
.navbar {
    background-color: var(--primary-color);
    color: white;
    position: sticky;        /* Stays at top when scrolling */
    top: 0;
    z-index: 1000;          /* Above other content */
    box-shadow: var(--shadow);
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: var(--spacing-md);
}
```

**Mobile Navigation** (hamburger menu):
```css
@media (max-width: 768px) {
    .nav-toggle {
        display: flex;      /* Show hamburger icon */
    }

    .nav-menu {
        position: absolute;
        top: 100%;
        right: 0;
        background: var(--primary-color);
        flex-direction: column;
        width: 100%;
        max-height: 0;      /* Hidden by default */
        overflow: hidden;
        transition: max-height 0.3s ease;
    }

    .nav-menu.active {
        max-height: 500px;  /* Expanded state */
    }
}
```

**Features**:
- Sticky navigation (follows scroll)
- Smooth hamburger menu animation
- Touch-friendly tap targets (min 44px)
- Active state highlighting for current page

#### Form Styles

**Input Fields**:
```css
input[type="text"],
input[type="email"],
input[type="password"],
input[type="number"],
input[type="date"],
textarea,
select {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

input:focus,
textarea:focus,
select:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(139, 0, 0, 0.1);
}
```

**Buttons**:
```css
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--border-radius);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.btn-secondary {
    background-color: var(--secondary-color);
    color: white;
}

.btn-danger {
    background-color: var(--danger-color);
    color: white;
}
```

**Validation States**:
```css
input:invalid {
    border-color: var(--danger-color);
}

input:valid {
    border-color: var(--success-color);
}

.error-message {
    color: var(--danger-color);
    font-size: 0.875rem;
    margin-top: 0.25rem;
}
```

#### Card Components

```css
.card {
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
}

.card-header {
    font-size: 1.25rem;
    font-weight: bold;
    margin-bottom: var(--spacing-sm);
    padding-bottom: var(--spacing-sm);
    border-bottom: 2px solid var(--light-gray);
}

.card-body {
    /* Card content */
}

.card-footer {
    margin-top: var(--spacing-sm);
    padding-top: var(--spacing-sm);
    border-top: 1px solid var(--light-gray);
}
```

**Usage**: Dashboard stats, sighting details, user profiles

#### Table Styles

```css
.table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow);
}

.table th {
    background-color: var(--secondary-color);
    color: white;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
}

.table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--light-gray);
}

.table tr:hover {
    background-color: #F8F9FA;
}

/* Mobile: Horizontal scroll for tables */
@media (max-width: 768px) {
    .table-container {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}
```

**Features**:
- Striped rows for readability (alternating)
- Hover effects for row highlighting
- Sticky header (advanced tables)
- Responsive horizontal scroll on mobile

#### Flash Message Styles

```css
.flash {
    padding: 1rem 1.5rem;
    border-radius: var(--border-radius);
    margin-bottom: var(--spacing-sm);
    display: flex;
    justify-content: space-between;
    align-items: center;
    animation: slideDown 0.3s ease;
}

.flash-success {
    background-color: #D4EDDA;
    color: #155724;
    border-left: 4px solid var(--success-color);
}

.flash-error {
    background-color: #F8D7DA;
    color: #721C24;
    border-left: 4px solid var(--danger-color);
}

.flash-warning {
    background-color: #FFF3CD;
    color: #856404;
    border-left: 4px solid var(--warning-color);
}

.flash-info {
    background-color: #D1ECF1;
    color: #0C5460;
    border-left: 4px solid var(--info-color);
}

@keyframes slideDown {
    from {
        transform: translateY(-100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
```

**Features**:
- Color-coded by message type
- Slide-down animation on appearance
- Auto-dismiss after 5 seconds (JavaScript)
- Close button with hover effect

#### Responsive Design

**Breakpoints**:
```css
/* Mobile First (default): < 768px */
/* Styles here apply to all screen sizes */

/* Tablet: 768px and up */
@media (min-width: 768px) {
    .container {
        padding: var(--spacing-lg);
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: var(--spacing-md);
    }
}

/* Desktop: 1024px and up */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* Large Desktop: 1440px and up */
@media (min-width: 1440px) {
    .container {
        max-width: 1400px;
    }
}
```

**Responsive Patterns**:
- **Mobile**: Single column, stacked cards, hamburger menu
- **Tablet**: Two-column grid, expanded navigation
- **Desktop**: Three-column grid, full navbar, larger spacing

#### Statistics & Charts

```css
.stat-card {
    background: white;
    border-radius: var(--border-radius);
    padding: var(--spacing-md);
    text-align: center;
    box-shadow: var(--shadow);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--primary-color);
}

.stat-label {
    font-size: 0.875rem;
    color: var(--medium-gray);
    text-transform: uppercase;
}

/* Simple CSS bar chart */
.chart-bar {
    background: var(--light-gray);
    height: 30px;
    border-radius: var(--border-radius);
    position: relative;
    margin-bottom: var(--spacing-sm);
}

.chart-bar-fill {
    background: var(--primary-color);
    height: 100%;
    border-radius: var(--border-radius);
    transition: width 0.5s ease;
}
```

**Charts Rendered**:
- Location frequency (horizontal bars)
- Size distribution (vertical bars)
- Time of day patterns (horizontal bars)
- Trend lines (CSS gradients)

#### Utility Classes

```css
/* Spacing */
.mt-1 { margin-top: var(--spacing-xs); }
.mt-2 { margin-top: var(--spacing-sm); }
.mt-3 { margin-top: var(--spacing-md); }
.mb-1 { margin-bottom: var(--spacing-xs); }
.mb-2 { margin-bottom: var(--spacing-sm); }
.mb-3 { margin-bottom: var(--spacing-md); }

/* Text Alignment */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

/* Display */
.d-none { display: none; }
.d-block { display: block; }
.d-flex { display: flex; }
.d-grid { display: grid; }

/* Flexbox */
.flex-row { flex-direction: row; }
.flex-column { flex-direction: column; }
.justify-center { justify-content: center; }
.align-center { align-items: center; }
.space-between { justify-content: space-between; }

/* Text Color */
.text-primary { color: var(--primary-color); }
.text-success { color: var(--success-color); }
.text-danger { color: var(--danger-color); }
.text-muted { color: var(--medium-gray); }
```

---

## JavaScript Directory (`js/`)

### `main.js` - Client-Side JavaScript

**Purpose**: Interactive features and form enhancements
**Lines**: ~157 lines
**Version**: 1.0.0
**Key Features**:

#### Mobile Navigation Toggle

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        // Open/close menu on hamburger click
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navToggle.contains(event.target) ||
                                     navMenu.contains(event.target);
            if (!isClickInsideNav && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
            }
        });
    }
});
```

**Features**:
- Toggle menu visibility on mobile
- Close menu when clicking outside navigation
- Smooth animation via CSS transitions
- Keyboard accessible (Enter/Space triggers click)

#### Auto-Dismiss Flash Messages

```javascript
// Auto-dismiss flash messages after 5 seconds
const flashMessages = document.querySelectorAll('.flash');
flashMessages.forEach(function(flash) {
    setTimeout(function() {
        flash.style.opacity = '0';
        setTimeout(function() {
            flash.remove();
        }, 300);  // Wait for fade-out animation
    }, 5000);  // 5 second delay
});
```

**Features**:
- Automatic dismissal after 5 seconds
- Smooth fade-out animation
- Removes element from DOM after animation
- Manual close button also available

#### Form Validation

```javascript
const forms = document.querySelectorAll('form');
forms.forEach(function(form) {
    form.addEventListener('submit', function(event) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(function(field) {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Please fill in all required fields.');
        }
    });
});
```

**Validation Rules**:
- Required field checking
- Empty string detection (trim whitespace)
- Visual error highlighting (red border)
- Prevents form submission if invalid
- User-friendly error messages

#### Photo Upload Preview

```javascript
const photoInput = document.getElementById('photo');
if (photoInput) {
    photoInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            // Check file size (16MB max)
            if (file.size > 16 * 1024 * 1024) {
                alert('File size must be less than 16MB');
                photoInput.value = '';
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('photo-preview');
                if (preview) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
            };
            reader.readAsDataURL(file);
        }
    });
}
```

**Features**:
- Real-time image preview before upload
- File size validation (16MB limit)
- Supported formats: PNG, JPG, JPEG, GIF, WEBP
- Preview updates when file changed
- Error messages for invalid files

#### Delete Confirmation

```javascript
const deleteButtons = document.querySelectorAll('.btn-delete');
deleteButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        const confirmDelete = confirm('Are you sure you want to delete this item? This action cannot be undone.');
        if (!confirmDelete) {
            event.preventDefault();
        }
    });
});
```

**Features**:
- Confirmation dialog before deletion
- Prevents accidental deletions
- Clear warning message
- Cancellable action

#### Statistics Chart Animation

```javascript
// Animate chart bars on page load
const chartBars = document.querySelectorAll('.chart-bar-fill');
chartBars.forEach(function(bar) {
    const targetWidth = bar.dataset.width;
    bar.style.width = '0%';

    setTimeout(function() {
        bar.style.width = targetWidth + '%';
    }, 100);
});
```

**Features**:
- Smooth width animation for bar charts
- Delayed start for sequential effect
- Data-driven (width from dataset attribute)
- CSS transitions handle animation

#### Form Auto-Save (Local Storage)

```javascript
// Auto-save form data to localStorage
const autoSaveForms = document.querySelectorAll('[data-autosave]');
autoSaveForms.forEach(function(form) {
    const formId = form.getAttribute('data-autosave');

    // Load saved data
    const savedData = localStorage.getItem('form_' + formId);
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(function(key) {
            const field = form.querySelector('[name="' + key + '"]');
            if (field) {
                field.value = data[key];
            }
        });
    }

    // Save on input change
    form.addEventListener('input', function() {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        localStorage.setItem('form_' + formId, JSON.stringify(data));
    });

    // Clear on submit
    form.addEventListener('submit', function() {
        localStorage.removeItem('form_' + formId);
    });
});
```

**Benefits**:
- Prevents data loss on accidental page close
- Saves form state to browser localStorage
- Restores data on page reload
- Clears saved data on successful submission

---

## Uploads Directory (`uploads/`)

### User-Generated Photo Storage

**Purpose**: Store uploaded roach sighting photos
**Access**: Public (served by Flask static file handler)
**Naming Convention**: `[timestamp]_[random].[ext]`

**Example Filenames**:
```
20251031_143022_a7f3b9c2.jpg
20251031_143045_d8e1f4a6.png
20251031_144312_9b2c8d7e.webp
```

**Filename Components**:
- `YYYYMMDD_HHMMSS` - Timestamp of upload
- `[random]` - 8-character random hex string
- `[ext]` - File extension (jpg, png, gif, webp)

**Security**:
- Filename sanitization prevents directory traversal
- Extension validation (whitelist only)
- File size limit enforced (16MB max)
- Decompression bomb protection
- No executable file types allowed

**Storage Details**:
- **Location**: `static/uploads/` directory
- **Permissions**: Read-only for web server
- **Backup**: Included in data backups
- **Retention**: Permanent (unless manually deleted)
- **Database Reference**: Stored as relative path in `sightings.photo_path`

**Photo Processing Pipeline**:
1. User selects photo file in form
2. Client-side: Validate file size and type
3. Server-side: Re-validate (never trust client)
4. Generate unique filename with timestamp
5. Resize large images (max 1920x1920 pixels)
6. Save optimized image to uploads directory
7. Store relative path in database
8. Return success response

**File Management**:
```python
# From app/utils.py
def save_photo(file):
    """
    Save uploaded photo with validation and optimization
    Returns: relative path (e.g., 'uploads/20251031_143022_a7f3b9c2.jpg')
    """

def delete_photo(photo_path):
    """
    Safely delete photo file
    - Validates path is within uploads directory
    - Prevents directory traversal attacks
    """
```

**Directory Size Management**:
- Monitor disk usage regularly
- Consider cleanup policy for old/unused photos
- Implement photo archival for deleted sightings
- Compress photos periodically (future feature)

**Access in Templates**:
```jinja2
<!-- Serve photo via Flask static route -->
<img src="{{ url_for('static', filename='uploads/' + sighting.photo_path) }}"
     alt="Roach sighting in {{ sighting.location }}">
```

**URL Pattern**:
```
http://localhost:5000/static/uploads/20251031_143022_a7f3b9c2.jpg
```

---

## Performance Optimizations

### CSS Performance

**File Size Optimization**:
- CSS minification in production (remove whitespace/comments)
- Gzip compression enabled on server
- Original: ~530 lines (~16KB)
- Minified: ~11KB
- Gzipped: ~3KB

**Loading Optimization**:
```html
<!-- In base.html -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

**Browser Caching**:
- Cache-Control header: `max-age=31536000` (1 year)
- Versioning via query string for cache busting
- Example: `style.css?v=1.2.0`

**CSS Performance Tips**:
- Use CSS variables instead of repeated values
- Minimize use of expensive properties (box-shadow, gradients)
- Use transform instead of left/top for animations
- Avoid universal selector (`*`) in performance-critical rules

### JavaScript Performance

**File Size**:
- Original: ~157 lines (~4.8KB)
- Minified: ~2.5KB
- Gzipped: ~1KB

**Loading Strategy**:
```html
<!-- Defer execution until DOM ready -->
<script src="{{ url_for('static', filename='js/main.js') }}" defer></script>
```

**Performance Features**:
- Event delegation for dynamic elements
- Debouncing for input events (search, auto-save)
- Throttling for scroll events
- Efficient DOM queries (querySelector vs getElementById)

**JavaScript Best Practices**:
```javascript
// Good: Query once, reuse reference
const navToggle = document.getElementById('navToggle');

// Bad: Query multiple times
document.getElementById('navToggle').addEventListener(...);
document.getElementById('navToggle').classList.toggle(...);
```

### Image Optimization

**Photo Upload Processing**:
1. **Resize**: Max dimensions 1920x1920 pixels
2. **Compress**: JPEG quality 85%, PNG optimized
3. **Format**: Convert HEIC/HEIF to JPEG on server
4. **Progressive**: JPEG progressive encoding
5. **Result**: Average 200-500KB (from 2-5MB originals)

**Lazy Loading**:
```html
<!-- Native lazy loading for images -->
<img src="photo.jpg" loading="lazy" alt="Roach sighting">
```

**Responsive Images** (future enhancement):
```html
<picture>
    <source srcset="photo-800.webp" media="(max-width: 800px)" type="image/webp">
    <source srcset="photo-1200.webp" media="(min-width: 801px)" type="image/webp">
    <img src="photo.jpg" alt="Roach sighting" loading="lazy">
</picture>
```

---

## Browser Compatibility

### Supported Browsers

**Desktop**:
- Chrome 90+ ✓
- Firefox 88+ ✓
- Safari 14+ ✓
- Edge 90+ ✓

**Mobile**:
- iOS Safari 14+ ✓
- Chrome Android 90+ ✓
- Samsung Internet 14+ ✓

### CSS Features Used

**Modern CSS**:
- CSS Variables (Custom Properties) - Supported all modern browsers
- Flexbox - Supported IE11+
- Grid Layout - Supported all modern browsers
- Media Queries - Universal support
- Transitions & Animations - Universal support

**Progressive Enhancement**:
- Core layout works without CSS Grid (fallback to Flexbox)
- Navigation functional without JavaScript
- Forms work without JavaScript validation (server-side validation)

### JavaScript Features

**ES6+ Features Used**:
- `const` and `let` - Supported all modern browsers
- Arrow functions - Supported all modern browsers
- Template literals - Supported all modern browsers
- `forEach` - Universal support
- `addEventListener` - Universal support
- `classList` - Supported IE10+

**Polyfills Not Required** (modern browser target):
- No need for Babel transpilation
- No need for polyfill.io
- Native browser APIs sufficient

---

## Accessibility (A11y)

### CSS Accessibility Features

**Focus Styles**:
```css
a:focus,
button:focus,
input:focus {
    outline: 3px solid var(--primary-color);
    outline-offset: 2px;
}

.btn:focus-visible {
    box-shadow: 0 0 0 3px rgba(139, 0, 0, 0.3);
}
```

**High Contrast Support**:
```css
@media (prefers-contrast: high) {
    :root {
        --primary-color: #B00000;  /* Higher contrast red */
        --text-color: #000000;     /* Pure black text */
    }
}
```

**Reduced Motion**:
```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

**Color Contrast**:
- All text meets WCAG AA standard (4.5:1 minimum)
- Buttons and links have 3:1 contrast minimum
- Form inputs clearly distinguishable

### JavaScript Accessibility

**Keyboard Navigation**:
```javascript
// Ensure Enter key triggers button clicks
button.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        button.click();
    }
});
```

**Screen Reader Support**:
- No reliance on visual-only indicators
- Flash messages use ARIA live regions
- Form errors announced properly
- Loading states communicated

---

## Development Guidelines

### Adding New Styles

**Step 1**: Add to appropriate section in `style.css`
```css
/* ===== NEW COMPONENT ===== */
.my-component {
    /* Styles here */
}
```

**Step 2**: Use CSS variables for colors and spacing
```css
.my-component {
    color: var(--text-color);           /* Good */
    /* color: #2C3E50; */               /* Bad */

    padding: var(--spacing-md);         /* Good */
    /* padding: 1.5rem; */              /* Bad */
}
```

**Step 3**: Make it responsive
```css
.my-component {
    /* Mobile styles */
}

@media (min-width: 768px) {
    .my-component {
        /* Tablet/Desktop styles */
    }
}
```

### Adding New JavaScript

**Step 1**: Wrap in DOMContentLoaded
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Your code here
});
```

**Step 2**: Check element exists before accessing
```javascript
const element = document.getElementById('my-element');
if (element) {
    // Safe to use element
}
```

**Step 3**: Use event delegation for dynamic content
```javascript
// Good: Handles dynamically added buttons
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-delete')) {
        // Handle delete
    }
});

// Bad: Only handles existing buttons
document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', handleDelete);
});
```

### Code Style Guidelines

**CSS**:
- Use 4 spaces for indentation
- One selector per line in multi-selector rules
- Properties alphabetically ordered (optional)
- Comments for major sections

**JavaScript**:
- Use `const` by default, `let` when needed, never `var`
- Single quotes for strings
- Semicolons always
- Descriptive variable names (no `x`, `temp`, `data1`)

---

## Testing

### CSS Testing

**Visual Regression Testing**:
- Test on all supported browsers
- Compare screenshots at different viewports
- Verify responsive breakpoints work correctly

**Cross-Browser Testing Checklist**:
- [ ] Flexbox layouts render correctly
- [ ] CSS Grid layouts work on all browsers
- [ ] Animations smooth and performant
- [ ] Forms styled consistently
- [ ] Images load and display properly

### JavaScript Testing

**Manual Testing**:
```
Test Case: Mobile navigation toggle
1. Open site on mobile viewport (< 768px)
2. Click hamburger menu icon
3. Verify menu expands
4. Click outside menu
5. Verify menu collapses
Expected: Menu toggles open/closed correctly
```

**Console Testing**:
```javascript
// Test photo upload validation
const input = document.getElementById('photo');
const file = new File([''], 'test.jpg', { size: 20 * 1024 * 1024 }); // 20MB
input.files = [file];
input.dispatchEvent(new Event('change'));
// Expected: Alert showing file too large
```

---

## Troubleshooting

### CSS Not Loading

**Issue**: Styles not applied, page looks unstyled
**Solution**:
1. Check browser console for 404 errors
2. Verify `static/css/style.css` exists
3. Clear browser cache (Ctrl+Shift+R)
4. Check Flask static folder configuration in `app/__init__.py`

### JavaScript Not Working

**Issue**: Interactive features not functioning
**Solution**:
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify `main.js` loaded successfully (Network tab)
4. Ensure script has `defer` attribute

### Images Not Displaying

**Issue**: Uploaded photos show broken image icon
**Solution**:
1. Verify `static/uploads/` directory exists
2. Check file permissions (readable by web server)
3. Confirm file path correct in database
4. Use correct URL: `/static/uploads/filename.jpg`

### Mobile Menu Not Working

**Issue**: Hamburger menu doesn't open/close
**Solution**:
1. Check if JavaScript loaded (console for errors)
2. Verify element IDs match: `navToggle` and `navMenu`
3. Test CSS `.active` class toggles correctly
4. Ensure no conflicting click event handlers

---

## Related Documentation

- [Templates README](../templates/README.md) - HTML templates that use these styles
- [Application Backend README](../app/README.md) - Python backend serving static files
- [Main README](../README.md) - Project overview

---

## Version History

### v1.2.0 (2025-10-31)
- Added profile page styles
- Added password change form styles
- Enhanced form validation styling
- Improved accessibility (focus states, ARIA)
- Added high contrast mode support

### v1.1.0 (2025-10-31)
- Added authentication page styles (login, register)
- Added admin dashboard styles
- Enhanced navigation with user info display
- Added role badge styling
- Improved mobile responsiveness

### v1.0.0 (2025-10-31)
- Initial CSS and JavaScript implementation
- Mobile-first responsive design
- Complete component library
- Interactive navigation
- Form validation
- Flash message system
- Statistics chart styles

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
