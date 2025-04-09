from flask import render_template, redirect, url_for, flash, request, Blueprint, session
from flask_login import login_user, current_user
from app import db  # Import db
from app.forms import StudentRegistrationForm, TeacherRegistrationForm, LoginForm  # Import Teacher forms
from app.models import User, GradeLevel, GraduationYear, AllowedDomain, RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/select_role')
def select_role():
    return render_template('select_role.html')


@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()

    if form.is_submitted():  # Check if the form was submitted
        if form.validate():  # Check if the form validates
            email = form.email.data
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email address already registered. Please use a different email.", "danger")
                return render_template('register_student.html', form=form)

            allowed_domains = AllowedDomain.query.all()
            domain_allowed = False
            user_domain = email.split('@')[1] if '@' in email else ''

            for allowed in allowed_domains:
                allowed_pattern = allowed.domain.lstrip('@')
                if allowed.domain.startswith('@*.'):
                    if user_domain.endswith(allowed_pattern[2:]):
                        domain_allowed = True
                        break
                elif allowed.domain.startswith('@'):
                    if user_domain == allowed_pattern:
                        domain_allowed = True
                        break

            if not domain_allowed:
                flash(f"Registrations are not allowed from the domain \"{user_domain}\".", "danger")
                return render_template('register_student.html', form=form)

            hashed_password = generate_password_hash(form.password.data)

            new_student = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=email,
                password=hashed_password,
                studentID=form.student_id.data,
                grade_level_id=int(form.grade_level.data),
                graduation_year_id=int(form.graduation_year.data),
                is_admin=False  # Students should not have admin privileges
            )

            db.session.add(new_student)

            try:
                db.session.commit()
                flash(f"{form.first_name.data} registered successfully! Please log in.", "success")
                return redirect(url_for('auth.login'))
            except IntegrityError:
                db.session.rollback()
                flash("An error occurred during registration. Please try again.", "danger")
                return render_template('register_student.html', form=form)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('register_student.html', form=form)


@auth_bp.route('/teacher/register', methods=["GET", "POST"])
def register_teacher():
    form = TeacherRegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('auth.login'))

        hashed_password = generate_password_hash(form.password.data)

        # Teachers are not admin by default
        new_teacher = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=email,
            password=hashed_password,
            role=RoleEnum.TEACHER # Ensure the role is set correctly
        )

        db.session.add(new_teacher)
        db.session.commit()

        flash(f"{form.first_name.data} registered successfully! Please log in.", "success")
        return redirect(url_for('auth.login'))  # Redirect to login page after registration

    return render_template('teacher/register_teacher.html', form=form)

# Assuming auth_bp is your Blueprint object
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    # Use helper methods for the initial check
    if current_user.is_authenticated:
        print(f"Authenticated user role via method: {current_user.role.value}")  # Use .value for display if needed
        if current_user.is_admin():  # Use the helper method
            print("Redirecting authenticated admin user to admin dashboard.")
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.is_teacher():  # Use the helper method
            print("Redirecting authenticated teacher user to teacher dashboard.")
            return redirect(url_for('teacher.dashboard'))
        elif current_user.is_student():  # Use the helper method
            print("Redirecting authenticated student user to student dashboard.")
            return redirect(url_for('lockers.student_dashboard'))
        else:
            # Optional: Handle cases where a logged-in user might have an unexpected role
            flash("Logged in with unrecognized role.", "warning")
            return redirect(url_for('main.index'))  # Or a default page

    form = LoginForm()

    if form.validate_on_submit():
        print("Form successfully validated.")
        email = form.email.data
        password = form.password.data
        print(f"Attempting login with email: {email}")

        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User found: {user.email}")
            # You can use the model's check_password method too:
            # if user.check_password(password):
            if check_password_hash(user.password, password):  # Or keep using this, both work
                print(f"Password matched for user: {user.email}")
                login_user(user, remember=form.remember_me.data)
                session["username"] = user.full_name  # Added this line!
                session["role"] = user.role.value  # Add this line to store the role

                # Use helper methods for redirection after successful login
                print(f"User role via method: {user.role.value}")  # Display value if needed
                if user.is_admin():  # Use the helper method
                    print("Redirecting to admin dashboard...")
                    return redirect(url_for('admin.admin_dashboard'))
                elif user.is_teacher():  # Use the helper method
                    print("Redirecting to teacher dashboard...")
                    return redirect(url_for('teacher.dashboard'))
                elif user.is_student():  # Use the helper method
                    print("Redirecting to student dashboard...")
                    return redirect(url_for('lockers.student_dashboard'))
                else:
                    # Optional: Handle successful login but unexpected role
                    flash("Login successful, but role is unrecognized.", "warning")
                    return redirect(url_for('main.index'))  # Or a default page
            else:
                print("Password does not match for user:", email)
                flash("Invalid email or password. Please try again.", "danger")
        else:
            print("No user found with email:", email)
            flash("Invalid email or password. Please try again.", "danger")
    else:
        # Only print errors if validation *actually* failed (validate_on_submit is False on POST)
        if request.method == 'POST':  # Avoid logging this on initial GET request
            print("Form validation failed.")
            print("Validation errors:", form.errors)

    # Render the login form for GET requests or failed POST attempts
    return render_template("login.html", form=form)

@auth_bp.route('/debug-roles')
def debug_roles():
    # Fetch all users from the database
    users = User.query.all()
    output = []

    for user in users:
        role = user.role  # This should be a RoleEnum value
        is_admin = user.is_admin()
        is_teacher = user.is_teacher()
        is_student = user.is_student()

        output.append(
            f"User: {user.email} | Role: {role} | is_admin: {is_admin} | is_teacher: {is_teacher} | is_student: {is_student}"
        )

    return "<br>".join(output)  # Renders the debug info as an HTML response


@auth_bp.route('/logout')
def logout():
    session.clear()
    print("Session cleared:", session)  # Debugging line
    flash("You have successfully logged out.", "info")
    return redirect(url_for('main.index'))
