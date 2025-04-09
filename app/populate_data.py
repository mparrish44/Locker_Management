from app.database import db
from app.models import GradeLevel, GraduationYear, Settings


def populate_grade_and_graduation():
    """Populates grade_level and graduation_year tables."""

    grade_levels = [
        GradeLevel(grade_level=9),
        GradeLevel(grade_level=10),
        GradeLevel(grade_level=11),
        GradeLevel(grade_level=12),
    ]

    graduation_years = [
        GraduationYear(graduation_year=2028, grade_level_id=1),  # 9th grade
        GraduationYear(graduation_year=2027, grade_level_id=2),  # 10th grade
        GraduationYear(graduation_year=2026, grade_level_id=3),  # 11th grade
        GraduationYear(graduation_year=2025, grade_level_id=4),  # 12th grade
    ]

    # Check if the tables are already populated.
    if not GradeLevel.query.first():
        db.session.add_all(grade_levels)
    if not GraduationYear.query.first():
        db.session.add_all(graduation_years)
    db.session.commit()

def populate_settings():
    """Creates initial settings if the table is empty."""
    if not db.session.query(Settings).count() > 0:
        initial_settings = Settings(rss_feed_enabled=False, mail_username=None, mail_password=None)
        db.session.add(initial_settings)
        db.session.commit()

# Call the function when your application starts (e.g., in your __init__.py or app.py)
# from app import app
# with app.app_context():
#     populate_grade_and_graduation()
#     populate_settings()