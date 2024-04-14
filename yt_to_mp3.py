from youtubesearchpython import VideosSearch

import threading
import json

import yt_helpers as yth
import pyside_gui as psg


def search_queries(query, features, limit):
    # search for videos matching the query
    videos_search = VideosSearch(query, limit=limit)
    dlp_result = videos_search.result()
    videos = dlp_result['result']

    # extract important features
    video_features = [yth.prune_dict(vid, features) for vid in videos]
    
    return dlp_result, video_features



def download_and_convert_videos(video_URLs, dl_filepath, audio_format):
    def download_and_convert_video(video_URL, dl_filepath, audio_format):
        dl_file = yth.download_video(video_URL, dl_filepath)
        yth.convert_video(dl_file, audio_format)

    threads = []
    for video_URL in video_URLs:
        thread = threading.Thread(target=download_and_convert_video, args=(video_URL, dl_filepath, audio_format))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def terminal_deploy():
    # limit = input("Enter the number of videos to query: ")
    limit = 8
    query = "travis scott type beat"
    features = ['title', 'publishedTime', 'duration', 'channel.name', 'channel.id']
    
    dlp_result, video_features = yth.search_queries(query, features, int(limit))

    # print(json.dumps(video_features, indent=4))
    choices_str = input('Which videos look the best to you? Enter the index(es) as CSV: ')

    choices = [i for i in range(int(limit))] if choices_str == "all" else [int(c) for c in choices_str.split(',')]
    video_URLs = [dlp_result['result'][choice]['link'] for choice in choices]

    yth.download_and_convert_videos(video_URLs, 'Travis/', 'mp3')



if __name__ == "__main__":
    # terminal_deploy()
    psg.pyside6_gui_deploy()

