# Youtube Downloader

Simple Youtube Video and Audio downloader script written in Python

## HOW TO USE

> You may need to install the required modules first by running in the terminal/console

```bash
$ pip install click requests
```

You can then run the program from the terminal by using the command below:

```bash
$ python youtube_download.py [urls in quotes separated by spaces]
```

For example:

```bash
$ python youtube_download.py "https://www.youtube.com/watch?v=QImrM_rbF6o https://www.youtube.com/watch?v=fiyYoe678yI"
```
Alternatively to specify `media download type, use:

```bash
$ python youtube_download.py [MEDIA_TYPE] [urls in quotes separated by spaces]
```
break a change
For example:

```bash
$ pytthe media type as in the second example, you don't need to enclose the video urls in quotes.

> Valid `MEDIA_TYPES` are `audio` and `video`

break a change