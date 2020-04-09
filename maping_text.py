import re

text = '''The stonecutter
Once upon a time there was a stone cutter. The stone cutter lived in a land where a life of privilege meant being powerful. Looking at his life he decided that he was unsatisfied with the way things were and so he set out to become the most powerful thing in the land.
Looking around his land he wondered to himself what is it to be powerful. Looking up he saw the Sun shining down on all the land. «The Sun must be the most powerful thing that there is, for it shines down on all things, and all things grow from it’s touch.» So he became the Sun.
Days later, as he shone his power down on the inhabitants of the land, there came a cloud which passed beneath him obstructing his brilliance. Frustrated he realized that the Sun was not the most powerful thing in the land, if a simple cloud could interrupt his greatness. So he became a cloud, in fact, he became the most powerful storm that the world had ever seen.
And so he blew his rain and lightning, and resounded with thunder all over the land, demonstrating that he was the most powerful. Until one day he came across a boulder.
Down and down he poured and his thunder roared, lightning flashed and filled the sky, striking the ground near the boulder. His winds blew and blew and blew, and yet, despite all his efforts, he could not budge the boulder.
Frustrated again, he realized that the storm was not the most powerful thing in the land, rather it must be the boulder. So he became the boulder.
For days he sat, unmovable, and impassive, demonstrating his power, until one day, a stone cutter came and chiseled him to bits.
The moral of the story is: sometimes the most important thing to remember is that you have everything you need already, right inside of you. Power is an illusion.'''

recognized_text = ['The stonecutter once', 'Upon a time there was a stonecutter', 'The stonecutter lived in the land where life of PI', 'Management being powerful', 'What is lifey decided that he was unsatisfied', 'The way things were and so he said', 'How to become the most powerful thing in the', '', 'And he wants to himself what is the', 'To be powerful looking up', 'Heeso the sun shining down all the land', 'This must be the most', 'Cool thing that there is white shines down', '100 things and allthingsd grow from', 'Watch sur became the', 'Sun', 'John his power down on the inhabitants of the land', 'Make a macleod which cost beneath', 'And obstructing his brilliance', 'Straightened he realise that the sun', 'Is not the most powerful thing in the land', 'If a simple cloudcode interrupt his great', 'Miss you become a class', 'In fact he became the most', 'Powerful stoon that the world ever seen', 'Blue history', 'Train and lightning founded with sound', 'Over the land demonstrating that', 'Who was the most powerful', 'Until sunday came across a boat', 'Down heath', 'Wood and his thunder roullet lightning', 'Aston villa sky striking', 'Ground near the builder', 'Who and when to do i get to spy', 'All his athetes he could not', 'What budge the boulder', 'Castrated again he realise that the store', 'When was not the most powerful thing in the', 'Land rover it must be', 'Boda Ebay', 'The bull dot', 'Seasat unmovable and in', 'Massive demonstrating his power', 'Until 1 day a stonecutter',
'Name and chisel tend to bits', 'The story is', 'Sometimes the most important thing to remember', 'Is that you have everything you need', 'Eddie wright insideview']


# На вход принемаем оригинальный текст и список распознанных отрывков
def maping_text(text, *args):
    # Убираем из текста все знаки препинания и разбиваем по словам
    split_text = re.sub("[.,!?;:]", "", text).lower().split()

    # Та самая секунда, на которой находится диктор
    second = 0

    # Номер слова и само слово в тексте, на котором находится диктор
    last_word = [0, None, second]
    list_last_word = [last_word]

    for recognized in recognized_text:
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
    print(list_last_word)


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


maping_text(text, recognized_text)
