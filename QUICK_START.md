**File**: `QUICK_START.md`
**Path**: `QUICK_START.md`
**Purpose**: Fast-track setup and usage guide for new users
**Author**: dnoice + Claude AI
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

# Quick Start Guide

**Roach Tracker - Complete Setup and Usage Guide**

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Bash shell (Linux, macOS, or WSL on Windows)
- 50 MB free disk space

### Step 1: Clone the Repository

```bash
git clone https://github.com/dnoice/Roach-Tracker.git
cd Roach-Tracker
```

### Step 2: Run Setup Script

```bash
./setup.sh
```

This script will:
- Create a Python virtual environment
- Install all required dependencies
- Create a `.env` configuration file
- Initialize the SQLite database

### Step 3: Configure Environment (Optional)

Edit `.env` to customize settings:

```bash
nano .env
```

Important settings:
- `SECRET_KEY`: Change this to a random string for production
- `HOST`: Default is `0.0.0.0` (all interfaces)
- `PORT`: Default is `5000`

### Step 4: Launch the Application

```bash
./run.sh
```

Open your browser to: `http://localhost:5000`

---

## First-Time Usage

### 1. Explore the Dashboard

The dashboard shows:
- Total sightings and roach count
- Recent sightings
- Top problem areas
- Quick action buttons

### 2. Log Your First Sighting

1. Click "Log New Sighting" button
2. Fill in the form:
   - **Location**: e.g., "Kitchen", "Bathroom"
   - **Count**: Number of roaches seen
   - **Size**: Select from dropdown
   - **Photo**: Upload from camera or gallery
   - **Notes**: Any additional observations
3. Click "Log Sighting"

### 3. View Sighting Details

- Click on any sighting to see full details
- Edit or delete from the detail page
- Photos are displayed in full resolution

### 4. Search Sightings

- Use the search bar on "All Sightings" page
- Search by location or notes
- Results update instantly

### 5. View Statistics

Navigate to "Statistics" page to see:
- Location distribution
- Size distribution
- Time of day patterns
- 7-day activity trend

### 6. Generate Reports

From the Statistics page:
- Click "Export PDF Report" for professional documentation
- Click "Export CSV Data" for spreadsheet analysis
- Files are saved to `exports/` directory

---

## Daily Workflow

### When You Spot a Roach

1. Open the app (bookmark `http://localhost:5000`)
2. Click "Log Sighting"
3. Take a photo (or upload existing)
4. Fill in location and details
5. Submit

### Weekly Review

1. Check Statistics page
2. Identify problem areas
3. Note any patterns (time of day, weather)

### When Filing a Complaint

1. Go to Statistics page
2. Export PDF report
3. Review `SAMPLE_COMPLAINT_LETTER.txt`
4. Attach PDF to your complaint
5. Keep copies for your records

---

## Mobile Usage

### Android/iOS Browser

The application is fully responsive:
- Touch-optimized buttons and forms
- Camera integration for photos
- Swipe-friendly navigation
- Readable on small screens

### Taking Photos

- Use the file upload button
- On mobile, it will activate the camera
- Photos are automatically resized for storage

---

## Advanced Features

### Editing Sightings

1. Navigate to sighting detail page
2. Click "Edit"
3. Modify any fields
4. Upload new photo (optional)
5. Click "Update"

### Deleting Sightings

From sighting detail page:
- Click "Delete" button
- Confirm the deletion
- Photo files are also removed

### Search and Filter

- Use search on "All Sightings" page
- Search by location: "kitchen"
- Search by notes: "near sink"

---

## Troubleshooting

### Application Won't Start

```bash
# Verify installation
./verify.sh

# If errors found, re-run setup
./setup.sh
```

### Database Errors

```bash
# Backup your database first
cp data/roach_tracker.db data/backup.db

# Reinitialize (WARNING: This erases data)
rm data/roach_tracker.db
python3 -c "from app import create_app; app = create_app()"
```

### Photos Not Uploading

- Check file size (max 16MB)
- Supported formats: JPG, PNG, GIF, WEBP
- Ensure `static/uploads/` directory exists and is writable

### Port Already in Use

Edit `.env` and change `PORT=5000` to another port (e.g., `PORT=5001`), then restart.

---

## Data Management

### Backup Your Data

```bash
# Backup database
cp data/roach_tracker.db ~/roach_tracker_backup_$(date +%Y%m%d).db

# Backup photos
tar -czf ~/roach_photos_backup_$(date +%Y%m%d).tar.gz static/uploads/
```

### Export All Data

1. Go to Statistics page
2. Click "Export CSV Data"
3. CSV contains all sighting information
4. Import into Excel, Google Sheets, etc.

### Restore from Backup

```bash
# Restore database
cp ~/roach_tracker_backup_YYYYMMDD.db data/roach_tracker.db

# Restore photos
tar -xzf ~/roach_photos_backup_YYYYMMDD.tar.gz
```

---

## Tips for Effective Documentation

### Best Practices

1. **Log Immediately**: Document sightings as they happen
2. **Always Photo**: Visual evidence is powerful
3. **Be Detailed**: Include time, location, and context
4. **Track Patterns**: Use statistics to identify trends
5. **Keep Records**: Export reports regularly

### Photo Tips

- Use good lighting
- Include reference objects for scale
- Capture multiple angles if possible
- Don't edit or filter photos
- Original, unmodified photos have more credibility

### Report Tips

- Export reports monthly
- Keep dated copies
- Include in all correspondence with management
- Note any responses from management in sighting notes

---

## Stopping the Application

Press `Ctrl+C` in the terminal where the app is running.

---

## Uninstallation

```bash
# Remove virtual environment
rm -rf venv/

# Remove database (WARNING: Data loss)
rm -rf data/

# Remove uploads (WARNING: Photo loss)
rm -rf static/uploads/

# Remove exports
rm -rf exports/
```

---

## Getting Help

- Review [README.md](README.md) for overview
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Review [SAMPLE_COMPLAINT_LETTER.txt](SAMPLE_COMPLAINT_LETTER.txt) for complaint guidance

---

**Version**: 1.0.0
**Last Updated**: 2025-10-31
