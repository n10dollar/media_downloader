import os

X = 100
Y = 100
WIDTH = 800
HEIGHT = 400

QUERY = "cool new instrumentals!"
LIMIT = 3
FEATURES = ["title", "duration", "channel.name"]
ENGINE = "yt"
DL_FILEPATH = os.path.expanduser("/Music/Media_Converter/")
CHOICES_STR = "0"
AUDIO_FORMAT = "mp3"

ENGINES = ["yt", "sc"]
YDL_OPTS = {
    'format': 'bestaudio',
}
