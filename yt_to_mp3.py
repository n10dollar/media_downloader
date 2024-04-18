from youtubesearchpython import VideosSearch
from soundcloud import SoundCloud

import threading
import json

import yt_helpers as yth
import pyside_gui as psg



def search_soundcloud(query, features, limit):
    # search for videos matching the query
    soundcloud = SoundCloud()
    search_res = soundcloud.search_tracks(query)
    songs = [next(search_res) for _ in range(limit)]
    
    # extract important features
    song_features = [{feat: getattr(song, feat) for feat in features if hasattr(song, feat)} for song in songs]
    return songs, song_features



def search_youtube(query, features, limit):
    # search for videos matching the query
    videos_search = VideosSearch(query, limit=limit)
    search_res = videos_search.result()
    videos = search_res['result']

    # extract important features
    video_features = [yth.prune_dict(vid, features) for vid in videos]
    return search_res, video_features



def download_and_convert_videos(video_URLs, dl_filepath, audio_format):
    conv_files = []
    def download_and_convert_video(video_URL, dl_filepath, audio_format):
        dl_file = yth.download_video(video_URL, dl_filepath)
        conv_file = yth.convert_video(dl_file, audio_format)
        conv_files.append(conv_file)

    threads = []
    for video_URL in video_URLs:
        thread = threading.Thread(target=download_and_convert_video, args=(video_URL, dl_filepath, audio_format))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return conv_files



def terminal_deploy():
    # limit = input("Enter the number of videos to query: ")
    limit = 8
    query = "travis scott type beat"
    features = ['title', 'publishedTime', 'duration', 'channel.name', 'channel.id']
    
    search_res, video_features = yth.search_youtube(query, features, int(limit))

    # print(json.dumps(video_features, indent=4))
    choices_str = input('Which videos look the best to you? Enter the index(es) as CSV: ')

    choices = [i for i in range(int(limit))] if choices_str == "all" else [int(c) for c in choices_str.split(',')]
    video_URLs = [search_res['result'][choice]['link'] for choice in choices]

    yth.download_and_convert_videos(video_URLs, 'Travis/', 'mp3')



if __name__ == "__main__":
    # terminal_deploy()
    psg.pyside6_gui_deploy()
    # query = "the parrot has no head"
    # features = ['title', 'sharing']
    # songs, song_features = search_soundcloud(query, features, 3)
    # download_and_convert_videos([songs[0].permalink_url], 'weeknd_songs/', 'mp3')
    # print(song_features)
