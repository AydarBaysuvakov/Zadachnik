from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ProblemForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired()])
    description = TextAreaField('Условие задачи', validators=[DataRequired()])
    input_description = TextAreaField('Входные данные', validators=[DataRequired()])
    output_description = TextAreaField('Выходные данные', validators=[DataRequired()])
    difficult = IntegerField('Сложность', validators=[DataRequired()])
    time_needed = IntegerField('Необходимое время(в секундах)', validators=[DataRequired()])
    memory_needed = IntegerField('Необходимая память(в МБ)', validators=[DataRequired()])
    example_count = IntegerField('Колличество примеров', validators=[DataRequired()])
    test_count = IntegerField('Колличество тестов', validators=[DataRequired()])
    submit = SubmitField('Принять')