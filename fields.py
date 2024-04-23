import yt_to_mp3 as ytm

QUERY = "producerx weekend-type beat"
LIMIT = 3
FIELDS = ["title", "duration", "channel.name"]
ENGINE = "yt"
DL_FILEPATH = "/Users/neiltendolkar10/Music/Script_DL/"
CHOICES_STR = "0"
AUDIO_FORMAT = "mp3"

ENGINES = ["yt", "sc"]
YDL_OPTS = {
    'format': 'bestaudio',
}
