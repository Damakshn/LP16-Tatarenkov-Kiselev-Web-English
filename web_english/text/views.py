import re

from flask import render_template, url_for, redirect
from pydub import AudioSegment

from config import Config
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
        filename = re.sub(r'\s', r'_', form.title_text.data.lower())
        filename = re.sub(r'\W', r'', filename)
        filename = f'{filename[:15]}.mp3'  # 15 первых символов, чтобы не было больших имен
        audios.save(form.audio.data, name=filename)
        duration = duration_audio(f'{Config.UPLOADED_AUDIOS_DEST}/{filename}')
        text = Content(
            title=form.title_text.data,
            text_en=form.text_en.data,
            text_ru=form.text_ru.data,
            duration=duration
        )
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('text.create'))
    return redirect(url_for('text.create'))


def duration_audio(filename):
    audio = AudioSegment.from_file_using_temporary_files(filename)
    duration_audio = len(audio)
    return duration_audio
