"""
File: utils.py
Path: app/utils.py
Purpose: Utility functions for photo processing, PDF/CSV generation, and validation
Author: dnoice + Claude AI
Version: 1.0.0
Created: 2025-10-31
Updated: 2025-10-31
"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Optional
from PIL import Image, UnidentifiedImageError
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib import colors
from werkzeug.utils import secure_filename
from html import escape


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Check if file extension is allowed.

    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions

    Returns:
        bool: True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def process_and_save_photo(file, upload_folder: str, max_size: tuple = (1200, 1200), max_file_size: int = 16 * 1024 * 1024) -> Optional[str]:
    """
    Process and save uploaded photo with resizing.

    Args:
        file: File object from request
        upload_folder: Directory to save the file
        max_size: Maximum dimensions (width, height)
        max_file_size: Maximum file size in bytes (default 16MB)

    Returns:
        str or None: Relative path to saved file, or None if no file provided

    Raises:
        ValueError: If file is invalid, too large, or not an image
        IOError: If upload folder is not writable or file cannot be saved
    """
    if not file or not file.filename:
        return None

    # Validate upload folder exists and is writable
    if not os.path.exists(upload_folder):
        raise IOError(f"Upload folder does not exist: {upload_folder}")
    if not os.access(upload_folder, os.W_OK):
        raise IOError(f"Upload folder is not writable: {upload_folder}")

    # Check file size before processing (seek to end to get size)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset to beginning

    if file_size > max_file_size:
        raise ValueError(f"File too large: {file_size} bytes (max: {max_file_size} bytes)")

    if file_size == 0:
        raise ValueError("File is empty")

    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_filename = secure_filename(file.filename)
    if not original_filename:
        raise ValueError("Invalid filename")

    filename = f"{timestamp}_{original_filename}"
    filepath = os.path.join(upload_folder, filename)

    try:
        # Open and validate image
        image = Image.open(file)
        image.verify()  # Verify it's a valid image
        file.seek(0)  # Reset after verify
        image = Image.open(file)  # Re-open after verify

        # Check image dimensions are reasonable (prevent decompression bombs)
        if image.width * image.height > 178956970:  # ~178 megapixels
            raise ValueError("Image dimensions too large")

        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        elif image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')

        # Resize maintaining aspect ratio
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save optimized image
        image.save(filepath, 'JPEG', quality=85, optimize=True)

        # Return relative path for database storage
        return os.path.join('static/uploads', filename)

    except UnidentifiedImageError:
        raise ValueError("File is not a valid image")
    except (IOError, OSError) as e:
        raise IOError(f"Failed to process image: {str(e)}")
    except Exception as e:
        # Clean up any partially written file
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
        raise ValueError(f"Image processing failed: {str(e)}")


def generate_pdf_report(sightings: List[Dict], output_path: str) -> str:
    """
    Generate a professional PDF report from sighting data.

    Args:
        sightings: List of sighting dictionaries
        output_path: Path to save the PDF file

    Returns:
        str: Path to generated PDF file
    """
    # Create document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#8B0000'),
        spaceAfter=30,
        alignment=1  # Center
    )
    story.append(Paragraph("Roach Tracker Report", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Report metadata
    report_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    meta_style = styles['Normal']
    story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", meta_style))
    story.append(Paragraph(f"<b>Total Sightings:</b> {len(sightings)}", meta_style))

    total_roaches = sum(s.get('roach_count', 1) for s in sightings)
    story.append(Paragraph(f"<b>Total Roaches Documented:</b> {total_roaches}", meta_style))
    story.append(Spacer(1, 0.3 * inch))

    # Summary section
    story.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
    summary_text = f"""
    This report documents {len(sightings)} cockroach sighting(s) totaling {total_roaches} individual
    roach(es). Each sighting has been cataloged with timestamp, location, and relevant details
    to provide comprehensive documentation for property management review.
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))

    # Sightings detail
    story.append(Paragraph("<b>Detailed Sightings Log</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1 * inch))

    for idx, sighting in enumerate(sightings, 1):
        # Sighting header
        sighting_header = f"Sighting #{idx}: {sighting['location']}"
        story.append(Paragraph(sighting_header, styles['Heading3']))

        # Sighting details
        timestamp = sighting.get('timestamp', 'N/A')
        if timestamp != 'N/A':
            try:
                dt = datetime.fromisoformat(timestamp)
                timestamp = dt.strftime('%B %d, %Y at %I:%M %p')
            except (ValueError, TypeError):
                pass  # Keep original timestamp if parsing fails

        # Sanitize all text fields to prevent XML parsing errors
        details = [
            ['Timestamp:', escape(str(timestamp))],
            ['Location:', escape(str(sighting.get('location', 'N/A')))],
            ['Room Type:', escape(str(sighting.get('room_type', 'N/A')))],
            ['Roach Count:', escape(str(sighting.get('roach_count', 1)))],
            ['Roach Size:', escape(str(sighting.get('roach_size', 'N/A')))],
            ['Time of Day:', escape(str(sighting.get('time_of_day', 'N/A')))],
        ]

        table = Table(details, colWidths=[1.5 * inch, 4.5 * inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(table)

        # Notes (sanitized to prevent XML parsing errors)
        if sighting.get('notes'):
            story.append(Spacer(1, 0.1 * inch))
            sanitized_notes = escape(str(sighting['notes']))
            story.append(Paragraph(f"<b>Notes:</b> {sanitized_notes}", styles['Normal']))

        # Photo if available
        if sighting.get('photo_path'):
            try:
                photo_path = sighting['photo_path']
                if os.path.exists(photo_path) and os.path.isfile(photo_path):
                    img = RLImage(photo_path, width=3 * inch, height=3 * inch, kind='proportional')
                    story.append(Spacer(1, 0.1 * inch))
                    story.append(img)
            except (IOError, OSError, ValueError) as e:
                # Log error but continue with report generation
                story.append(Paragraph(f"<i>[Photo unavailable: {escape(str(e))}]</i>", styles['Normal']))

        story.append(Spacer(1, 0.3 * inch))

    # Build PDF
    doc.build(story)
    return output_path


def generate_csv_export(sightings: List[Dict], output_path: str) -> str:
    """
    Generate CSV export from sighting data.

    Args:
        sightings: List of sighting dictionaries
        output_path: Path to save the CSV file

    Returns:
        str: Path to generated CSV file
    """
    fieldnames = [
        'id', 'timestamp', 'location', 'room_type', 'roach_count',
        'roach_size', 'roach_type', 'photo_path', 'notes',
        'weather', 'temperature', 'time_of_day', 'created_at', 'updated_at'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sighting in sightings:
            writer.writerow({k: sighting.get(k, '') for k in fieldnames})

    return output_path


def format_timestamp(timestamp_str: str) -> str:
    """
    Format ISO timestamp to human-readable string.

    Args:
        timestamp_str: ISO format timestamp string

    Returns:
        str: Formatted timestamp or original string if parsing fails
    """
    if not timestamp_str:
        return 'N/A'

    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except (ValueError, TypeError, AttributeError):
        return str(timestamp_str)


def get_time_of_day(timestamp_str: str = None) -> str:
    """
    Determine time of day category from timestamp.

    Args:
        timestamp_str: ISO format timestamp string (optional, uses current time if None)

    Returns:
        str: Time category (Morning, Afternoon, Evening, Night, or Unknown if parsing fails)
    """
    try:
        if timestamp_str:
            dt = datetime.fromisoformat(timestamp_str)
        else:
            dt = datetime.now()

        hour = dt.hour
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'
    except (ValueError, TypeError, AttributeError):
        return 'Unknown'
