import yt_to_mp3 as ytm

QUERY = "producerx"
LIMIT = 3
FIELDS = ["title", "duration", "channel.name"]
ENGINE = "Youtube"
DL_FILEPATH = "/Users/neiltendolkar10/Music/Script_DL/"
CHOICES_STR = "0"
AUDIO_FORMAT = "mp3"

ENGINES = ["yt", "sc"]
YDL_OPTS = {
    'format': 'best-audio',
}

# 'outtmpl': f'{dl_filepath}%(title)s.%(ext)s'