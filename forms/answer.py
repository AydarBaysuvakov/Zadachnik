from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    code = TextAreaField('Отправить решение', validators=[DataRequired()])
    submit = SubmitField('Принять')