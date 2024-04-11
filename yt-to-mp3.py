from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

import ffmpeg
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



def download_videos(dlp_result, dl_filepath, choices_str):
    # parse choices input
    choices = [i for i in range(limit)] if choices_str == "all" else [int(c) for c in choices_str.split(',')]

    # configure parameters
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{dl_filepath}%(title)s.%(ext)s'
    }

    # get the videos' URLS
    ydl = YoutubeDL(ydl_opts)
    video_URLs = [dlp_result['result'][choice]['link'] for choice in choices]

    # video identifiers
    dl_files = []

    # download videos
    for video_URL in video_URLs:
        # video data
        video_info = ydl.extract_info(video_URL, download=False)

        downloaded_file_name = ydl.prepare_filename(video_info)
        dl_files.append(downloaded_file_name)

        # download file
        ydl.download([video_URL])
    
    return dl_files



def convert_videos(conv_files, audio_format):
    for conv_file in conv_files:
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
    limit = input("Enter the number of videos to query: ")

    query = "best travis scott type beat"
    features = ['title', 'publishedTime', 'duration', 'channel.name', 'channel.id']
    
    (dlp_result, video_features) = search_queries(query, features, int(limit))

    print(json.dumps(video_features, indent=4))
    choices_str = input('Which videos look the best to you? Enter the index(es) as CSV: ')

    dl_files = download_videos(dlp_result, 'Synthwave/', choices_str)
    print(dl_files)
    convert_videos(dl_files, 'mp3')