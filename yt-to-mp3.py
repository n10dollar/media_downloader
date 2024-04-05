from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

import ffmpeg
import os

def download_yt_video(query, audio_format):
    # search for videos matching the query
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()

    # get the first video's ID and title
    video_id = result['result'][0]['id']
    video_URL = result['result'][0]['link']
    video_title = result['result'][0]['title']

    # configure parameters
    ydl_opts = {
        'format': 'bestaudio'
    }

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

if __name__ == "__main__":
    query = input("Enter the title of the YouTube video: ")
    download_yt_video(query, 'mp3')
