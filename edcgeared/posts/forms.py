from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    """Post form"""

    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    categories = SelectMultipleField('Categories', coerce=int, choices=[], default=['1'], validators=[DataRequired()])
    image = FileField('Update post image', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Post')
