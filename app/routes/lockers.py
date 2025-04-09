from flask import Blueprint, render_template, session, request, flash, redirect, url_for, current_app
from app.models import Locker, Building, User  # Import your models, and User
from app import db  # Import your db instance
from app.forms import RssForm  # Import the RssForm
from app.utils import teacher_required, student_required  # Import student_required decorator
import logging
from datetime import datetime

lockers_bp = Blueprint('lockers', __name__, url_prefix='/student')  # Added url_prefix for clarity
logger = logging.getLogger(__name__)


# Student Dashboard
@lockers_bp.route('/dashboard')
@student_required
def student_dashboard():
    locker = Locker.query.filter_by(assigned_user_id=session.get("user_id")).first()
    print(f"Session data on teacher dashboard: {session}")  # Add this line
    return render_template('dashboard_student.html', locker=locker)


# Select Building
@lockers_bp.route('/select_building')
@student_required
def select_building():
    buildings = Building.query.all()
    return render_template('select_building.html', buildings=buildings)


# Select Locker from building selection
@lockers_bp.route('/available_lockers', methods=['POST'])
@student_required
def show_available_lockers():
    building_id = request.form.get('building_id')
    building = Building.query.get(building_id)
    if not building:
        flash("Building not found.", "danger")
        return redirect(url_for('lockers.select_building'))
    available_lockers = Locker.query.filter_by(building_id=building_id, assigned_user_id=None).all()
    return render_template('show_available_lockers.html', lockers=available_lockers, building_name=building.name)


# Register Locker - From Available Lockers Page
@lockers_bp.route('/register_locker', methods=['POST'])
@student_required
def register_locker():
    student_id = session.get('user_id')
    existing_locker = Locker.query.filter_by(assigned_user_id=student_id).first()

    if existing_locker:
        flash("You already have a locker assigned.", "danger")
        return redirect(url_for('lockers.student_dashboard'))

    locker_id = request.form.get('locker_id')
    locker = Locker.query.get(locker_id)

    if locker and locker.assigned_user_id is None:
        locker.assigned_user_id = student_id
        locker.assignment_date = datetime.utcnow()  # Set the assignment date here
        try:
            db.session.commit()
            flash("Locker registered successfully!", "success")
            return redirect(url_for('lockers.student_dashboard'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error committing locker registration for locker ID {locker_id}: {e}")
            flash("An error occurred while registering the locker.", "danger")
            return redirect(url_for('lockers.select_building'))
    else:
        flash("Locker is not available.", "danger")
        return redirect(url_for('lockers.select_building'))


# View Locker
@lockers_bp.route('/view_locker')
@student_required
def view_locker():
    locker = Locker.query.filter_by(assigned_user_id=session.get('user_id')).first()

    if locker:
        building = Building.query.get(locker.building_id)
        return render_template('view_locker.html', locker=locker, building_name=building.name)
    else:
        return render_template('view_locker.html', locker=None)


@lockers_bp.route('/release_locker', methods=['POST'])
@student_required
def release_locker():
    student_id = session.get('user_id')
    locker = Locker.query.filter_by(assigned_user_id=student_id).first()

    if locker:
        locker.assigned_user_id = None
        locker.assignment_date = None  # Optionally clear the assignment date
        db.session.commit()
        flash("Locker released successfully!", "success")
    else:
        flash("You do not have a locker to release.", "danger")

    return redirect(url_for('lockers.student_dashboard'))


@lockers_bp.route('/schedule_options/student', methods=['GET', 'POST'])
@student_required
def schedule_options_student():
    form = RssForm()
    user = User.query.filter_by(email=session.get('username')).first()
    rss_enabled = current_app.config.get('RSS_ENABLED', False)

    if not rss_enabled:
        flash("Schedule options are currently disabled by the administrator.", "warning")
        return redirect(url_for('lockers.student_dashboard'))

    if form.validate_on_submit():
        user.rss_feed = form.rss_url.data
        db.session.commit()
        flash('RSS feed saved!', 'success')
        return redirect(url_for('lockers.schedule_options_student'))

    return render_template('schedule_options_student.html', form=form, rss_feed=user.rss_feed)


@lockers_bp.route('/test_select_building')
def test_select_building():
    return render_template('select_building.html', buildings=[])
