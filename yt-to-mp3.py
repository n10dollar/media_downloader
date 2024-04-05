from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import ffmpeg

def download_yt_video(query):
    # search for videos matching the query
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()

    # get the first video's ID and title
    video_id = result['result'][0]['id']
    video_URL = result['result'][0]['link']
    video_title = result['result'][0]['title']

    # configure parameters
    ydl_opts = {
        # 'format': 'bestaudio'
        # 'outtmpl': f'{video_title}.mp3',
    }

    # download the video
    ydl = YoutubeDL(ydl_opts)
    ydl.download([video_URL])

    file_name = video_title
    file_format = 'mp3'

    # convert it to mp3
    stream = ffmpeg.input(file_name)
    stream = ffmpeg.output(stream, file_name, format=file_format)
    ffmpeg.run(stream, overwrite_output=True)

    print(f"Downloaded {file_name}'")

if __name__ == "__main__":
    query = input("Enter the title of the YouTube video: ")
    download_yt_video(query)
