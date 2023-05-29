from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange


class RequestForm(FlaskForm):
    number_of_questions = IntegerField(label=10, default=1, validators=[NumberRange(min=1, max=10)])
