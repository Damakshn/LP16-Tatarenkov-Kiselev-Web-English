from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class TextForm(FlaskForm):
    title_text = TextAreaField('Title', validators=[DataRequired()])
    text_en = TextAreaField('Text EN', validators=[DataRequired()])
    text_ru = TextAreaField('Text RU', validators=[DataRequired()])
    audio = FileField('Audio')
    submit = SubmitField('Save')
