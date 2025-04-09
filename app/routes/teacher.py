from flask import render_template, redirect, url_for, flash, request, Blueprint, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Locker, Building
from app.forms import AddUserForm, EditUserForm, EditLockerForm, AddLockerForm, DeleteUserForm
from app.utils import teacher_required  # Your custom decorator
from app.database import db
from app.models import RoleEnum
from collections import defaultdict

teacher_bp = Blueprint('teacher', __name__)


# Redirect the teacher to the dashboard after login
@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    print(f"Session data on teacher dashboard: {session}")  # Add this line
    return render_template('teacher/dashboard_teacher.html')  # Dashboard view template


# Manage Users with Pagination
@teacher_bp.route('/manage_users', defaults={'page': 1})
@teacher_bp.route('/manage_users/page/<int:page>')
@login_required
@teacher_required
def manage_users(page):
    per_page = 10  # Users per page
    users_pagination = User.query.paginate(page=page, per_page=per_page)
    delete_form = DeleteUserForm()  # Instantiate the delete form
    return render_template(
        'teacher/manage_users.html',
        users_pagination=users_pagination,
        delete_form=delete_form  # Pass the form to the template
    )


# Search Users
@teacher_bp.route('/search_users')
@login_required
@teacher_required
def search_users():
    query = request.args.get('query')
    if query:
        search_term = f'%{query.lower()}%'
        users_pagination = User.query.filter(
            (db.func.lower(User.first_name).like(search_term)) |
            (db.func.lower(User.last_name).like(search_term)) |
            (db.func.lower(User.email).like(search_term))
        ).paginate(page=1, per_page=10)
    else:
        users_pagination = User.query.paginate(page=1, per_page=10)
    delete_form = DeleteUserForm()  # Instantiate the delete form
    return render_template('teacher/manage_users.html', users_pagination=users_pagination,
                           delete_form=delete_form)  # Pass the form


# Add User Form Handling
@teacher_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        student_id = form.student_id.data
        grade_level_id = form.grade_level.data
        graduation_year_id = form.graduation_year.data
        is_teacher = form.is_teacher.data
        agreement = form.agreement.data
        creating_teacher = current_user

        role = RoleEnum.TEACHER if is_teacher else RoleEnum.STUDENT

        new_user = User(
            studentID=student_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,  # Assign the RoleEnum value
            created_by_teacher_id=creating_teacher.id,
            agreement_acknowledged=agreement,
            grade_level_id=grade_level_id,
            graduation_year_id=graduation_year_id
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully!", "success")
        return redirect(url_for('teacher.manage_users'))

    return render_template('teacher/add_user.html', form=form)


# Edit Existing Users
@teacher_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)  # Instantiate the form and populate with user data

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        # Only update password if a new one is provided
        if form.password.data:
            user.set_password(form.password.data)
        user.role = RoleEnum.TEACHER if form.is_teacher.data else RoleEnum.STUDENT

        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('teacher.manage_users'))

    return render_template('teacher/edit_user.html', user=user, form=form)


# Delete Users
@teacher_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@teacher_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for('teacher.manage_users'))


# Assign Lockers to Users
@teacher_bp.route('/assign_locker', methods=['GET', 'POST'])
@login_required
@teacher_required
def assign_locker():
    buildings = Building.query.all()
    available_lockers = Locker.query.filter_by(assigned_user_id=None).all()
    grouped_lockers = defaultdict(list)

    for locker in available_lockers:
        grouped_lockers[locker.building].append(locker)

    for building in grouped_lockers:
        grouped_lockers[building].sort(
            key=lambda locker: (locker.floor if locker.floor is not None else '', locker.locker_number))

    # Filter users to only include those who do not have an assigned locker
    users = User.query.outerjoin(Locker, User.id == Locker.assigned_user_id).filter(Locker.id.is_(None)).all()

    student_query = request.args.get('student_query')
    selected_building_id = request.form.get('building_id', type=int)

    if student_query:
        users = User.query.outerjoin(Locker, User.id == Locker.assigned_user_id).filter(Locker.id.is_(None)).filter(
            db.or_(
                User.first_name.like(f'%{student_query}%'),
                User.last_name.like(f'%{student_query}%'),
                User.email.like(f'%{student_query}%'),
                db.func.lower(User.first_name + ' ' + User.last_name).like(f'%{student_query.lower()}%')
            )).all()

    if selected_building_id:
        grouped_lockers = {building: lockers for building, lockers in grouped_lockers.items() if
                           building and building.id == selected_building_id}

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        locker_id = request.form.get('locker_id')

        if not user_id or not locker_id:
            flash("Both student and locker must be selected!", "danger")
        else:
            locker = Locker.query.get_or_404(locker_id)
            locker.assigned_user_id = user_id
            db.session.commit()
            flash("Locker assigned successfully!", "success")
            return redirect(url_for('teacher.view_lockers'))

    return render_template('teacher/assign_locker.html',
                           buildings=buildings,
                           grouped_lockers=grouped_lockers,
                           users=users,
                           student_query=student_query,
                           selected_building_id=selected_building_id)


# Unassign a Locker
@teacher_bp.route('/unassign_locker/<int:locker_id>', methods=['POST'])
@login_required
@teacher_required
def unassign_locker(locker_id):
    locker = Locker.query.get_or_404(locker_id)
    locker.assigned_user_id = None
    db.session.commit()
    flash(f"Locker {locker.locker_number} has been unassigned.", "success")
    return redirect(url_for('teacher.view_lockers'))


# View Lockers
@teacher_bp.route('/view_lockers', defaults={'page': 1})
@teacher_bp.route('/view_lockers/page/<int:page>')
@login_required
@teacher_required
def view_lockers(page):
    per_page = 10
    status = request.args.get('status')
    building_id = request.args.get('building_id', type=int)
    floor = request.args.get('floor')

    query = Locker.query.join(Building).outerjoin(User, Locker.assigned_user_id == User.id)

    if status == 'available':
        query = query.filter(Locker.assigned_user_id.is_(None))
    elif status == 'assigned':
        query = query.filter(Locker.assigned_user_id.isnot(None))

    if building_id:
        query = query.filter(Locker.building_id == building_id)

    if floor:
        query = query.filter(Locker.floor == floor)

    query = query.order_by(
        Building.__table__.c.name,
        Locker.__table__.c.floor,
        Locker.__table__.c.locker_number,
        User.__table__.c.last_name
    )

    lockers_pagination = query.paginate(page=page, per_page=per_page)
    delete_form = DeleteUserForm()
    buildings = Building.query.all()  # Added this line back
    return render_template('teacher/view_lockers.html',
                           lockers_pagination=lockers_pagination,
                           delete_form=delete_form,
                           buildings=buildings,
                           current_building_id=building_id,
                           current_floor=floor,
                           current_status=status)


# Locker Statistics Visualization
@teacher_bp.route('/locker_stats')
@login_required
@teacher_required
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
        'teacher/locker_stats.html',
        total_lockers=total_lockers,
        assigned_lockers=assigned_lockers,
        available_lockers=available_lockers,
        percentage_assigned=round(percentage_assigned, 2),
        stats=stats,
        buildings_pagination=buildings_pagination,
        recent_assignments_pagination=recent_assignments_pagination
    )
