from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, Label, FileField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    code = TextAreaField('Отправить решение', validators=[])
    file = FileField('Отправить файл', validators=[])
    message = Label('code', '')
    submit = SubmitField('Принять')