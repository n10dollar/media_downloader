import sys
import json
from PySide6.QtWidgets import *

import yt_to_mp3 as ytm
import yt_helpers as yth

QUERY = 'travis type beat'
LIMIT = 3
FIELDS = ['title', 'duration', 'channel.name']
ENGINE = 'YouTube'
DL_FILEPATH = '/Users/neiltendolkar10/Music/Script_DL/'
CHOICES_STR = '0'
AUDIO_FORMAT = 'mp3'

class YTWidget(QWidget):
    def __init__(self):
        super().__init__()

        # data variables (str)
        self.query_val = QUERY
        self.limit_val = LIMIT
        self.fields_val = FIELDS
        self.engine_val = ENGINE
        self.search_res_val = None
        self.video_features_val = None
        self.dl_filepath_val = DL_FILEPATH
        self.choices_str_val = CHOICES_STR
        self.audio_format_val = AUDIO_FORMAT

        self.dl_files = []

        self.setWindowTitle('Basic PySide6 GUI')
        self.setGeometry(100, 100, 800, 200)
        
        # Create widgets
        self.query = QLabel('Query:')
        self.query_res = QLineEdit()
        self.limit = QLabel('Limit:')
        self.limit_res = QLineEdit()
        self.fields = QLabel('Fields:')
        self.fields_res = QLineEdit()
        self.engine = QComboBox()
        self.search_but = QPushButton('Search')

        self.choices = QLabel('Choices:')
        self.choices_res = QLineEdit()
        self.filepath = QLabel('File Path:')
        self.filepath_res = QLineEdit()
        self.audio_format = QLabel('Format:')
        self.audio_format_res = QLineEdit()
        self.download_but = QPushButton('Download')

        self.video_features = QLabel('')

        self.engine.addItems(['Default', 'Youtube', 'SoundCloud', 'All'])

        self.widgets = [self.query, self.query_res, 
                        self.limit, self.limit_res,
                        self.fields, self.fields_res, 
                        self.engine,
                        self.search_but, 
                        self.choices, self.choices_res,
                        self.filepath, self.filepath_res,
                        self.audio_format, self.audio_format_res,
                        self.download_but,
                        self.video_features]

        # Connect button click event to a function
        self.search_but.clicked.connect(self.on_search)
        self.download_but.clicked.connect(self.on_download)

        # Create layout and add widgets
        layout = QVBoxLayout()
        [layout.addWidget(widget) for widget in self.widgets]

        # Set the layout for the widget
        self.setLayout(layout)


    def on_search(self):
        self.query_val = self.query_res.text() or QUERY
        self.limit_val = self.limit_res.text() or LIMIT
        self.fields_val = self.fields_res.text() or FIELDS
        self.engine_val = self.engine.currentText() or ENGINE

        engines_opts = {'YouTube': False, 'SoundCloud': False}
        engines_funcs = {'YouTube': ytm.search_youtube, 'SoundCloud': ytm.search_soundcloud}
        if self.engine_val == 'Default':
            engines_opts[ENGINE] = True
        elif self.engine_val == 'All':
            [engines_opts.update({engine: True}) for engine in engines_opts.keys()]
        else:
            [engines_opts.update({engine: True}) for engine in engines_opts.keys() if engine == self.engine_val]

        engines_search = [engines_funcs[engine] for engine in engines_opts if engines_opts[engine]]
        all_video_features = ''
        for engine_search in engines_search:
            search_res, video_features = engine_search(self.query_val, self.fields_val, int(self.limit_val))
            self.search_res_val = search_res
            self.video_features_val = video_features

            vid_feat_str = json.dumps(video_features, indent=4)
            all_video_features = f'{all_video_features}\n{vid_feat_str}'
            
        self.video_features_val = all_video_features
        self.video_features.setText(self.video_features_val)


    def on_download(self):
        self.dl_filepath_val = self.filepath_res.text() or DL_FILEPATH
        self.choices_str_val = self.choices_res.text() or CHOICES_STR
        self.audio_format_val = self.audio_format_res.text() or AUDIO_FORMAT

        video_URLs = yth.extract_URLs(self.search_res_val, self.limit, self.choices_str_val)
        conv_files = ytm.download_and_convert_videos(video_URLs, self.dl_filepath_val, self.audio_format_val)
        self.dl_files = conv_files



def pyside6_gui_deploy():
    app = QApplication(sys.argv)
    widget = YTWidget()
    widget.show()
    sys.exit(app.exec())