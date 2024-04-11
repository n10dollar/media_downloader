from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

import ffmpeg
import threading
import json
import os


def search_queries(query, features, limit):
    # search for videos matching the query
    videos_search = VideosSearch(query, limit=limit)
    dlp_result = videos_search.result()
    videos = dlp_result['result']

    # extract important features
    video_features = [prune_dict(vid, features) for vid in videos]
    
    return (dlp_result, video_features)



def download_and_convert_videos(video_URLs, dl_filepath, audio_format):
    def download_and_convert_video(video_URL, dl_filepath, audio_format):
        dl_file = download_video(video_URL, dl_filepath)
        convert_video(dl_file, audio_format)

    threads = []
    for video_URL in video_URLs:
        thread = threading.Thread(target=download_and_convert_video, args=(video_URL, dl_filepath, audio_format))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

       

def download_video(video_URL, dl_filepath):
    # configure parameters
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{dl_filepath}%(title)s.%(ext)s'
    }
    ydl = YoutubeDL(ydl_opts)

    # video data
    video_info = ydl.extract_info(video_URL, download=False)

    # downloaded file name
    dl_file = ydl.prepare_filename(video_info)

    # download file
    ydl.download([video_URL])
    
    return dl_file



def convert_video(conv_file, audio_format):
    # process output file name
    name_and_ext = conv_file.split('.')
    output_file = f'{name_and_ext[0]}.{audio_format}'

    if not os.path.exists(output_file):
        # convert file to audio_format
        stream = ffmpeg.input(conv_file)
        stream = ffmpeg.output(stream, output_file, format=audio_format)
        ffmpeg.run(stream)

    # remove original file with bestaudio_ext
    os.remove(conv_file)

    print(f"Downloaded and processed into {conv_file}'")



def prune_dict(ref_dict, features):
    def construct(ref_dict, construct_dict, split):
        # if [a1, a2, ..., an]
        curr_key = split[0]
        rest_keys = split[1:]
        
        # check if key exists
        if curr_key not in ref_dict:
            raise KeyError(f'{curr_key} doesn\'t exist in ref_dict')

        # base of dict: [a]
        if len(split) == 1:
            construct_dict[split[0]] = ref_dict[split[0]]
            return

        # recurse on sub-dicts
        if curr_key not in construct_dict:
            construct_dict[curr_key] = {}    
        construct(ref_dict[curr_key], construct_dict[curr_key], rest_keys)
            
    pruned_dict = {}
    [construct(ref_dict, pruned_dict, feat.split('.')) for feat in features]

    return pruned_dict

    

if __name__ == "__main__":
    # limit = input("Enter the number of videos to query: ")
    limit = 8
    limit_int = int(limit)

    query = "travis scott type beat"
    features = ['title', 'publishedTime', 'duration', 'channel.name', 'channel.id']
    
    (dlp_result, video_features) = search_queries(query, features, limit_int)

    print(json.dumps(video_features, indent=4))
    choices_str = input('Which videos look the best to you? Enter the index(es) as CSV: ')

    choices = [i for i in range(limit_int)] if choices_str == "all" else [int(c) for c in choices_str.split(',')]
    video_URLs = [dlp_result['result'][choice]['link'] for choice in choices]

    download_and_convert_videos(video_URLs, 'Travis/', 'mp3')