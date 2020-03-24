from flask import render_template, url_for, redirect
from web_english.text import bp
from web_english import db
from web_english.text.forms import TextForm
from web_english.models import Content


@bp.route('/create')
def create():
    form = TextForm()
    return render_template(
        'text/create_text.html',
        title='Создание текста',
        form=form,
        form_action=url_for('text.process_create')
    )

@bp.route('/process_create', methods=['POST'])
def process_create():
    form = TextForm()

    if form.validate_on_submit():
        text = Content(
            title=form.title_text.data,
            text_eu=form.text_eu.data,
            text_ru=form.text_ru.data
        )
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('text.create'))
    return redirect(url_for('text.create'))