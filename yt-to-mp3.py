from youtubesearchpython import VideosSearch
import youtube_dl

def search_and_download(query):
    # Search for videos matching the query
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()

    if not result['result']:
        print("No video found matching the query.")
        return

    # Get the first video's ID and title
    video_id = result['result'][0]['id']
    video_title = result['result'][0]['title']

    # Download the video and convert it to MP3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{video_title}.mp3',
        'listformats': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL() as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

    print(f"Downloaded '{video_title}.mp3'")

if __name__ == "__main__":
    query = input("Enter the title of the YouTube video: ")
    search_and_download(query)
