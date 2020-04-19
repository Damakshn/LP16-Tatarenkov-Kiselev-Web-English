from flask import render_template, url_for, redirect, flash, request
from pydub import AudioSegment

from web_english import db
from web_english.text.forms import TextForm, EditForm
from web_english.text.maping_text import Recognizer, create_name, recognition_start
from web_english.models import Content, Chunk
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
        filename = create_name(form.title_text.data)[0]
        audios.save(form.audio.data, name=filename)
        audio = AudioSegment.from_file_using_temporary_files(filename)
        duration = len(audio)
        text = Content(
            title_text=form.title_text.data,
            text_en=form.text_en.data,
            text_ru=form.text_ru.data,
            duration=duration
        )
        db.session.add(text)
        db.session.commit()
        #  Используем Celery
        recognition_start.delay(form.title_text.data)
        flash('Ваш текст сохранен! Обработка текста может занять некоторое время.')
        return redirect(url_for('text.texts_list'))
    return redirect(url_for('text.create'))


def texts_list():
    title = 'Список текстов'
    texts = Content.query.all()
    return render_template(
                           'text/texts_list.html',
                           title=title,
                           texts=texts
                           )


def edit_text(text_id):
    form = EditForm()
    text = Content.query.filter(Content.id == text_id).first()
    title_text = text.title_text
    title_page = f'Правка {title_text}'
    chunks = Chunk.query.filter(Chunk.content_id == text.id).all()
    chunks_resault = []
    for chunk in chunks:
        recognized_chunk = chunk.chunks_recognized.lower()
        chunks_resault.append(recognized_chunk)
    recognizer = Recognizer(title_text)
    chunks_text = recognizer.list_chunks_text(text_id, chunks_resault)
    merged_chunks = list(zip(chunks_text, chunks_resault))
    return render_template('text/edit_text.html',
                           title_page=title_page,
                           merged_chunks=merged_chunks,
                           form=form,
                           form_action=url_for('text.process_edit_text', id=text.id))


def process_edit_text():
    text_id = request.args.get('id')
    text = Content.query.filter(Content.id == text_id).first()
    title_text = text.title_text
    chunks = Chunk.query.filter(Chunk.content_id == text.id).all()
    edited_chunks = request.form.to_dict(flat=False)['chunk_recognized']
    form = EditForm()
    recognizer = Recognizer(title_text)
    if form.validate_on_submit():
        recognizer.edit_maping(edited_chunks, chunks)
        flash('Ваши правки сохранены!')
        return redirect(url_for('text.texts_list'))
