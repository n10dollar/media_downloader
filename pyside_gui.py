import sys
import json
from PySide6.QtWidgets import *

import process as prc
import utils
from fields import *

class YTWidget(QWidget):
    def __init__(self):
        super().__init__()

        # data variables (str)
        self.query_val = QUERY
        self.limit_val = LIMIT
        self.fields_val = FIELDS
        self.engine_val = ENGINE
        self.media_val = None
        self.video_features_val = None
        self.dl_filepath_val = DL_FILEPATH
        self.choices_str_val = CHOICES_STR
        self.audio_format_val = AUDIO_FORMAT

        # data variables
        self.media = None
        self.video_features = None

        self.dl_files = None

        self.setWindowTitle('yt_to_mp3')
        self.setGeometry(100, 100, 800, 200)

        # Create widgets
        self.query_tx = QLabel('Query:')
        self.query_res = QLineEdit()
        self.limit_tx = QLabel('Limit:')
        self.limit_res = QLineEdit()
        self.fields_tx = QLabel('Fields:')
        self.fields_res = QLineEdit()
        self.engine_tx = QLabel('Engine:')
        self.engine_res = QLineEdit()
        self.search_but = QPushButton('Search')

        self.choices_tx = QLabel('Choices:')
        self.choices_res = QLineEdit()
        self.filepath_tx = QLabel('File Path:')
        self.filepath_res = QLineEdit()
        self.audio_format_tx = QLabel('Format:')
        self.audio_format_res = QLineEdit()
        self.download_but = QPushButton('Download')

        self.video_features_tx = QLabel('')

        self.widgets = [self.query_tx, self.query_res,
                        self.limit_tx, self.limit_res,
                        self.fields_tx, self.fields_res,
                        self.engine_tx,
                        self.search_but,
                        self.choices_tx, self.choices_res,
                        self.filepath_tx, self.filepath_res,
                        self.audio_format_tx, self.audio_format_res,
                        self.download_but,
                        self.video_features_tx]

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
        self.engine_val = self.engine_res.text() or ENGINE

        media, video_features = prc.search(self.engine_val, self.query_val, int(self.limit_val))

        self.media = media
        self.video_features = video_features

        self.video_features_val = video_features
        self.video_features.setText(self.video_features_val)

    def on_download(self):
        self.dl_filepath_val = self.filepath_res.text() or DL_FILEPATH
        self.choices_str_val = self.choices_res.text() or CHOICES_STR
        self.audio_format_val = self.audio_format_res.text() or AUDIO_FORMAT

        choices = [int(c) for c in self.choices_str_val.split(',')]
        urls = [self.media[choice]['link'] for choice in choices]

        conv_files = prc.download_and_convert_multithread(urls, YDL_OPTS, self.audio_format_val)
        self.dl_files = conv_files


def pyside6_gui_deploy():
    app = QApplication(sys.argv)
    widget = YTWidget()
    widget.show()
    sys.exit(app.exec())


# engines = [(name, search_func)]
def search(engines, query, fields, limit):
    search_ress = []
    video_features = {}
    for name, search_func in engines:
        search_res, video_features = search_func(query, fields, limit)
        search_ress.append(search_res)
        vid_feat_str = json.dumps(video_features, indent=4)
        video_features[name] = vid_feat_str

    features_str = ''
    for name, features in video_features:
        features_str = f'{features_str}\n_____{name}_____\n{features}'

    return search_ress, features_str
