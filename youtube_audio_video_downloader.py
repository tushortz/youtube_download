import requests
import re
from urllib import parse
import json
import html
import time
import click


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

    r = requests.get(file_url, stream=True)
    total_length = int(r.headers.get('content-length'))
    chunks = r.iter_content(chunk_size=1024)

    with click.progressbar(chunks, length=int(total_length/1024) + 1, label="Downloading %s" % filename, show_percent=True, show_pos=True, show_eta=True, width=50, color="green") as bar, open(filename, "wb") as f:
        for chunk in bar:
            f.write(chunk)
            f.flush()

            bar.update(int(len(chunk)/2048))

    end_time = time.perf_counter()
    total_time = int(end_time - start_time)

    print("'%s' download complete in %s seconds" % (filename, total_time))


if __name__ == "__main__":
    # ------------------CAN EDIT --------------------------------------------
    MEDIA_TYPE = "audio"
    VIDEO_URLS = [
        "https://www.youtube.com/watch?v=yYw_JBNO1Kg",
        "https://www.youtube.com/watch?v=brQT6X5xG7k",
        "https://www.youtube.com/watch?v=C-be3I6RulQ",
        "https://www.youtube.com/watch?v=BBqFvQijM1k",
        "https://www.youtube.com/watch?v=OhHyHnAG_I8",
        "https://www.youtube.com/watch?v=FVbEe_a_-rM",
        "https://www.youtube.com/watch?v=4G5BAQhLzMw",
        "https://www.youtube.com/watch?v=OwrE0YjfNGg",
        "https://www.youtube.com/watch?v=8R4bM54Cp7I"
    ]

    # ---------------DO NOT EDIT ----------------------------
    for VIDEO_URL in VIDEO_URLS:
        get_youtube_file(VIDEO_URL, MEDIA_TYPE)
    # --------------------------------------------------------
