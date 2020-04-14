import json
import re
import urllib.request

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
            filename = f'web_english/text/uploads/audio/chunks/{self.title}chunk{str(counter)}.ogg'
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

            params = "&".join([
                "topic=general",
                "folderId=%s" % Config.FOLDER_ID,
                "lang=en-US"
            ])

            url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params,
                                         data=data)
            url.add_header("Authorization", "Api-Key %s" % Config.API_KEY)

            responseData = urllib.request.urlopen(url).read().decode('UTF-8')
            decodedData = json.loads(responseData)

            if decodedData.get("error_code") is None:
                chunks_result.append(decodedData.get("result"))
        return chunks_result

    def maping_text(self, chunks_result):
        content = Content.query.filter(Content.title == self.title).first()
        # Убираем из текста все знаки препинания и разбиваем по словам
        split_text = re.sub("[.,!?;:]", "", content.text_en).lower().split()

        # Та самая секунда, на которой находится диктор
        second = 0

        # Номер слова и само слово в тексте, на котором находится диктор
        last_word = [0, None, second]
        last_words = [last_word]

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
            # Запись в базу данных
            words_saved = Chunk(chunks_recognized=recognized,
                                id_content=content.id,
                                word=last_word[1],
                                word_number=last_word[0],
                                word_time=last_word[2]
                                )
            db.session.add(words_saved)
            db.session.commit()
            last_words.append(last_word)
        return last_words


@celery.task
def run(title):
    recognizer = Recognizer(title)
    chunks = recognizer.chunk_audiofile(title)
    chunks_result = recognizer.send_ya_speech_kit(chunks)
    last_words = recognizer.maping_text(chunks_result)
    return last_words


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
