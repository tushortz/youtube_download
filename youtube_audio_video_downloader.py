import requests
import re
from urllib import parse
import json
import html
import time
import click
import ast
import sys


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
    source = source.replace("\\u0026", "&").replace("\\", "")
    source = parse.unquote_plus(source)

    title = re.search(r'"title":"(.*?)"',
                      source).group(1).replace("\\", "").replace("?", "-")
    results = re.findall(r'"url":"(.*?)","mimeType":"(.*?); ', source)

    for i in results:
        file_url, mime = i

        if mime.lower().startswith(media_type) and file_url:

            if mime.endswith("mp4"):
                break

    filename = "%s.%s" % (title, file_ext)
    filename = filename.replace("/", "-")
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
    args = sys.argv
    MEDIA_TYPE = "audio"

    if len(args) == 2:
        VIDEO_URLS = list(filter(lambda x: x.startswith("http"), args[1].split(" ")))
    
    elif len(args) > 2:
        MEDIA_TYPE = args[1]
        VIDEO_URLS = list(filter(lambda x: x.startswith("http"), args))
    else:
        sys.exit("""
HOW TO USE
==========

python youtube_audio_video_downloader.py "<links in quotes separated by spaces>"

or

python youtube_audio_video_downloader.py <media type> <links separated by spaces>

-----------------------------------------------------------
media type can be "audio" or "video". Default is audio

""")
    # ---------------DO NOT EDIT ----------------------------
    for VIDEO_URL in VIDEO_URLS:
        get_youtube_file(VIDEO_URL, MEDIA_TYPE)
    # --------------------------------------------------------
