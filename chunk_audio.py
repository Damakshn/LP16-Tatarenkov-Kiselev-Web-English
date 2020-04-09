from pydub import AudioSegment

audio = AudioSegment.from_mp3('the_stonecutter.mp3')
n = len(audio)
counter = 1
interval = 3000
start = 0
end = 0
flag = 0
list_chunks = []

for i in range(0, n, interval):
    if i == 0:
        start = 0
        end = interval
    else:
        start = end
        end = start + interval
    if end >= n:
        end = n
        flag = 1
    chunk = audio[start:end]
    filename = 'chunks/chunk'+str(counter)+'.ogg'
    list_chunks.append(filename)
    chunk.export(filename, format='ogg')
    print("Processing chunk "+str(counter)+". Start = "+str(start)+" end = "+str(end))
    counter = counter + 1
print(list_chunks)