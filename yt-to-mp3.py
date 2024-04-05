from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import os

def search_and_download(query):
    # Search for videos matching the query
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()

    if not result['result']:
        print("No video found matching the query.")
        return

    # Get the first video's ID and title
    video_id = result['result'][0]['id']
    video_URL = result['result'][0]['link']
    video_title = result['result'][0]['title']

    ydl_opts = {
        # 'format': 'bestaudio'
        # 'outtmpl': f'{video_title}.mp3',
    }

    # Download the video and convert it to MP3
    ydl = YoutubeDL(ydl_opts)
    ydl.download([video_URL])
    

    print(f"Downloaded '{video_title}.mp3'")

if __name__ == "__main__":
    query = input("Enter the title of the YouTube video: ")
    search_and_download(query)
