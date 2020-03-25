from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from web_english.generics.forms import GenericForm

class TextForm(GenericForm):
    title_text = TextAreaField('Title', validators=[DataRequired()])
    text_eu = TextAreaField('Text EU', validators=[DataRequired()])
    text_ru = TextAreaField('Text RU', validators=[DataRequired()])
    submit = SubmitField('Save')
