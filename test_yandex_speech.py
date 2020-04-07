import json
import os
import urllib.request

FOLDER_ID = os.environ.get("FOLDER_ID_YANDEX")  # Идентификатор каталога
API_KEY = os.environ.get("API_KEY_YANDEX")

with open("1234.ogg", "rb") as f:
    data = f.read()

params = "&".join([
    "topic=general",
    "folderId=%s" % FOLDER_ID,
    "lang=en-US"
])

url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
url.add_header("Authorization", "Api-Key %s" % API_KEY)

responseData = urllib.request.urlopen(url).read().decode('UTF-8')
decodedData = json.loads(responseData)

if decodedData.get("error_code") is None:
    print(decodedData.get("result"))
