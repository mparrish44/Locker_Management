from functools import wraps
from flask import redirect, url_for, flash, session, request
from flask_login import current_user


def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated and has teacher role
        if not current_user.is_authenticated or not current_user.is_teacher():
            flash("Access restricted to teachers!", "danger")
            return redirect(url_for('auth.login', next=request.url))  # Redirect to login with `next`
        return f(*args, **kwargs)

    return decorated_function


def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated and has student role
        if not current_user.is_authenticated or not current_user.is_student():
            flash("Access restricted to students!", "danger")
            return redirect(url_for('auth.login', next=request.url))  # Redirect to login with `next`
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated and has admin role
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("You must be an admin to access this page.", "danger")
            return redirect(url_for('auth.login', next=request.url))  # Redirect to login with `next`
        return f(*args, **kwargs)

    return decorated_function
