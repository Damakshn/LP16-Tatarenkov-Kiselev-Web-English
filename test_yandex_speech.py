import json
import urllib.request
from config import Config


list_chunks = ['chunks/chunk1.ogg', 'chunks/chunk2.ogg', 'chunks/chunk3.ogg', 'chunks/chunk4.ogg', 'chunks/chunk5.ogg', 'chunks/chunk6.ogg', 'chunks/chunk7.ogg', 'chunks/chunk8.ogg', 'chunks/chunk9.ogg', 'chunks/chunk10.ogg', 'chunks/chunk11.ogg', 'chunks/chunk12.ogg', 'chunks/chunk13.ogg', 'chunks/chunk14.ogg', 'chunks/chunk15.ogg', 'chunks/chunk16.ogg', 'chunks/chunk17.ogg', 'chunks/chunk18.ogg', 'chunks/chunk19.ogg', 'chunks/chunk20.ogg', 'chunks/chunk21.ogg', 'chunks/chunk22.ogg', 'chunks/chunk23.ogg', 'chunks/chunk24.ogg', 'chunks/chunk25.ogg', 'chunks/chunk26.ogg', 'chunks/chunk27.ogg', 'chunks/chunk28.ogg', 'chunks/chunk29.ogg', 'chunks/chunk30.ogg', 'chunks/chunk31.ogg', 'chunks/chunk32.ogg', 'chunks/chunk33.ogg', 'chunks/chunk34.ogg', 'chunks/chunk35.ogg', 'chunks/chunk36.ogg', 'chunks/chunk37.ogg', 'chunks/chunk38.ogg', 'chunks/chunk39.ogg', 'chunks/chunk40.ogg', 'chunks/chunk41.ogg', 'chunks/chunk42.ogg', 'chunks/chunk43.ogg', 'chunks/chunk44.ogg', 'chunks/chunk45.ogg', 'chunks/chunk46.ogg', 'chunks/chunk47.ogg', 'chunks/chunk48.ogg', 'chunks/chunk49.ogg', 'chunks/chunk50.ogg', 'chunks/chunk51.ogg', 'chunks/chunk52.ogg', 'chunks/chunk53.ogg', 'chunks/chunk54.ogg', 'chunks/chunk55.ogg', 'chunks/chunk56.ogg', 'chunks/chunk57.ogg']


def send_ya_speech_kit(*args):
    list_chunks_result = []
    for chunk in list_chunks:
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


print(send_ya_speech_kit(list_chunks))
