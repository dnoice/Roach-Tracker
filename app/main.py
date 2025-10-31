"""
File: main.py
Path: app/main.py
Purpose: Flask routes and application logic for Roach Tracker
Author: dnoice + Claude AI
Version: 1.1.0
Created: 2025-10-31
Updated: 2025-10-31
"""

from flask import render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from app.models import Database, User
from app.auth import admin_required, property_manager_required, get_user_accessible_properties
from app.utils import (
    allowed_file, process_and_save_photo, generate_pdf_report,
    generate_csv_export, format_timestamp, get_time_of_day
)


def register_routes(app):
    """
    Register all application routes with the Flask app.

    Args:
        app: Flask application instance
    """

    # Initialize database
    db = Database(app.config['DATABASE'])

    # ===================================================================
    # Authentication Routes
    # ===================================================================

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration page."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            try:
                username = request.form.get('username', '').strip()
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                password_confirm = request.form.get('password_confirm', '')
                full_name = request.form.get('full_name', '').strip()

                # Validation
                if not username or not email or not password:
                    flash('All fields are required', 'error')
                    return render_template('register.html')

                if password != password_confirm:
                    flash('Passwords do not match', 'error')
                    return render_template('register.html')

                # Create user (default role is 'resident')
                user_id = db.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role='resident',
                    full_name=full_name if full_name else None
                )

                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))

            except ValueError as e:
                flash(str(e), 'error')
                return render_template('register.html')
            except Exception as e:
                flash('An error occurred during registration. Please try again.', 'error')
                current_app.logger.error(f"Registration error: {str(e)}")
                return render_template('register.html')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login page."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            try:
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '')
                remember = request.form.get('remember', False)

                if not username or not password:
                    flash('Username and password are required', 'error')
                    return render_template('login.html')

                # Verify credentials
                user_data = db.verify_user_password(username, password)

                if user_data:
                    # Check if user is active
                    if not user_data.get('is_active'):
                        flash('Your account has been deactivated. Please contact support.', 'error')
                        return render_template('login.html')

                    # Create User object and log in
                    user = User(user_data)
                    login_user(user, remember=bool(remember))
                    flash(f'Welcome back, {user.username}!', 'success')

                    # Redirect to next page or index
                    next_page = request.args.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'error')
                    return render_template('login.html')

            except ValueError as e:
                flash(str(e), 'error')
                return render_template('login.html')
            except Exception as e:
                flash('An error occurred during login. Please try again.', 'error')
                current_app.logger.error(f"Login error: {str(e)}")
                return render_template('login.html')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        """Log out current user."""
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('login'))

    # ===================================================================
    # Main Application Routes
    # ===================================================================

    @app.route('/')
    @login_required
    def index():
        """Dashboard home page with recent sightings overview."""
        recent_sightings = db.get_all_sightings(limit=5)
        stats = db.get_statistics()
        return render_template('index.html',
                             recent_sightings=recent_sightings,
                             stats=stats,
                             format_timestamp=format_timestamp)

    @app.route('/log', methods=['GET', 'POST'])
    @login_required
    def log_sighting():
        """Log a new roach sighting."""
        if request.method == 'POST':
            try:
                # Validate required fields
                location = request.form.get('location', '').strip()
                if not location:
                    flash('Location is required', 'error')
                    return render_template('log_sighting.html')

                # Parse roach_count with error handling
                try:
                    roach_count = int(request.form.get('roach_count', 1))
                    if roach_count < 1:
                        raise ValueError("Count must be positive")
                except (ValueError, TypeError):
                    flash('Invalid roach count. Must be a positive number.', 'error')
                    return render_template('log_sighting.html')

                # Parse temperature with error handling
                temperature = None
                temp_str = request.form.get('temperature', '').strip()
                if temp_str:
                    try:
                        temperature = float(temp_str)
                    except (ValueError, TypeError):
                        flash('Invalid temperature value', 'error')
                        return render_template('log_sighting.html')

                # Process form data
                data = {
                    'timestamp': request.form.get('timestamp') or datetime.now().isoformat(),
                    'location': location,
                    'room_type': request.form.get('room_type'),
                    'roach_count': roach_count,
                    'roach_size': request.form.get('roach_size'),
                    'roach_type': request.form.get('roach_type'),
                    'notes': request.form.get('notes'),
                    'weather': request.form.get('weather'),
                    'temperature': temperature,
                    'time_of_day': get_time_of_day(request.form.get('timestamp')),
                    'user_id': current_user.id,  # Associate with logged-in user
                }

                # Handle photo upload
                photo_path = None
                if 'photo' in request.files:
                    file = request.files['photo']
                    if file and file.filename:
                        if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
                            flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP', 'error')
                            return render_template('log_sighting.html')

                        try:
                            photo_path = process_and_save_photo(file, app.config['UPLOAD_FOLDER'])
                            if photo_path:  # Only set if successfully processed
                                data['photo_path'] = photo_path
                        except ValueError as e:
                            flash(f'Photo upload failed: {str(e)}', 'error')
                            return render_template('log_sighting.html')
                        except IOError:
                            flash('Photo upload failed: Server error', 'error')
                            return render_template('log_sighting.html')

                # Save to database
                sighting_id = db.create_sighting(data)
                flash('Sighting logged successfully!', 'success')
                return redirect(url_for('view_sighting', sighting_id=sighting_id))

            except ValueError as e:
                flash(f'Validation error: {str(e)}', 'error')
                return render_template('log_sighting.html')
            except Exception as e:
                flash('An error occurred while logging the sighting. Please try again.', 'error')
                current_app.logger.error(f"Error logging sighting: {str(e)}")
                return render_template('log_sighting.html')

        return render_template('log_sighting.html')

    @app.route('/sightings')
    @login_required
    def view_sightings():
        """View all sightings with search capability."""
        query = request.args.get('q', '').strip()
        sightings = []

        try:
            if query:
                sightings = db.search_sightings(query)
            else:
                sightings = db.get_all_sightings()
        except ValueError as e:
            flash(f'Search error: {str(e)}', 'error')
            sightings = []
        except Exception as e:
            flash('An error occurred while retrieving sightings', 'error')
            current_app.logger.error(f"Error retrieving sightings: {str(e)}")
            sightings = []

        return render_template('view_sightings.html',
                             sightings=sightings,
                             query=query,
                             format_timestamp=format_timestamp)

    @app.route('/sighting/<int:sighting_id>')
    @login_required
    def view_sighting(sighting_id):
        """View detailed information about a specific sighting."""
        try:
            sighting = db.get_sighting(sighting_id)
        except ValueError:
            flash('Invalid sighting ID', 'error')
            return redirect(url_for('view_sightings'))

        if not sighting:
            flash('Sighting not found.', 'error')
            return redirect(url_for('view_sightings'))

        return render_template('view_sighting.html',
                             sighting=sighting,
                             format_timestamp=format_timestamp)

    @app.route('/sighting/<int:sighting_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_sighting(sighting_id):
        """Edit an existing sighting."""
        try:
            sighting = db.get_sighting(sighting_id)
        except ValueError:
            flash('Invalid sighting ID', 'error')
            return redirect(url_for('view_sightings'))

        if not sighting:
            flash('Sighting not found.', 'error')
            return redirect(url_for('view_sightings'))

        if request.method == 'POST':
            try:
                # Validate required fields
                location = request.form.get('location', '').strip()
                if not location:
                    flash('Location is required', 'error')
                    return render_template('edit_sighting.html', sighting=sighting)

                # Parse roach_count with error handling
                try:
                    roach_count = int(request.form.get('roach_count', 1))
                    if roach_count < 1:
                        raise ValueError("Count must be positive")
                except (ValueError, TypeError):
                    flash('Invalid roach count. Must be a positive number.', 'error')
                    return render_template('edit_sighting.html', sighting=sighting)

                # Parse temperature with error handling
                temperature = None
                temp_str = request.form.get('temperature', '').strip()
                if temp_str:
                    try:
                        temperature = float(temp_str)
                    except (ValueError, TypeError):
                        flash('Invalid temperature value', 'error')
                        return render_template('edit_sighting.html', sighting=sighting)

                # Process form data
                data = {
                    'timestamp': request.form.get('timestamp') or sighting['timestamp'],
                    'location': location,
                    'room_type': request.form.get('room_type'),
                    'roach_count': roach_count,
                    'roach_size': request.form.get('roach_size'),
                    'roach_type': request.form.get('roach_type'),
                    'notes': request.form.get('notes'),
                    'weather': request.form.get('weather'),
                    'temperature': temperature,
                    'time_of_day': get_time_of_day(request.form.get('timestamp')),
                    'photo_path': sighting['photo_path'],  # Keep existing photo
                    'user_id': sighting.get('user_id'),  # Maintain original user
                    'property_id': sighting.get('property_id'),  # Maintain original property
                }

                # Handle new photo upload
                if 'photo' in request.files:
                    file = request.files['photo']
                    if file and file.filename:
                        if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
                            flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP', 'error')
                            return render_template('edit_sighting.html', sighting=sighting)

                        try:
                            photo_path = process_and_save_photo(file, app.config['UPLOAD_FOLDER'])
                            if photo_path:  # Only update if successfully processed
                                # Delete old photo if exists and is different
                                if sighting['photo_path'] and sighting['photo_path'] != photo_path:
                                    if os.path.exists(sighting['photo_path']) and os.path.isfile(sighting['photo_path']):
                                        try:
                                            os.remove(sighting['photo_path'])
                                        except (OSError, IOError) as e:
                                            current_app.logger.warning(f"Failed to delete old photo: {str(e)}")
                                data['photo_path'] = photo_path
                        except ValueError as e:
                            flash(f'Photo upload failed: {str(e)}', 'error')
                            return render_template('edit_sighting.html', sighting=sighting)
                        except IOError:
                            flash('Photo upload failed: Server error', 'error')
                            return render_template('edit_sighting.html', sighting=sighting)

                # Update database
                db.update_sighting(sighting_id, data)
                flash('Sighting updated successfully!', 'success')
                return redirect(url_for('view_sighting', sighting_id=sighting_id))

            except ValueError as e:
                flash(f'Validation error: {str(e)}', 'error')
                return render_template('edit_sighting.html', sighting=sighting)
            except Exception as e:
                flash('An error occurred while updating the sighting. Please try again.', 'error')
                current_app.logger.error(f"Error updating sighting: {str(e)}")
                return render_template('edit_sighting.html', sighting=sighting)

        return render_template('edit_sighting.html',
                             sighting=sighting)

    @app.route('/sighting/<int:sighting_id>/delete', methods=['POST'])
    @login_required
    def delete_sighting(sighting_id):
        """Delete a sighting."""
        try:
            sighting = db.get_sighting(sighting_id)
        except ValueError:
            flash('Invalid sighting ID', 'error')
            return redirect(url_for('view_sightings'))

        if not sighting:
            flash('Sighting not found.', 'error')
            return redirect(url_for('view_sightings'))

        # Delete photo if exists
        if sighting['photo_path']:
            photo_path = sighting['photo_path']
            if os.path.exists(photo_path) and os.path.isfile(photo_path):
                try:
                    os.remove(photo_path)
                except (OSError, IOError) as e:
                    # Log but don't fail the deletion
                    current_app.logger.warning(f"Failed to delete photo file: {str(e)}")

        # Delete from database
        try:
            db.delete_sighting(sighting_id)
            flash('Sighting deleted successfully!', 'success')
        except ValueError as e:
            flash(f'Validation error: {str(e)}', 'error')
        except Exception as e:
            flash('An error occurred while deleting the sighting', 'error')
            current_app.logger.error(f"Error deleting sighting: {str(e)}")

        return redirect(url_for('view_sightings'))

    @app.route('/statistics')
    @login_required
    def statistics():
        """View comprehensive statistics and analytics."""
        try:
            stats = db.get_statistics()
            all_sightings = db.get_all_sightings()
        except Exception as e:
            flash('Error loading statistics. Please try again.', 'error')
            current_app.logger.error(f"Error loading statistics: {str(e)}")
            stats = {
                'total_sightings': 0,
                'total_roaches': 0,
                'locations': [],
                'sizes': [],
                'times_of_day': [],
                'recent_trend': []
            }
            all_sightings = []

        return render_template('statistics.html',
                             stats=stats,
                             all_sightings=all_sightings,
                             format_timestamp=format_timestamp)

    @app.route('/export/pdf')
    @login_required
    def export_pdf():
        """Generate and download PDF report."""
        try:
            sightings = db.get_all_sightings()
        except Exception as e:
            flash('Error retrieving sightings for export', 'error')
            current_app.logger.error(f"Error retrieving sightings for PDF: {str(e)}")
            return redirect(url_for('index'))

        if not sightings:
            flash('No sightings to export.', 'warning')
            return redirect(url_for('index'))

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'roach_tracker_report_{timestamp}.pdf'
        output_path = os.path.join('exports', filename)

        try:
            generate_pdf_report(sightings, output_path)
            return send_file(output_path,
                           as_attachment=True,
                           download_name=filename,
                           mimetype='application/pdf')
        except Exception as e:
            flash('Error generating PDF report. Please try again.', 'error')
            current_app.logger.error(f"Error generating PDF: {str(e)}")
            return redirect(url_for('statistics'))

    @app.route('/export/csv')
    @login_required
    def export_csv():
        """Generate and download CSV export."""
        try:
            sightings = db.get_all_sightings()
        except Exception as e:
            flash('Error retrieving sightings for export', 'error')
            current_app.logger.error(f"Error retrieving sightings for CSV: {str(e)}")
            return redirect(url_for('index'))

        if not sightings:
            flash('No sightings to export.', 'warning')
            return redirect(url_for('index'))

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'roach_tracker_export_{timestamp}.csv'
        output_path = os.path.join('exports', filename)

        try:
            generate_csv_export(sightings, output_path)
            return send_file(output_path,
                           as_attachment=True,
                           download_name=filename,
                           mimetype='text/csv')
        except Exception as e:
            flash('Error generating CSV export. Please try again.', 'error')
            current_app.logger.error(f"Error generating CSV: {str(e)}")
            return redirect(url_for('statistics'))

    # ===================================================================
    # Admin Routes - User Management
    # ===================================================================

    @app.route('/admin/users')
    @admin_required
    def admin_users():
        """Admin page to manage users."""
        try:
            users = db.get_all_users()
        except Exception as e:
            flash('Error loading users', 'error')
            current_app.logger.error(f"Error loading users: {str(e)}")
            users = []

        return render_template('admin_users.html', users=users)

    @app.route('/admin/users/create', methods=['GET', 'POST'])
    @admin_required
    def admin_create_user():
        """Admin page to create new user."""
        if request.method == 'POST':
            try:
                username = request.form.get('username', '').strip()
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                role = request.form.get('role', 'resident')
                full_name = request.form.get('full_name', '').strip()

                if not username or not email or not password:
                    flash('Username, email, and password are required', 'error')
                    return render_template('admin_create_user.html')

                user_id = db.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role,
                    full_name=full_name if full_name else None
                )

                flash(f'User {username} created successfully!', 'success')
                return redirect(url_for('admin_users'))

            except ValueError as e:
                flash(str(e), 'error')
                return render_template('admin_create_user.html')
            except Exception as e:
                flash('An error occurred while creating the user', 'error')
                current_app.logger.error(f"Error creating user: {str(e)}")
                return render_template('admin_create_user.html')

        return render_template('admin_create_user.html')

    @app.route('/admin/users/<int:user_id>/toggle-active', methods=['POST'])
    @admin_required
    def admin_toggle_user_active(user_id):
        """Toggle user active status."""
        try:
            user_data = db.get_user_by_id(user_id)
            if not user_data:
                flash('User not found', 'error')
                return redirect(url_for('admin_users'))

            # Prevent deactivating yourself
            if user_id == current_user.id:
                flash('You cannot deactivate your own account', 'error')
                return redirect(url_for('admin_users'))

            new_status = 0 if user_data.get('is_active') else 1
            db.update_user(user_id, {'is_active': new_status})

            status_text = 'activated' if new_status else 'deactivated'
            flash(f'User {user_data["username"]} {status_text} successfully', 'success')

        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('An error occurred while updating the user', 'error')
            current_app.logger.error(f"Error toggling user active: {str(e)}")

        return redirect(url_for('admin_users'))

    @app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_user(user_id):
        """Delete a user."""
        try:
            user_data = db.get_user_by_id(user_id)
            if not user_data:
                flash('User not found', 'error')
                return redirect(url_for('admin_users'))

            # Prevent deleting yourself
            if user_id == current_user.id:
                flash('You cannot delete your own account', 'error')
                return redirect(url_for('admin_users'))

            db.delete_user(user_id)
            flash(f'User {user_data["username"]} deleted successfully', 'success')

        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('An error occurred while deleting the user', 'error')
            current_app.logger.error(f"Error deleting user: {str(e)}")

        return redirect(url_for('admin_users'))

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('index.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        flash('An internal error occurred. Please try again.', 'error')
        return redirect(url_for('index'))
