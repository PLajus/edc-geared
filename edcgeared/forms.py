from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, InputRequired, Length, ValidationError
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
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken.')

class LoginForm(FlaskForm):

    """User log in form"""

    email = StringField('Email', validators=[InputRequired(), Email()])

    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')

    submit = SubmitField("Sign in")
    