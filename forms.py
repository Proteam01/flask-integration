import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    type = StringField('type')
    created = DateField('created')
    save = SubmitField('save')
