import re

from flask import render_template, jsonify, send_from_directory

from config import Config
from web_english.models import Content, Chunk
from web_english.text.maping_text import create_name


def index():
    return render_template("main/index.html")


def learning(text_id):
    text = Content.query.filter(Content.id == text_id).first()
    return render_template("main/learning.html", text=text)


def send_chunks(text_id):
    text = Content.query.filter(Content.id == text_id).first()
    chunks = Chunk.query.filter(Chunk.content_id == text_id).all()
    split_text = text.text_en.split()
    word_number_start = 0
    word_number_end = 0
    chunks_for_sending = []
    for chunk in chunks:
        word_number_start = word_number_end
        word_number_end = chunk.word_number + 1
        split_chunk = split_text[word_number_start:word_number_end]
        join_chunk = " ".join(split_chunk)
        chunks_for_sending.append(join_chunk)
    sentences_en = re.split(r"(?<=\w[.!?;]) ", text.text_en)
    sentences_ru = re.split(r"(?<=\w[.!?;]) ", text.text_ru)
    sending = {
        "chunks_for_sending": chunks_for_sending,
        "sentences_en": sentences_en,
        "sentences_ru": sentences_ru,
    }
    return jsonify(sending)


def serve_audio(text_id):
    text = Content.query.get(text_id)
    filename = f"{create_name(text.title_text)}.mp3"
    return send_from_directory(Config.UPLOADED_AUDIOS_DEST, filename)
