from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from app.models import HomePageContent
from app.extensions import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    role = session.get("role")
    if role == "student":
        return redirect(url_for("lockers.student_dashboard"))
    elif role == "teacher":
        return redirect(url_for("teacher.dashboard"))
    elif role == "admin":
        return redirect(url_for("admin.admin_dashboard"))

    # For non-authenticated users, display the public homepage
    return render_template("index.html")


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')


@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')


@main_bp.route('/terms')
def terms():
    return render_template('terms.html')


@main_bp.route('/sitemap.xml')
def sitemap():
    # This is a basic example, you might want to generate this dynamically
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>{{ url_for('main.index', _external=True) }}</loc>
            <priority>1.0</priority>
        </url>
        <url>
            <loc>{{ url_for('auth.register_student', _external=True) }}</loc>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{{ url_for('auth.student_login', _external=True) }}</loc>
            <priority>0.8</priority>
        </url>
        <url>
            <loc>{{ url_for('about', _external=True) }}</loc>
            <priority>0.5</priority>
        </url>
        <url>
            <loc>{{ url_for('contact', _external=True) }}</loc>
            <priority>0.5</priority>
        </url>
        </urlset>
    """
    from flask import Response
    response = Response(xml_content, mimetype='application/xml')
    return response
