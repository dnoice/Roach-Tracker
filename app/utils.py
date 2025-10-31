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
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib import colors
from werkzeug.utils import secure_filename


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


def process_and_save_photo(file, upload_folder: str, max_size: tuple = (1200, 1200)) -> str:
    """
    Process and save uploaded photo with resizing.

    Args:
        file: File object from request
        upload_folder: Directory to save the file
        max_size: Maximum dimensions (width, height)

    Returns:
        str: Relative path to saved file
    """
    if not file or not file.filename:
        return None

    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_filename = secure_filename(file.filename)
    filename = f"{timestamp}_{original_filename}"
    filepath = os.path.join(upload_folder, filename)

    # Open and resize image
    image = Image.open(file)

    # Convert RGBA to RGB if necessary
    if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background

    # Resize maintaining aspect ratio
    image.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Save optimized image
    image.save(filepath, 'JPEG', quality=85, optimize=True)

    # Return relative path for database storage
    return os.path.join('static/uploads', filename)


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
            except:
                pass

        details = [
            ['Timestamp:', timestamp],
            ['Location:', sighting.get('location', 'N/A')],
            ['Room Type:', sighting.get('room_type', 'N/A')],
            ['Roach Count:', str(sighting.get('roach_count', 1))],
            ['Roach Size:', sighting.get('roach_size', 'N/A')],
            ['Time of Day:', sighting.get('time_of_day', 'N/A')],
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

        # Notes
        if sighting.get('notes'):
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(f"<b>Notes:</b> {sighting['notes']}", styles['Normal']))

        # Photo if available
        if sighting.get('photo_path'):
            try:
                photo_path = sighting['photo_path']
                if os.path.exists(photo_path):
                    img = RLImage(photo_path, width=3 * inch, height=3 * inch, kind='proportional')
                    story.append(Spacer(1, 0.1 * inch))
                    story.append(img)
            except:
                pass

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
        str: Formatted timestamp
    """
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        return timestamp_str


def get_time_of_day(timestamp_str: str = None) -> str:
    """
    Determine time of day category from timestamp.

    Args:
        timestamp_str: ISO format timestamp string (optional, uses current time if None)

    Returns:
        str: Time category (Morning, Afternoon, Evening, Night)
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
    except:
        return 'Unknown'
