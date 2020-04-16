import json
import re
import requests

from pydub import AudioSegment

from config import Config
from web_english import db, celery
from web_english.models import Chunk, Content


class Recognizer():

    def __init__(self, title):
        self.title = title

    def chunk_audiofile(self, title):
        audiofile = create_filename(self.title)
        audio = AudioSegment.from_mp3(audiofile)
        length_audio = len(audio)
        counter = 1

        # 3000 - это интервал в 3 секунды распознования текста. К этому числу мы будем
        # привязывать слова в оригинальном тексте.
        interval = 3000
        start = 0
        end = 0
        chunks = []
        for i in range(0, length_audio, interval):
            if i == 0:
                start = 0
                end = interval
            else:
                start = end
                end = start + interval
            if end >= length_audio:
                end = length_audio
            chunk = audio[start:end]
            filename = f'{Config.UPLOADED_AUDIOS_DEST}/chunks/{self.title}chunk{str(counter)}.ogg'
            chunks.append(filename)
            chunk.export(filename, format='ogg')
            print(f"Processing {self.title}chunk{counter}. Start = {start} End = {end}")
            counter += 1
        return chunks

    def send_ya_speech_kit(self, chunks):
        chunks_result = []
        for chunk in chunks:
            # Эта часть кода взята с яндекса и изменена под наш проект. Названия переменных
            # взяты оригинальные (изменены значения).
            with open(chunk, "rb") as f:
                data = f.read()
            params = {
                      'lang': 'en-US',
                      'folderId': Config.FOLDER_ID
            }
            url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
            headers = {"Authorization": f"Api-Key {Config.API_KEY}"}
            response = requests.post(url, params=params, data=data, headers=headers)
            decode_response = response.content.decode('UTF-8')
            chunk = json.loads(decode_response)
            if chunk.get("error_code") is None:
                chunks_result.append(chunk.get("result"))
        return chunks_result

    def maping_text(self, chunks_result, title=None):
        content = Content.query.filter(Content.title_text == self.title).first()

        # Убираем из текста все знаки препинания и разбиваем по словам
        split_text = re.sub("[.,!?;:]", "", content.text_en).lower().split()

        # Та самая секунда, на которой находится диктор
        second = 0

        # Номер слова и само слово в тексте, на котором находится диктор
        last_word = [0, None, second]
        chunks_text = []
        chunks_saved = []

        for recognized in chunks_result:
            # Каждый отрывок - это 3 секунды чтения диктора
            second += 3

            # Отрезок оригинального текста, который будет сравниваться с
            # определенным распознанным отрывком
            # 15  - это примерное кол-во слов, которое диктор может произнести за 3 скунды
            # Можно поставить хоть 500, но тогда будет дольше считать. Но если меньше 15, то
            # split_recognized может оказать больше, а это неправильно
            cut_split_text = split_text[last_word[0]:last_word[0] + 15]

            # Разбиваем распознанный отрывок на слова и приводим к нижнему регистру
            split_recognized = recognized.lower().split()

            # Перебираем каждое слово в оригинальном отрезке
            for word in cut_split_text:

                # Если находим это слово в распознанном, то записываем его как последнее найденное слово
                # и удаляем первое это слово из распознанного отрывка, чтобы больше не встречалось
                if word in split_recognized:
                    medium_word = word
                    split_recognized.remove(word)

            # Кол-во одинаковых "последних" слов в распознанном отрезке. Отнимаем 1, чтобы можно было
            # использовать его в списке повторяющихся слов в оригинальном отрезке
            number_duplicate = recognized.lower().split().count(medium_word) - 1

            # Если это кол-во равно 1 (не забываем, что оняли 1 выше), то прибавляем к
            # индексу найденного последнего слова индекс предыдущего во всем тексте - это
            # будет индекс нашего найденного последнего слова
            if number_duplicate == 0:
                number_word = cut_split_text.index(medium_word) + last_word[0]

            # Иначе ищем индекс последнего слова, которое было по порядку на том месте,
            # сколько встречалось в распознанном тексте
            else:
                number_word_cut_split_text = duplicate_word(cut_split_text, medium_word, number_duplicate)
                number_word = number_word_cut_split_text + last_word[0]
            last_word = [number_word, medium_word, second]
            chunk_saved = [recognized, content.id, last_word[1], last_word[0], last_word[2]]
            chunks_saved.append(chunk_saved)
            chunk_text = ' '.join(cut_split_text)
            chunks_text.append(chunk_text)
        return chunks_text, chunks_saved

    def save_chunks(self, chunks_saved):
        for chunk_saved in chunks_saved:
            save = Chunk(chunks_recognized=chunk_saved[0],
                         id_content=chunk_saved[1],
                         word=chunk_saved[2],
                         word_number=chunk_saved[3],
                         word_time=chunk_saved[4]
                         )
            db.session.add(save)
        db.session.commit()

    def save_edit_chunks(self, chunks_saved, chunks):
        count = 0
        for chunk in chunks:
            chunk.chunks_recognized = chunks_saved[count][0]
            chunk.id_content = chunks_saved[count][1]
            chunk.word = chunks_saved[count][2]
            chunk.word_number = chunks_saved[count][3]
            chunk.word_time = chunks_saved[count][4]
            db.session.add(chunk)
            count += 1
        db.session.commit()


@celery.task
def run(title):
    recognizer = Recognizer(title)
    chunks = recognizer.chunk_audiofile(title)
    chunks_result = recognizer.send_ya_speech_kit(chunks)
    chunks_saved = recognizer.maping_text(chunks_result)
    recognizer.save_chunks(chunks_saved[1])


def duplicate_word(cut_split_text, medium_word, number_duplicate):
    start_at = -1
    duplicates = []
    while True:
        try:
            duplicate = cut_split_text.index(medium_word, start_at + 1)
        except ValueError:
            break
        duplicates.append(duplicate)
        start_at = duplicate
    result = duplicates[number_duplicate]
    return result


def create_filename(title):
    filename_draft = re.sub(r'\s', r'_', title.lower())
    filename_without_mp3 = re.sub(r'\W', r'', filename_draft)
    filename = f'{Config.UPLOADED_AUDIOS_DEST}/{filename_without_mp3}.mp3'
    return filename
