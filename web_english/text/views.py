from flask import render_template, url_for, redirect
from pydub import AudioSegment

from web_english.text.maping_text import Recognizer, create_filename
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
        duration = duration_audio(filename)
        text = Content(
            title=form.title_text.data,
            text_en=form.text_en.data,
            text_ru=form.text_ru.data,
            duration=duration
        )
        db.session.add(text)
        db.session.commit()
        # recognizer = Recognizer(filename, text)
        # Recognizer.run.delay(filename, form.title_text.data)
        recognizer = Recognizer(form.title_text.data)
        # recognizer.delay()
        recognizer.delay(form.title_text.data)
        return redirect(url_for('text.create'))
    return redirect(url_for('text.create'))


def duration_audio(filename):
    audio = AudioSegment.from_file_using_temporary_files(filename)
    duration_audio = len(audio)
    return duration_audio
