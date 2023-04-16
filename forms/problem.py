from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ProblemForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Задача', validators=[DataRequired()])
    input_description = TextAreaField('Входные данные', validators=[DataRequired()])
    output_description = TextAreaField('Выходные данные', validators=[DataRequired()])
    dificult = IntegerField('', validators=[DataRequired()])
    example_input = TextAreaField('Пример входных данных', validators=[DataRequired()])
    example_output = TextAreaField('Пример выходных данных', validators=[DataRequired()])
    test_input = TextAreaField('Тестовые данные', validators=[DataRequired()])
    test_output = TextAreaField('Ответ', validators=[DataRequired()])
    submit = SubmitField('Применить')