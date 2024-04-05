from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from ffmpeg import stream

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

    # convert it to mp3
    str = stream.Stream()
    str.input(file_name)
    str.out()
    

    print(f"Downloaded '{video_title}.mp3'")

if __name__ == "__main__":
    query = input("Enter the title of the YouTube video: ")
    download_yt_video(query)
