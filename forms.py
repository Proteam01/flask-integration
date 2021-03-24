"""
defined forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    """
    form class wtforms for book
    """
    name = StringField('name', validators=[DataRequired()])
    type = StringField('type')
    created = DateField('created')
    save = SubmitField('save')
