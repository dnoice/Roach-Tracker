**File**: `ARCHITECTURE.md`
**Path**: `docs/ARCHITECTURE.md`
**Purpose**: System architecture, technical design, and structural documentation
**Author**: dnoice + Claude AI
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

# Architecture Documentation

**Roach Tracker - Technical Design and Structure**

---

## System Overview

Roach Tracker is a local-first web application built with Flask (Python) that provides a complete pest documentation system. The architecture emphasizes simplicity, privacy, and mobile responsiveness.

### Design Principles

1. **Local-First**: All data stored locally, no external dependencies
2. **Privacy-Focused**: No tracking, analytics, or cloud services
3. **Mobile-Responsive**: Touch-optimized interface for phones/tablets
4. **Zero-Config**: Automated setup with sensible defaults
5. **Self-Contained**: Single SQLite database, no external services

---

## Technology Stack

### Backend

- **Framework**: Flask 3.0.0
- **Language**: Python 3.8+
- **Database**: SQLite 3
- **Image Processing**: Pillow 10.1.0
- **PDF Generation**: ReportLab 4.0.7
- **Environment**: python-dotenv 1.0.0

### Frontend

- **HTML5**: Semantic markup
- **CSS3**: Custom responsive styles, CSS Grid, Flexbox
- **JavaScript**: Vanilla ES6+ (no frameworks)
- **Icons**: Inline SVG (following Rule #4: No emojis in UI)

### Development Tools

- **Bash Scripts**: Automated setup and deployment
- **Git**: Version control
- **Virtual Environment**: Isolated Python dependencies

---

## Application Structure

```
Roach-Tracker/
├── app/
│   ├── __init__.py       # Flask application factory
│   ├── main.py           # Routes and view functions
│   ├── models.py         # Database models and operations
│   └── utils.py          # Helper functions
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base layout template
│   ├── index.html        # Dashboard
│   ├── log_sighting.html # Sighting entry form
│   ├── view_sightings.html # All sightings list
│   ├── view_sighting.html  # Single sighting detail
│   ├── edit_sighting.html  # Edit form
│   └── statistics.html   # Analytics dashboard
├── static/
│   ├── css/
│   │   └── style.css     # Responsive styles
│   ├── js/
│   │   └── main.js       # Client-side JavaScript
│   └── uploads/          # Photo storage
├── data/
│   └── roach_tracker.db  # SQLite database
├── exports/              # Generated reports
└── docs/branches/        # AI continuity logs
```

---

## Database Schema

### Sightings Table

```sql
CREATE TABLE sightings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    location TEXT NOT NULL,
    room_type TEXT,
    roach_count INTEGER DEFAULT 1,
    roach_size TEXT,
    roach_type TEXT,
    photo_path TEXT,
    notes TEXT,
    weather TEXT,
    temperature REAL,
    time_of_day TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

### Field Descriptions

- **id**: Auto-incrementing primary key
- **timestamp**: ISO 8601 datetime of sighting
- **location**: User-defined location string
- **room_type**: Categorized room (Kitchen, Bathroom, etc.)
- **roach_count**: Number of roaches observed
- **roach_size**: Size category (Small, Medium, Large, Very Large)
- **roach_type**: Species if known
- **photo_path**: Relative path to uploaded photo
- **notes**: Free-form text observations
- **weather**: Weather conditions
- **temperature**: Temperature in Fahrenheit
- **time_of_day**: Auto-calculated (Morning/Afternoon/Evening/Night)
- **created_at**: Record creation timestamp
- **updated_at**: Last modification timestamp

---

## Module Breakdown

### app/__init__.py

**Purpose**: Flask application factory

**Responsibilities**:
- Create Flask app instance
- Configure app settings from environment
- Register routes from main.py
- Ensure required directories exist

**Key Configuration**:
```python
SECRET_KEY: Session security (from .env)
DATABASE: SQLite path (default: data/roach_tracker.db)
UPLOAD_FOLDER: Photo storage (default: static/uploads)
MAX_CONTENT_LENGTH: 16MB upload limit
ALLOWED_EXTENSIONS: {png, jpg, jpeg, gif, webp}
```

### app/models.py

**Purpose**: Database operations layer

**Key Classes**:
- `Database`: SQLite connection manager

**Key Methods**:
- `init_database()`: Create schema
- `create_sighting()`: Insert new record
- `get_sighting()`: Fetch single record
- `get_all_sightings()`: Fetch with pagination
- `update_sighting()`: Modify existing record
- `delete_sighting()`: Remove record
- `get_statistics()`: Calculate analytics
- `search_sightings()`: Full-text search

**Design Pattern**: Context manager for automatic connection handling

### app/utils.py

**Purpose**: Helper functions for file processing and reporting

**Key Functions**:

1. **Photo Processing**
   - `allowed_file()`: Validate file extensions
   - `process_and_save_photo()`: Resize and optimize images
   - Uses Pillow for image manipulation
   - Converts RGBA to RGB
   - Maintains aspect ratio with thumbnail()
   - Saves as optimized JPEG (quality 85)

2. **Report Generation**
   - `generate_pdf_report()`: Professional PDF with ReportLab
   - `generate_csv_export()`: CSV with all fields
   - Includes photos, statistics, and formatting

3. **Utilities**
   - `format_timestamp()`: Human-readable dates
   - `get_time_of_day()`: Auto-categorize time

### app/main.py

**Purpose**: Route definitions and request handling

**Routes**:

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Dashboard |
| `/log` | GET, POST | Log new sighting |
| `/sightings` | GET | View all sightings |
| `/sighting/<id>` | GET | View single sighting |
| `/sighting/<id>/edit` | GET, POST | Edit sighting |
| `/sighting/<id>/delete` | POST | Delete sighting |
| `/statistics` | GET | Analytics dashboard |
| `/export/pdf` | GET | Generate PDF report |
| `/export/csv` | GET | Generate CSV export |

**Error Handlers**:
- 404: Not Found
- 500: Internal Server Error

---

## Frontend Architecture

### Template Inheritance

```
base.html (layout)
  ├── index.html
  ├── log_sighting.html
  ├── view_sightings.html
  ├── view_sighting.html
  ├── edit_sighting.html
  └── statistics.html
```

### CSS Architecture

**Approach**: Utility-first with component classes

**Key Features**:
- CSS Custom Properties (variables)
- Mobile-first responsive design
- Flexbox and Grid layouts
- No external frameworks
- Touch-optimized (44px minimum tap targets)

**Responsive Breakpoints**:
- Desktop: > 768px
- Tablet: 481px - 768px
- Mobile: < 480px

### JavaScript Architecture

**Approach**: Progressive enhancement, vanilla JS

**Features**:
- Mobile navigation toggle
- Flash message auto-dismiss
- Form validation
- Photo preview
- Smooth scrolling
- Intersection Observer for animations
- No external dependencies

---

## Data Flow

### Creating a Sighting

1. User submits form (POST /log)
2. Flask validates required fields
3. Photo processed and saved (if present)
4. Data inserted into database
5. Redirect to sighting detail page
6. Flash success message

### Generating Reports

1. User clicks export (GET /export/pdf)
2. All sightings fetched from database
3. PDF generated with ReportLab
4. File saved to exports/
5. File sent as download
6. Browser triggers save dialog

### Search Flow

1. User enters query (GET /sightings?q=kitchen)
2. Database searches location and notes fields
3. Results rendered in template
4. Highlighting applied to matches

---

## Security Considerations

### Input Validation

- All user input sanitized
- File extensions whitelisted
- File size limits enforced
- SQL injection prevented (parameterized queries)

### Photo Handling

- Secure filename generation
- MIME type validation
- Size restrictions (16MB)
- Format conversion (RGBA → RGB)
- No executable files accepted

### Session Security

- Secret key from environment
- CSRF protection via Flask defaults
- No authentication (local-only app)

---

## Performance Optimizations

### Database

- Indexed primary keys
- Efficient queries (no N+1)
- Context managers for connections
- Row factory for dict conversion

### Photos

- Automatic resizing (max 1200x1200)
- JPEG optimization (quality 85)
- Lazy loading on frontend
- Responsive images

### Frontend

- Minimal JavaScript
- CSS variables for theming
- No external CDN dependencies
- Cached static assets

---

## Extensibility Points

### Adding New Fields

1. Update database schema in `models.py`
2. Add field to form templates
3. Update create/update logic in `main.py`
4. Add to PDF/CSV export in `utils.py`

### Custom Reports

Add new route in `main.py`:
```python
@app.route('/export/custom')
def export_custom():
    # Custom report logic
    return send_file(...)
```

### API Endpoints

Add JSON routes:
```python
@app.route('/api/sightings')
def api_sightings():
    sightings = db.get_all_sightings()
    return jsonify(sightings)
```

---

## Deployment

### Local Deployment

```bash
./setup.sh  # One-time setup
./run.sh    # Start server
```

### Production Deployment

For production use with a proper WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

### Environment Variables

Production settings in `.env`:
```
SECRET_KEY=random-secure-key-here
FLASK_ENV=production
FLASK_DEBUG=0
HOST=0.0.0.0
PORT=5000
```

---

## Testing Strategy

### Manual Testing Checklist

- [ ] Log sighting with all fields
- [ ] Log sighting with minimal fields
- [ ] Upload photo (various formats)
- [ ] Edit existing sighting
- [ ] Delete sighting
- [ ] Search functionality
- [ ] PDF export
- [ ] CSV export
- [ ] Mobile responsiveness
- [ ] Navigation menu

### Automated Testing (Future)

Potential test framework: pytest

```python
def test_create_sighting():
    # Test database insertion
    pass

def test_photo_upload():
    # Test file processing
    pass
```

---

## Future Enhancements

### Planned Features

- Multi-user support with authentication
- Email notifications for patterns
- Geolocation integration
- Timeline visualization
- Weather API integration
- Backup/restore functionality
- Mobile app (PWA)

### Technical Improvements

- Migration system for database updates
- Automated testing suite
- CI/CD pipeline
- Docker containerization
- API documentation

---

## Contributing

Follow the **10 Golden Rules** (see README.md)

### Code Style

- Python: PEP 8
- JavaScript: ES6+
- HTML: Semantic, accessible markup
- CSS: BEM-like naming

### Documentation

- All files include metadata headers
- Docstrings for all functions
- Comments for complex logic
- Update this document for architecture changes

---

**Version**: 1.0.0
**Last Updated**: 2025-10-31
**Authors**: dnoice + Claude AI
