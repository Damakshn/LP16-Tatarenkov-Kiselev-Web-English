from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TextForm(FlaskForm):
    title_text = TextAreaField('Title', validators=[DataRequired()])
    text_eu = TextAreaField('Text EU', validators=[DataRequired()])
    text_ru = TextAreaField('Text RU', validators=[DataRequired()])
    submit = SubmitField('Save')
