from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    name = StringField('Название работы', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])