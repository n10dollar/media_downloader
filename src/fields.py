X = 100
Y = 100
WIDTH = 800
HEIGHT = 400

QUERY = "the weeknd - after hours"
LIMIT = 3
FEATURES = ["title", "duration", "channel.name"]
ENGINE = "sc"
DL_FILEPATH = "/Users/neiltendolkar10/Music/Script_DL/"
CHOICES_STR = "0,1"
AUDIO_FORMAT = "mp3"

ENGINES = ["yt", "sc"]
YDL_OPTS = {
    'format': 'bestaudio',
}
