from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AuthorForm(FlaskForm):
    key = StringField('Ключ', validators=[DataRequired()])
    submit = SubmitField('Применить')