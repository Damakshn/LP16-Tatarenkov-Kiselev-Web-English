from io import BytesIO
import math
import os
from pydub import AudioSegment
import speech_recognition as sr
from config import BASE_DIR


"""
Для работы с аудио используется библиотека PyDub
https://github.com/jiaaro/pydub
Для работы требует ffmpeg.

Для распознавания используется пакет SpeechRecognition
https://pypi.org/project/SpeechRecognition/
SpeechRecognition требует PocketSphinx
https://pypi.org/project/pocketsphinx/
А он, в свою очередь, хочет Swig
http://www.swig.org/
"""

SECOND = 1000
FILE_NAME = "audio_full.mp3"

recognizer = sr.Recognizer()

def get_audio_duration_in_seconds(audio):
    total = len(audio)
    return total // 1000

def get_audio_duration_for_humans(duration_in_seconds=None, audio=None):
    if audio is not None:
        duration_in_seconds = get_audio_duration_in_seconds(audio)
    elif duration_in_seconds is None:
        raise ValueError("You should pass duration_in_seconds or AudioSegment.")
    minutes = str(duration_in_seconds // 60).zfill(2)
    seconds = str(duration_in_seconds % 60).zfill(2)
    return f"{minutes}:{seconds}"

def from_mp3_to_wav(audiosegment_in_mp3):
    # конвертация в wav необходима, т.к. SpeechRecognition
    # не воспринимает mp3
    with BytesIO() as stream:
        audiosegment_in_mp3.export(stream, format="wav")
        stream.seek(0)
        wav_segment = AudioSegment.from_file(stream, format="wav")
    return wav_segment

def recognize_chunk(audio_chunk):
    # сначала приводим аудиофрагмент к виду, пригодному для распознавания
    with BytesIO() as stream:
        audio_chunk.export(stream, format="wav")
        stream.seek(0)
        with sr.AudioFile(stream) as sr_audiofile:
            data = recognizer.record(sr_audiofile)
    try:
        result = recognizer.recognize_sphinx(data)
    except sr.UnknownValueError:
        result = ""
    return result

def get_audiomap(audiosegment_in_wav):
    audiomap = []
    # ceil для того чтобы хвост файла длиной меньше секунды
    # получил свой отдельный файл
    total_chunks = math.ceil(len(audiosegment_in_wav) / SECOND)
    rest_of_audio = audiosegment_in_wav
    for i in range(total_chunks):
        # если оставшаяся длина файла меньше секунды, берём всё
        # иначе отрезаем 1 секунду
        mark = min(SECOND, len(rest_of_audio))
        new_chunk = rest_of_audio[:mark]
        rest_of_audio = rest_of_audio[mark:]
        recognized_words = recognize_chunk(new_chunk)
        audiomap.append(recognized_words)
    return audiomap

if __name__ == "__main__":
    mp3 = AudioSegment.from_file(FILE_NAME, format="mp3")
    wav = from_mp3_to_wav(mp3)
    first_ten_sec = wav[:10*SECOND]
    print(get_audiomap(first_ten_sec))
