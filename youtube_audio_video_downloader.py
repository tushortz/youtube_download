import requests
import re
from urllib import parse
import json
import html
import time


def get_youtube_file(url, media_type="audio"):
    '''
    :url: path to youtube file
    :media_type: audio or video

    returns first match which is usually the best available
    '''

    start_time = time.perf_counter()

    media_type = media_type.lower()

    if media_type == "audio":
        file_ext = "mp3"
    elif media_type == "video":
        file_ext = "mp4"
    else:
        quit("Error: Invalid media type detected")

    source = requests.get(url).text
    source = source.replace("\\", "").replace("u0026", "&")
    source = parse.unquote_plus(source)

    title = re.search(r'"title":"(.*?)"',
                      source).group(1).replace("\\", "").replace("?", "-")
    results = re.findall(r'"url":"(.*?)","mimeType":"(.*?);', source)

    results = [{"url": i[0], "type": i[1]} for i in results]

    file_url = ""
    for i in results:
        if i.get("type").lower().startswith(media_type) and i.get("url"):
            file_url = i.get("url")

            if i.get("type").endswith("mp4"):
                break

    filename = "%s.%s" % (title, file_ext)
    with open(filename, "wb") as f:
        content = requests.get(file_url).content
        f.write(content)

    end_time = time.perf_counter()
    total_time = end_time - start_time

    print("DOWNLOADING '%s' COMPLETE IN %s" % (filename, total_time))


if __name__ == "__main__":
    # ------------------CAN EDIT --------------------------------------------
    VIDEO_URL = "https://www.youtube.com/watch?v=87GgSO5B5Hc&feature=youtu.be"
    MEDIA_TYPE = "audio"
    # -----------------------------------------------------------------------

    # ---------------DO NOT EDIT ----------------------------
    get_youtube_file(VIDEO_URL, MEDIA_TYPE)
    # --------------------------------------------------------
