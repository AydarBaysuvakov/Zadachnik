from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ProblemForm(FlaskForm):
    example_input = TextAreaField('Пример входных данных', validators=[DataRequired()])
    example_output = TextAreaField('Пример выходных данных', validators=[DataRequired()])
    test_input = TextAreaField('Тестовые данные', validators=[DataRequired()])
    test_output = TextAreaField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Применить')