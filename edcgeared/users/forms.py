from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from edcgeared.models import User

class RegistrationForm(FlaskForm):

    """User registration form"""

    email = StringField('Email', validators=[InputRequired(), Email()])

    first_name = StringField('First name', validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=1, max=30)])

    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm password',
    validators=[InputRequired(), EqualTo('password')])

    submit = SubmitField("Sign up")

    def validate_email(self, email):
        """Validate email"""

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken.')

class LoginForm(FlaskForm):

    """User log in form"""

    email = StringField('Email', validators=[InputRequired(), Email()])

    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')

    submit = SubmitField("Sign in")

class UpdateProfileForm(FlaskForm):

    """User account update form"""

    email = StringField('Email', validators=[InputRequired(), Email()])

    first_name = StringField('First name', validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=1, max=30)])

    image = FileField('Update profile image', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Save")

    def validate_email(self, email):
        """Check if email is taken when user changes email"""

        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken.')
