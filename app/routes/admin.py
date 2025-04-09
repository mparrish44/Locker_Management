from flask import render_template, redirect, url_for, flash, request, Blueprint, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import HomePageContent, AllowedDomain, Locker, Building, User, Settings, GradeLevel, GraduationYear, \
    RoleEnum  # Import RoleEnum
from app.database import db
from app.forms import (AddLockerForm, EditLockerForm, AddBuildingForm, EditBuildingForm, AssignLockerForm, AddUserForm,
                       EditUserForm, AddGradeLevelForm, EditGradeLevelForm, AddGraduationYearForm,
                       EditGraduationYearForm, StudentRegistrationForm, TeacherRegistrationForm, AddHomePageContentForm,
                       EditHomePageContentForm)
from app.utils import admin_required  # Import admin_required
from datetime import datetime
from sqlalchemy import or_

admin_bp = Blueprint('admin', __name__)


###############################################################################
# Admin Dashboard
###############################################################################

@admin_bp.route('/dashboard')
@admin_required  # Corrected decorator
def admin_dashboard():
    total_users = User.query.count()
    total_lockers = Locker.query.count()
    available_lockers = Locker.query.filter_by(assigned_user_id=None).count()
    occupied_lockers = Locker.query.filter(Locker.assigned_user_id.isnot(None)).count()

    # Get recent user registrations (last 5)
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()  # Assuming 'id' represents creation order

    # Get recent locker assignments (last 5)
    recent_assignments = Locker.query.filter(Locker.assigned_user_id.isnot(None)) \
        .order_by(Locker.assignment_date.desc()).limit(5).all()

    recent_activity = []
    for user in recent_users:
        recent_activity.append({
            'timestamp': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(user,
                                                                                  'created_at') and user.created_at else 'N/A',
            'description': f'New user registered: {user.full_name} ({user.role.value.capitalize()})'
        })

    for assignment in recent_assignments:
        user = User.query.get(assignment.assigned_user_id)
        if user:
            recent_activity.append({
                'timestamp': assignment.assignment_date.strftime(
                    '%Y-%m-%d %H:%M:%S') if assignment.assignment_date else 'N/A',
                'description': f'Locker {assignment.locker_number} assigned to {user.full_name}'
            })

    # Sort recent activity by timestamp in descending order
    recent_activity.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S') if x[
                                                                                                     'timestamp'] != 'N/A' else datetime.min,
                         reverse=True)
    recent_activity = recent_activity[:5]  # Limit to the latest 5 activities

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_lockers=total_lockers,
                           available_lockers=available_lockers,
                           occupied_lockers=occupied_lockers,
                           recent_activity=recent_activity)


###############################################################################
# Manage Users (Add, Edit, Delete, List)
###############################################################################

