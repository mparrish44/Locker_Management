from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum
from sqlalchemy.types import TypeDecorator, String
from flask_login import UserMixin  # Import UserMixin to integrate with Flask-Login


# Define the roles using Enum
class RoleEnum(Enum):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'


# Custom TypeDecorator for case-insensitive enum storage
class LowercaseEnum(TypeDecorator):
    """
    Custom SQLAlchemy type to store Enum values as lowercase strings in the database
    and retrieve them as their corresponding Enum members.
    """
    impl = String  # Store as a string in the database

    def __init__(self, enumtype):
        self.enumtype = enumtype
        super().__init__()

    def process_bind_param(self, value, dialect):
        """Convert Enum -> lowercase string before storing in the DB."""
        if value is None:
            return value
        return value.value.lower()

    def process_result_value(self, value, dialect):
        """Convert lowercase string from database -> Enum."""
        if value is None:
            return value
        for enum_member in self.enumtype:
            if value.lower() == enum_member.value.lower():
                return enum_member
        raise ValueError(f"'{value}' is not a valid {self.enumtype.__name__}")


# User model
class User(UserMixin, db.Model):  # Inherit from UserMixin for Flask-Login integration
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.String(50), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # Add role if you don't have it
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_by_teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    agreement_acknowledged = db.Column(db.Boolean, default=False)

    # Role column uses the LowercaseEnum to handle serialization/deserialization
    role = db.Column(LowercaseEnum(RoleEnum), default=RoleEnum.STUDENT, nullable=False)
    rss_feed = db.Column(db.String(255))

    grade_level_id = db.Column(db.Integer, db.ForeignKey('grade_levels.id'))
    graduation_year_id = db.Column(db.Integer, db.ForeignKey('graduation_years.id'))

    # Add this line:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one relationship to Locker
    assigned_locker = db.relationship(
        'Locker',
        uselist=False,
        back_populates='assigned_to_user',
        overlaps="lockers_assigned,user"
    )

    # ... (rest of your User model code)
    def set_password(self, password):
        """Hash the password and store it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password matches the hashed version."""
        return check_password_hash(self.password, password)

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Human-readable representation of a User object."""
        return f"<User {self.full_name}, Email: {self.email}, Role: {self.role.value}>"

    # Role check methods
    def is_admin(self):
        """Check if the user is an admin."""
        return self.role == RoleEnum.ADMIN

    def is_teacher(self):
        """Check if the user is a teacher."""
        return self.role == RoleEnum.TEACHER

    def is_student(self):
        """Check if the user is a student."""
        return self.role == RoleEnum.STUDENT


class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lockers = db.relationship('Locker', back_populates='building', lazy=True)

    @property
    def building_name(self):
        return self.name

    def __repr__(self):
        return f"<Building {self.name}>"


class GradeLevel(db.Model):
    __tablename__ = "grade_levels"
    id = db.Column(db.Integer, primary_key=True)
    grade_level = db.Column(db.String(10), unique=True, nullable=False)
    users = db.relationship('User', backref='grade_level', lazy=True)
    graduation_years = db.relationship('GraduationYear', backref='grade_level', lazy=True)


class GraduationYear(db.Model):
    __tablename__ = "graduation_years"
    id = db.Column(db.Integer, primary_key=True)
    graduation_year = db.Column(db.Integer, unique=True, nullable=False)
    grade_level_id = db.Column(db.Integer, db.ForeignKey('grade_levels.id'))
    users = db.relationship('User', backref='graduation_year', lazy=True)


class HomePageContent(db.Model):
    __tablename__ = "home_page_content"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Locker(db.Model):
    __tablename__ = "lockers"
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    locker_number = db.Column(db.String(255), nullable=False)
    floor = db.Column(db.String(10))
    section = db.Column(db.String(10))
    available = db.Column(db.Boolean, default=True)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assignment_date = db.Column(db.DateTime, default=datetime.utcnow)

    building = db.relationship('Building', back_populates='lockers')

    # Many-to-one relationship to User
    assigned_to_user = db.relationship(
        'User',
        back_populates='assigned_locker',
        overlaps="lockers_assigned,user"
    )


class AllowedDomain(db.Model):
    __tablename__ = "allowed_domains"
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<AllowedDomain {self.domain}>'


class Settings(db.Model):
    __tablename__ = "settings"
    id = db.Column(db.Integer, primary_key=True)
    rss_feed_enabled = db.Column(db.Boolean, default=False)
    mail_username = db.Column(db.String(255))
    mail_password = db.Column(db.String(255))

    def __repr__(self):
        return f"<Settings rss_enabled={self.rss_feed_enabled}, mail_username={self.mail_username}>"
