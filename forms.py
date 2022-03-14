from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length

class RegistrationForm(FlaskForm):

    """User registration form"""

    email = StringField('Email', validators=[DataRequired(), Email()])

    first_name = StringField('First name', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=1, max=50)])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):

    """User log in form"""

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')

    submit = SubmitField("Sign in")
    