@admin_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(
            studentID=form.student_id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User added successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/add_user.html', form=form)


@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.studentID = form.student_id.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        if form.password.data:  # Only update password if a new one is provided
            user.password = form.password.data
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/edit_user.html', form=form, user=user)


@admin_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/delete_user.html', user=user)


@admin_bp.route('/manage_users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)


###############################################################################
# Manage Grade Levels (Add, Edit, Delete, List)
###############################################################################

@admin_bp.route('/add_grade_level', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def add_grade_level():
    form = AddGradeLevelForm()
    if form.validate_on_submit():
        grade_level = GradeLevel(grade_level=form.grade_level.data)
        db.session.add(grade_level)
        db.session.commit()
        flash('Grade Level added successfully.', 'success')
        return redirect(url_for('admin.manage_grade_levels'))
    return render_template('admin/add_grade_level.html', form=form)


@admin_bp.route('/edit_grade_level/<int:grade_level_id>', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def edit_grade_level(grade_level_id):
    grade_level = GradeLevel.query.get_or_404(grade_level_id)
    form = EditGradeLevelForm(obj=grade_level)
    if form.validate_on_submit():
        grade_level.grade_level = form.grade_level.data
        db.session.commit()
        flash('Grade Level updated successfully.', 'success')
        return redirect(url_for('admin.manage_grade_levels'))
    return render_template('admin/edit_grade_level.html', form=form, grade_level=grade_level)


@admin_bp.route('/delete_grade_level/<int:grade_level_id>', methods=['POST'])
@admin_required  # Corrected decorator
def delete_grade_level(grade_level_id):
    grade_level = GradeLevel.query.get_or_404(grade_level_id)
    db.session.delete(grade_level)
    db.session.commit()
    flash('Grade Level deleted successfully.', 'success')
    return redirect(url_for('admin.manage_grade_levels'))


@admin_bp.route('/manage_grade_levels')
@admin_required
def manage_grade_levels():
    grade_levels = GradeLevel.query.all()

    def sort_key(grade_level):
        level = grade_level.grade_level.upper()
        if level == 'PRE-K':
            return -4
        elif level == 'TK':
            return -3
        elif level == 'JK':
            return -2
        elif level == 'SK':
            return -1
        elif level.isdigit():
            return int(level)
        else:
            return level  # Keep other non-numeric values as strings

    grade_levels.sort(key=sort_key)
    form = AddGradeLevelForm()
    return render_template('admin/manage_grade_levels.html', grade_levels=grade_levels, form=form)


###############################################################################
# Manage Graduation Years (Add, Edit, Delete, List)
###############################################################################

@admin_bp.route('/add_graduation_year', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def add_graduation_year():
    form = AddGraduationYearForm()
    if form.validate_on_submit():
        graduation_year = GraduationYear(graduation_year=form.graduation_year.data)
        db.session.add(graduation_year)
        db.session.commit()
        flash('Graduation Year added successfully.', 'success')
        return redirect(url_for('admin.manage_graduation_years'))
    return render_template('admin/add_graduation_year.html', form=form)


@admin_bp.route('/edit_graduation_year/<int:graduation_year_id>', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def edit_graduation_year(graduation_year_id):
    graduation_year = GraduationYear.query.get_or_404(graduation_year_id)
    form = EditGraduationYearForm(obj=graduation_year)
    if form.validate_on_submit():
        graduation_year.graduation_year = form.graduation_year.data
        db.session.commit()
        flash('Graduation Year updated successfully.', 'success')
        return redirect(url_for('admin.manage_graduation_years'))
    return render_template('admin/edit_graduation_year.html', form=form, graduation_year=graduation_year)


@admin_bp.route('/delete_graduation_year/<int:graduation_year_id>', methods=['POST'])
@admin_required  # Corrected decorator
def delete_graduation_year(graduation_year_id):
    graduation_year = GraduationYear.query.get_or_404(graduation_year_id)
    db.session.delete(graduation_year)
    db.session.commit()
    flash('Graduation Year deleted successfully.', 'success')
    return redirect(url_for('admin.manage_graduation_years'))


@admin_bp.route('/manage_graduation_years')
@admin_required  # Corrected decorator
def manage_graduation_years():
    graduation_years = GraduationYear.query.order_by(GraduationYear.graduation_year).all()
    form = AddGraduationYearForm()
    return render_template('admin/manage_graduation_years.html', graduation_years=graduation_years, form=form)


###############################################################################
# Manage Home Page Content (Add, Edit, Delete, List)
###############################################################################

@admin_bp.route('/add_home_page_content', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def add_home_page_content():
    form = AddHomePageContentForm()
    if form.validate_on_submit():
        content = HomePageContent(
            content_title=form.content_title.data,
            content_text=form.content_text.data
        )
        db.session.add(content)
        db.session.commit()
        flash('Home Page Content added successfully.', 'success')
        return redirect(url_for('admin.home_page_content_list'))
    return render_template('admin/add_home_page_content.html', form=form)


@admin_bp.route('/edit_home_page_content/<int:content_id>', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def edit_home_page_content(content_id):
    content = HomePageContent.query.get_or_404(content_id)
    form = EditHomePageContentForm(obj=content)
    if form.validate_on_submit():
        content.content_title = form.content_title.data
        content.content_text = form.content_text.data
        db.session.commit()
        flash('Home Page Content updated successfully.', 'success')
        return redirect(url_for('admin.home_page_content_list'))
    return render_template('admin/edit_home_page_content.html', form=form, content=content)


@admin_bp.route('/delete_home_page_content/<int:content_id>', methods=['POST'])
@admin_required  # Corrected decorator
def delete_home_page_content(content_id):
    content = HomePageContent.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    flash('Home Page Content deleted successfully.', 'success')
    return redirect(url_for('admin.home_page_content_list'))


@admin_bp.route('/home_page_content_list')
@admin_required  # Corrected decorator
def home_page_content_list():
    content = HomePageContent.query.all()
    return render_template('admin/home_page_content_list.html', content=content)


###############################################################################
# Manage Buildings (Add, Edit, Delete, List) - Moved from settings.py
###############################################################################

@admin_bp.route('/manage_buildings', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def manage_buildings():
    form = AddBuildingForm()
    buildings = Building.query.all()
    if form.validate_on_submit():
        new_building = Building(name=form.building_name.data)  # Use form.building_name.data
        db.session.add(new_building)
        db.session.commit()
        flash(f"Building '{new_building.building_name.data}' added successfully!", 'success')
        return redirect(url_for('admin.manage_buildings'))
    return render_template('admin/manage_buildings.html', buildings=buildings, form=form)


@admin_bp.route('/add_building', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def add_building():
    form = AddBuildingForm()
    if form.validate_on_submit():
        building = Building(name=form.building_name.data)
        db.session.add(building)
        db.session.commit()
        flash('Building added successfully.', 'success')
        return redirect(url_for('admin.manage_buildings'))
    return render_template('admin/add_building.html', form=form)


@admin_bp.route('/edit_building/<int:building_id>', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def edit_building(building_id):
    building = Building.query.get_or_404(building_id)
    form = EditBuildingForm(obj=building)
    if form.validate_on_submit():
        building.name = form.building_name.data  # Use form.building_name.data
        db.session.commit()
        flash(f"Building '{building.name}' updated successfully!", 'success')
        return redirect(url_for('admin.manage_buildings'))
    return render_template('admin/edit_building.html', form=form, building=building)


@admin_bp.route('/delete_building/<int:building_id>', methods=['POST'])
@admin_required  # Corrected decorator
def delete_building(building_id):
    building = Building.query.get_or_404(building_id)
    db.session.delete(building)
    db.session.commit()
    flash(f"Building '{building.name}' deleted successfully!", 'success')
    return redirect(url_for('admin.manage_buildings'))


###############################################################################
# Manage Allowed Domains - Moved from settings.py
###############################################################################
@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def settings():
    settings_data = Settings.query.first()
    if not settings_data:
        settings_data = Settings()
        db.session.add(settings_data)
        db.session.commit()

    if request.method == 'POST':
        print("POST request received for /settings")
        if 'add_domain' in request.form:
            print("add_domain button found in request.form")
            domain = request.form['domain']
            if not domain.startswith('@'):
                domain = '@' + domain
            new_domain = AllowedDomain(domain=domain)
            db.session.add(new_domain)
            db.session.commit()
            flash(f"Domain '{domain}' added successfully!", 'success')
            return redirect(url_for('admin.settings'))
        else:
            print("add_domain button NOT found in request.form - Processing main settings")
            rss_enabled = request.form.get('rss_feed_enabled') == 'on'
            mail_user = request.form.get('mail_username')
            mail_pass = request.form.get('mail_password')

            print(
                f"Retrieved from form - RSS Enabled: {rss_enabled}, Mail Username: {mail_user}, Mail Password: {mail_pass}")

            settings_data.rss_feed_enabled = rss_enabled
            settings_data.mail_username = mail_user
            settings_data.mail_password = mail_pass

            db.session.commit()
            print("Settings data committed to database")
            flash("Settings updated successfully!", "success")
            print("Flash message set")
            return redirect(url_for('admin.settings'))

    allowed_domains = AllowedDomain.query.all()
    return render_template('admin/settings.html', settings=settings_data, domains=allowed_domains)


@admin_bp.route('/allowed_domains', methods=['GET', 'POST'])
@admin_required  # Corrected decorator
def allowed_domains():
    if request.method == 'POST':
        domain = request.form['domain']
        if not domain.startswith('@'):
            domain = '@' + domain
        new_domain = AllowedDomain(domain=domain)
        db.session.add(new_domain)
        db.session.commit()
        flash(f"Domain '{domain}' added successfully!", 'success')
        return redirect(url_for('admin.allowed_domains'))
    domains = AllowedDomain.query.all()
    return render_template('admin/allowed_domains.html', domains=domains)


@admin_bp.route('/allowed_domains/delete/<int:domain_id>', methods=['POST'])
@admin_required  # Corrected decorator
def delete_allowed_domain(domain_id):
    domain = AllowedDomain.query.get_or_404(domain_id)
    db.session.delete(domain)
    db.session.commit()
    flash(f"Domain '{domain.domain}' deleted successfully!", 'success')
    return redirect(url_for('admin.allowed_domains'))


###############################################################################
# Modify Tables - Moved from settings.py
###############################################################################

@admin_bp.route('/modify_tables')
@admin_required  # Corrected decorator
def modify_tables():
    return render_template('admin/modify_tables.html')


###############################################################################
# Manage Lockers (Add, Edit, Delete, List)
###############################################################################


@admin_bp.route('/manage_lockers', defaults={'page': 1})
@admin_bp.route('/manage_lockers/page/<int:page>')
@admin_required
def manage_lockers(page):
    per_page = 10  # You can adjust the number of lockers per page
    lockers_pagination = Locker.query.paginate(page=page, per_page=per_page)
    return render_template('admin/manage_lockers.html', assigned_lockers_pagination=lockers_pagination)


@admin_bp.route('/add_locker', methods=['GET', 'POST'])
@admin_required
def add_locker():
    form = AddLockerForm()  # Assuming you have this form to add lockers
    if form.validate_on_submit():
        locker = Locker(
            location=form.location.data,  # Adjust based on the fields you need
            building_id=form.building_id.data  # Assuming you have a foreign key to Building
        )
        db.session.add(locker)
        db.session.commit()
        flash('Locker added successfully.', 'success')
        return redirect(url_for('admin.manage_lockers'))
    return render_template('admin/add_locker.html', form=form)


@admin_bp.route('/edit_locker/<int:locker_id>', methods=['GET', 'POST'])
@admin_required
def edit_locker(locker_id):
    locker = Locker.query.get_or_404(locker_id)
    form = EditLockerForm(obj=locker)
    if form.validate_on_submit():
        locker.location = form.location.data  # Adjust based on your model's fields
        locker.building_id = form.building_id.data
        db.session.commit()
        flash('Locker updated successfully.', 'success')
        return redirect(url_for('admin.manage_lockers'))
    return render_template('admin/edit_locker.html', form=form, locker=locker)


@admin_bp.route('/delete_locker/<int:locker_id>', methods=['POST'])
@admin_required
def delete_locker(locker_id):
    locker = Locker.query.get_or_404(locker_id)
    db.session.delete(locker)
    db.session.commit()
    flash('Locker deleted successfully.', 'success')
    return redirect(url_for('admin.manage_lockers'))


###############################################################################
# Locker Stats
###############################################################################
@admin_bp.route('/locker_stats')
@login_required
@admin_required
def locker_stats():
    # All lockers
    lockers = Locker.query.all()

    # Total number of lockers
    total_lockers = len(lockers)

    # Lockers that are assigned
    assigned_lockers = sum(1 for locker in lockers if locker.assigned_user_id)

    # Available lockers are the difference
    available_lockers = total_lockers - assigned_lockers

    # Percentage of lockers that are assigned
    percentage_assigned = (assigned_lockers / total_lockers * 100) if total_lockers > 0 else 0

    # Paginated data for buildings
    building_page = request.args.get("building_page", 1, type=int)
    buildings_pagination = Building.query.paginate(page=building_page, per_page=5)
    for building in buildings_pagination.items:
        building.total_lockers = len(building.lockers)
        building.assigned_lockers = sum(1 for locker in building.lockers if locker.assigned_user_id)
        building.available_lockers = building.total_lockers - building.assigned_lockers
        building.percentage_assigned = (
                building.assigned_lockers / building.total_lockers * 100) if building.total_lockers else 0

    # Paginated data for recent assignments
    recent_page = request.args.get("recent_page", 1, type=int)
    recent_assignments_pagination = Locker.query.filter(Locker.assigned_user_id.isnot(None)) \
        .order_by(Locker.assignment_date.desc()) \
        .paginate(page=recent_page, per_page=5)

    # Prepare stats for the pie chart (or other visualizations)
    stats = {
        "labels": ["Assigned", "Available"],
        "values": [assigned_lockers, available_lockers],
    }

    return render_template(
        'admin/locker_stats.html',
        total_lockers=total_lockers,
        assigned_lockers=assigned_lockers,
        available_lockers=available_lockers,  # Get recent user registrations (last 5)
        percentage_assigned=round(percentage_assigned, 2),
        stats=stats,
        buildings_pagination=buildings_pagination,
        recent_assignments_pagination=recent_assignments_pagination
    )
