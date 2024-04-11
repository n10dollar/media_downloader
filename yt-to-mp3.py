from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

import ffmpeg
import os

import json

def download_yt_video(query, dl_filepath, limit, audio_format):
    # search for videos matching the query
    videos_search = VideosSearch(query, limit=limit)
    result = videos_search.result()
    videos = result['result']

    # extract important features
    video_features = []
    features = ['title', 'publishedTime', 'duration', 'channel.name', 'channel.id']
    [video_features.append(prune_dict(vid, features)) for vid in videos]
    
    print(json.dumps(video_features, indent=4))
    choices_str = input('Which videos look the best to you? Enter the index(es) in CSV format (zero-indexed), or say "all": ')
    choices = [i for i in range(limit)] if choices_str == "all" else [int(c) for c in choices_str.split(',')]

    # get the videos' URLS
    video_URLs = [result['result'][choice]['link'] for choice in choices]

    # configure parameters
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{dl_filepath}%(title)s.%(ext)s'
    }

    [download_and_process(ydl_opts, video_URL, audio_format) for video_URL in video_URLs]



def download_and_process(ydl_opts, video_URL, audio_format):
    # video data
    ydl = YoutubeDL(ydl_opts)
    video_info = ydl.extract_info(video_URL, download=False)
    bestaudio_ext = video_info.get('ext')

    downloaded_file_name = ydl.prepare_filename(video_info)
    processed_file_name = f'{downloaded_file_name.removesuffix(bestaudio_ext)}{audio_format}'

    # download file
    ydl.download([video_URL])

    # convert it to audio_format
    stream = ffmpeg.input(downloaded_file_name)
    stream = ffmpeg.output(stream, processed_file_name, format=audio_format)
    ffmpeg.run(stream, overwrite_output=True)

    # remove original file with bestaudio_ext
    os.remove(downloaded_file_name)

    print(f"Downloaded and processed into {processed_file_name}'")



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
    # query = input("Enter the title of the YouTube video: ")
    limit = input("Enter the number of videos to query: ")

    # download_yt_video(query, 'YouTube/', int(limit), 'mp3')
    query = "best weeknd-type synthwave beats"
    download_yt_video(query, 'Synthwave/', int(limit), 'mp3')
