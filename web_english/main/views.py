from flask import render_template

from web_english.models import Content


def index():
    return render_template("main/index.html")


def learning(text_id):
    text = Content.query.filter(Content.id == text_id).first()
    title = text.title_text
    text_en = text.text_en
    text_ru = text.text_ru
    sentence_en = text_en.split('.')[0]
    sentence_ru = text_ru.split('.')[0]
    return render_template(
                           'main/learning.html',
                           title=title,
                           text_en=text_en,
                           sentence_en=sentence_en,
                           sentence_ru=sentence_ru
                           )
