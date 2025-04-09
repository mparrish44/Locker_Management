from flask import Flask, render_template
from flask_login import LoginManager
from app.extensions import db, migrate, mail, cors, jwt  # Import initialized extensions
from .models import GradeLevel, GraduationYear, Locker, Settings, User, AllowedDomain, HomePageContent
from .populate_data import populate_grade_and_graduation, populate_settings
import os
import sys


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'lockers.db')
    app.config['RSS_ENABLED'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = app.config['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = app.config['MAIL_PASSWORD']
    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    # Initialize extensions
    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)  # Initialize SQLAlchemy with the app
    migrate.init_app(app, db)
    mail.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Adjust to 'auth.login' since login is in the auth blueprint

    # Define user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Ensure this query is valid for your User model

    with app.app_context():
        populate_grade_and_graduation()
        if not (len(sys.argv) > 1 and sys.argv[1] in ['db', 'db.py']):
            populate_settings()

    # Import blueprints
    from app.routes import auth_bp, lockers_bp, admin_bp, main_bp, teacher_bp  # Import all required blueprints
    app.register_blueprint(auth_bp)  # Register auth blueprint
    app.register_blueprint(lockers_bp)  # Register lockers blueprint
    app.register_blueprint(admin_bp)  # Register admin blueprint
    app.register_blueprint(main_bp)  # Register main blueprint
    app.register_blueprint(teacher_bp, url_prefix='/teacher')  # Register teacher blueprint with a '/teacher' prefix

    # Add a context processor to inject models globally
    @app.context_processor
    def inject_models():
        settings = Settings.query.first()  # Inject settings into the context
        return dict(Locker=Locker, Settings=settings, User=User)

    return app


# Main entry point
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
