from wtforms import TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
from web_english.generics.forms import GenericForm


class TextForm(GenericForm):
    title_text = TextAreaField('Title', validators=[DataRequired()])
    text_en = TextAreaField('Text EN', validators=[DataRequired()])
    text_ru = TextAreaField('Text RU', validators=[DataRequired()])
    audio = FileField('Audio')
    submit = SubmitField('Save')
