from yt_dlp import YoutubeDL

import ffmpeg
import os

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

    

def extract_URLs(dlp_result, limit, choices_str):
    choices = [i for i in range(limit)] if choices_str == "all" else [int(c) for c in choices_str.split(',')]
    video_URLs = [dlp_result['result'][choice]['link'] for choice in choices]

    return video_URLs
