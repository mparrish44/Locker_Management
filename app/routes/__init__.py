from .auth import auth_bp
from .lockers import lockers_bp
from .admin import admin_bp
from .main import main_bp
from .teacher import teacher_bp  # Import the teacher blueprint

# Expose blueprints for easier imports in app/__init__.py
__all__ = ['auth_bp', 'lockers_bp', 'admin_bp', 'main_bp', 'teacher_bp']  # Add teacher_bp to the list
