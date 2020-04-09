import json
import re
import urllib.request

from pydub import AudioSegment

from config import Config


def chunk_audiofile(audiofile, title):
    audio = AudioSegment.from_mp3(audiofile)
    length_audio = len(audio)
    counter = 1
    interval = 3000
    start = 0
    end = 0
    list_chunks = []
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
        filename = f'chunks/{title}chunk{str(counter)}.ogg'
        list_chunks.append(filename)
        chunk.export(filename, format='ogg')
        print(f"Processing {title}chunk{str(counter)}. Start = {str(start)} End = {str(end)}")
        counter = counter + 1
    return list_chunks


def send_ya_speech_kit(*args):
    list_chunks_result = []
    for chunk in args:
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
                list_chunks_result.append(decodedData.get("result"))
    return list_chunks_result


# На вход принемаем оригинальный текст и список распознанных отрывков
def maping_text(text, *args):
    # Убираем из текста все знаки препинания и разбиваем по словам
    split_text = re.sub("[.,!?;:]", "", text).lower().split()

    # Та самая секунда, на которой находится диктор
    second = 0

    # Номер слова и само слово в тексте, на котором находится диктор
    last_word = [0, None, second]
    list_last_word = [last_word]

    for recognized in args:
        # Каждый отрывок - это 3 секунды чтения диктора
        second += 3

        # Отрезок оригинального текста, который будет сравниваться с
        # определенным распознанным отрывком
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
        list_last_word.append(last_word)
    return list_last_word


def duplicate_word(cut_split_text, medium_word, number_duplicate):
    start_at = -1
    duplicates = []
    while True:
        try:
            duplicate = cut_split_text.index(medium_word, start_at + 1)
        except ValueError:
            break
        else:
            duplicates.append(duplicate)
            start_at = duplicate
    result = duplicates[number_duplicate]
    return result
