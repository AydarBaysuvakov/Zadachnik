from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, Label
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    code = TextAreaField('Отправить решение', validators=[DataRequired()])
    message = Label('code', '')
    submit = SubmitField('Принять')