from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ExampleForm(FlaskForm):
    example_input = TextAreaField('Пример входных данных', validators=[DataRequired()])
    example_output = TextAreaField('Пример выходных данных', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class TestForm(FlaskForm):
    test_input = TextAreaField('Тестовые данные', validators=[DataRequired()])
    test_output = TextAreaField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
