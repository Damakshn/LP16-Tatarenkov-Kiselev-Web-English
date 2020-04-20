from flask import current_app, redirect, render_template, request, send_from_directory, url_for
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
        text = Content(
            title=form.title_text.data,
            text_en=form.text_en.data,
            text_ru=form.text_ru.data
        )
        db.session.add(text)
        db.session.commit()
        # зная id нового текста, генерируем имя файла и сохраняем его
        filename = f"{text.id}_{request.files['audio'].filename}"
        text.filename = filename
        db.session.commit()
        audios.save(form.audio.data, name=filename)
        return redirect(url_for('text.create'))
    return redirect(url_for('text.create'))

def listen(text_id):
    # ToDo content not found error
    text = Content.query.get(text_id)
    files_dir = current_app.config['UPLOADED_AUDIOS_DEST']
    return render_template(
        'text/listening_page.html',
        title=text.title,
        content=text
    )

def serve_audio(text_id):
    text = Content.query.get(text_id)
    files_dir = current_app.config['UPLOADED_AUDIOS_DEST']
    # ToDo audio does not exist error
    return send_from_directory(files_dir, text.filename)
