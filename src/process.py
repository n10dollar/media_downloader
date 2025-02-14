from youtubesearchpython import VideosSearch
from soundcloud import SoundCloud
from yt_dlp import YoutubeDL

import threading as thr
import ffmpeg
import os

import utils


def search(engine, query, limit):
    def search_youtube(query, limit):
        # search for videos matching the query
        videos_search = VideosSearch(query, limit=limit)
        search_res = videos_search.result()
        videos = search_res['result']
        return videos

    def search_soundcloud(query, limit):
        # search for songs matching the query
        soundcloud = SoundCloud()
        search_res = soundcloud.search_tracks(query)
        songs = [next(search_res) for _ in range(limit)]
        return songs

    mappings = {
        "yt": search_youtube,
        "sc": search_soundcloud
    }

    media = mappings[engine](query, limit)
    return media


def get_features(engine, media, features):
    mappings = {
        "yt": lambda medium, features: utils.prune_dict(medium, features),
        "sc": lambda medium, features: {feat: getattr(medium, feat) for feat in features if hasattr(medium, feat)}
    }

    features = [mappings[engine](medium, features) for medium in media]
    return features


def download(url, ydl_opts):
    ydl = YoutubeDL(ydl_opts)
    video_info = ydl.extract_info(url, download=False)
    dl_file = ydl.prepare_filename(video_info)

    ydl.download([url])
    return dl_file


def convert(dl_file, audio_format):
    # process output file name
    segments = dl_file.split('.')
    name, ext = '.'.join(segments[:-1]), segments[-1]
    conv_file = f'{name}.{audio_format}'

    if not os.path.exists(conv_file):
        # convert file to audio_format
        stream = ffmpeg.input(dl_file)
        stream = ffmpeg.output(stream, conv_file, format=audio_format)
        ffmpeg.run(stream)

        # remove original file
        os.remove(dl_file)

    return conv_file


def download_and_convert_multithread(video_urls, ydl_opts, audio_format):
    def download_and_convert(video_url, ydl_opts, audio_format):
        dl_file = download(video_url, ydl_opts)
        conv_file = convert(dl_file, audio_format)
        return conv_file

    # threading doesn't use return value
    def dc_wrapper(video_url, ydl_opts, audio_format, conv_files):
        conv_files.append(download_and_convert(video_url, ydl_opts, audio_format))

    threads = []
    conv_files = []
    for video_URL in video_urls:
        thread = thr.Thread(target=dc_wrapper, args=(video_URL, ydl_opts, audio_format, conv_files))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return conv_files
