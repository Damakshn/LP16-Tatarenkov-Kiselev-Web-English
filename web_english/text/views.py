from flask import render_template, url_for, redirect, flash
from pydub import AudioSegment

from web_english.text.maping_text import run, create_filename
from web_english import db
from web_english.text.forms import TextForm
from web_english.models import Content
from web_english import audios


def create():
    form = TextForm()
    return render_template(
        'text/create_text.html',
        title='Создание текста',
        form=form,
        form_action=url_for('text.process_create'),
        enctype="multipart/form-data"
    )


def process_create():
    form = TextForm()
    if form.validate_on_submit():
        filename = create_filename(form.title_text.data)
        audios.save(form.audio.data, name=filename)
        audio = AudioSegment.from_file_using_temporary_files(filename)
        duration = len(audio)
        text = Content(
            title=form.title_text.data,
            text_en=form.text_en.data,
            text_ru=form.text_ru.data,
            duration=duration
        )
        db.session.add(text)
        db.session.commit()
        run.delay(form.title_text.data)
        flash('Ваш текст сохранен! Обработка текста может занять некоторое время.')
        return redirect(url_for('text.create'))
    return redirect(url_for('text.create'))
