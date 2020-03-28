import os
from pydub import AudioSegment
from config import BASE_DIR
import math

"""
Для работы с аудио используется библиотека PyDub
https://github.com/jiaaro/pydub
Для работы требует ffmpeg.
"""

FILE_NAME = "audio.mp3"
FILE_NAME_WITHOUT_EXTENSION = FILE_NAME[:FILE_NAME.rfind(".")]


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


def split_audio(file):
    """
    Создаёт каталог, который называется ИМЯ_ФАЙЛА_dir, делит
    файл на кусочки длиной по 1 сек и пишет их туда.
    Кусочки называются ИМЯ_ФАЙЛА_N.mp3
    Процедура занимает много времени, есть ли вариант как-то
    ускорить процесс, например, через многопоточность?
    """
    audio = file[:30*1000]
    dir_name = os.path.join(BASE_DIR, f"{FILE_NAME_WITHOUT_EXTENSION}_dir")
    try:
        os.mkdir(dir_name)
        # ceil для того чтобы хвост файла длиной меньше секунды
        # получил свой отдельный файл
        total_chunks = math.ceil(len(audio) / 1000)
        rest_of_audio = audio
        for i in range(total_chunks):
            mark = min(len(rest_of_audio), 1000)
            new_chunk = rest_of_audio[:mark]
            rest_of_audio = rest_of_audio[mark:]
            new_file_name = os.path.join(dir_name, f"{FILE_NAME_WITHOUT_EXTENSION}_{i}.mp3")
            new_chunk.export(new_file_name, format="mp3")
        print("Done!")
    except Exception as e:
        print(e)

sound = AudioSegment.from_file(FILE_NAME, format="mp3")
print(get_audio_duration_in_seconds(sound))
print(get_audio_duration_for_humans(audio=sound))
split_audio(sound)
