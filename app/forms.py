import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange, Optional
from app.models import User, GradeLevel, GraduationYear, Building, HomePageContent, Locker
from app.utils import teacher_required, admin_required, student_required  # Importing specific decorators


# ============================
#    Validation Functions
# ============================

def validate_student_id(form, field):
    if User.query.filter_by(studentID=field.data).first():
        raise ValidationError('Student ID already registered.')


def validate_email(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')


def validate_password(form, field):
    password = field.data
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")


# ============================
#    User Forms
# ============================

class StudentRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()],
                       description="Your email address will be used as your username.")
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), validate_password])
    student_id = StringField('Student ID', validators=[DataRequired()])
    grade_level = SelectField('Grade Level', validators=[DataRequired()], coerce=int, choices=[])
    graduation_year = SelectField('Graduation Year', validators=[DataRequired()], coerce=int, choices=[])
    agreement = BooleanField('I have read and agree to the terms.', validators=[DataRequired()])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)

        grade_choices = [(g.id, str(g.grade_level)) for g in GradeLevel.query.all()]
        self.grade_level.choices = grade_choices

        year_choices = [(y.id, str(y.graduation_year)) for y in GraduationYear.query.all()]
        self.graduation_year.choices = year_choices


class TeacherRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()],
                       description="Your email address will be used as your username.")
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), validate_password])
    submit = SubmitField('Register')


class AddUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()],
                       description="Your email address will be used as your username.")
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), validate_password])

    # Student-specific fields
    student_id = StringField('Student ID', validators=[DataRequired()], render_kw={'placeholder': 'e.g. 12345'})
    grade_level = SelectField('Grade Level', coerce=int, validators=[DataRequired()], choices=[])
    graduation_year = SelectField('Graduation Year', coerce=int, validators=[DataRequired()], choices=[])

    # Teacher-specific field
    is_teacher = BooleanField('Is Teacher', default=False)

    # Agreement field for both admin and teacher
    agreement = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])

    submit = SubmitField('Save User')

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)

        # Populate choices for students
        if not self.is_teacher.data:  # if it's a student
            self.grade_level.choices = [(g.id, str(g.grade_level)) for g in GradeLevel.query.all()]
            self.graduation_year.choices = [(y.id, str(y.graduation_year)) for y in GraduationYear.query.all()]
        else:
            # For teachers, you can disable student-related fields
            self.student_id.render_kw = {'disabled': 'disabled'}
            self.grade_level.render_kw = {'disabled': 'disabled'}
            self.graduation_year.render_kw = {'disabled': 'disabled'}

class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()],
                       description="Your email address will be used as your username.")
    password = PasswordField('Password', validators=[Optional(), Length(min=8), validate_password])

    # Student-specific fields
    student_id = StringField('Student ID', validators=[Optional()], render_kw={'placeholder': 'e.g. 12345'})
    grade_level = SelectField('Grade Level', coerce=int, validators=[Optional()], choices=[])
    graduation_year = SelectField('Graduation Year', coerce=int, validators=[Optional()], choices=[])

    # Teacher-specific field
    is_teacher = BooleanField('Is Teacher', default=False)

    submit = SubmitField('Save Changes')

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        # Populate choices for students
        if not self.is_teacher.data:  # if it's a student
            self.grade_level.choices = [(g.id, str(g.grade_level)) for g in GradeLevel.query.all()]
            self.graduation_year.choices = [(y.id, str(y.graduation_year)) for y in GraduationYear.query.all()]
        else:
            # For teachers, you can disable student-related fields
            self.student_id.render_kw = {'disabled': 'disabled'}
            self.grade_level.render_kw = {'disabled': 'disabled'}
            self.graduation_year.render_kw = {'disabled': 'disabled'}


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('Remember Me')  # This might be missing
    submit = SubmitField('Log In')


# ============================
#    Locker Forms
# ============================
class AssignLockerForm(FlaskForm):
    locker_id = SelectField('Locker', coerce=int, validators=[DataRequired()])
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Locker')

    def __init__(self, *args, **kwargs):
        super(AssignLockerForm, self).__init__(*args, **kwargs)
        # Populate the locker choices from the database
        self.locker_id.choices = [(locker.id, f"Locker {locker.locker_id}") for locker in Locker.query.all()]
        # Populate the user choices from the database
        self.user_id.choices = [(user.id, f"{user.first_name} {user.last_name}") for user in User.query.all()]


class AddLockerForm(FlaskForm):
    locker_id = IntegerField('Locker ID', validators=[DataRequired()])
    building_id = SelectField('Building', coerce=int, validators=[DataRequired()])
    floor = StringField('Floor', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    submit = SubmitField('Add Locker')

    def __init__(self, *args, **kwargs):
        super(AddLockerForm, self).__init__(*args, **kwargs)
        self.building_id.choices = [(building.id, building.building_name) for building in Building.query.all()]


class EditLockerForm(FlaskForm):
    building_id = SelectField('Building', coerce=int, validators=[DataRequired()])
    floor = StringField('Floor', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    submit = SubmitField('Update Locker')

    def __init__(self, *args, **kwargs):
        super(EditLockerForm, self).__init__(*args, **kwargs)
        self.building_id.choices = [(building.id, building.building_name) for building in Building.query.all()]


# ============================
#    Building Forms
# ============================

class AddBuildingForm(FlaskForm):
    building_name = StringField('Building Name', validators=[DataRequired()])
    submit = SubmitField('Add Building')


class EditBuildingForm(FlaskForm):
    building_name = StringField('Building Name', validators=[DataRequired()])
    submit = SubmitField('Update Building')


# ============================
#    Grade Level Forms
# ============================

class AddGradeLevelForm(FlaskForm):
    grade_level = StringField('Grade Level', validators=[DataRequired()])
    submit = SubmitField('Add Grade Level')


class EditGradeLevelForm(FlaskForm):
    grade_level = StringField('Grade Level', validators=[DataRequired()])
    submit = SubmitField('Update Grade Level')


# ============================
#    Graduation Year Forms
# ============================

class AddGraduationYearForm(FlaskForm):
    graduation_year = IntegerField('Graduation Year',
                                   validators=[DataRequired(), NumberRange(min=2000)])  # Adjust min year as needed
    submit = SubmitField('Add Graduation Year')


class EditGraduationYearForm(FlaskForm):
    graduation_year = IntegerField('Graduation Year',
                                   validators=[DataRequired(), NumberRange(min=2000)])  # Adjust min year as needed
    submit = SubmitField('Update Graduation Year')


# ============================
#    Home Page Content Forms
# ============================

class AddHomePageContentForm(FlaskForm):
    content_title = StringField('Content Title', validators=[DataRequired()])
    content_text = StringField('Content Text', validators=[DataRequired()])
    submit = SubmitField('Add Content')


class EditHomePageContentForm(FlaskForm):
    content_title = StringField('Content Title', validators=[DataRequired()])
    content_text = StringField('Content Text', validators=[DataRequired()])
    submit = SubmitField('Update Content')


# ============================
#    RSS Feed
# ============================

class RssForm(FlaskForm):
    url = StringField('RSS Feed URL', validators=[DataRequired()])
    submit = SubmitField('Submit')
