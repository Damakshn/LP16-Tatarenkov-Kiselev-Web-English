from pydub import AudioSegment


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


print(chunk_audiofile('theres_a_man.mp3', '123'))
