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
        self.features_val = FEATURES
        self.engine_val = ENGINE
        self.feature_data_val = None
        self.dl_filepath_val = DL_FILEPATH
        self.choices_str_val = CHOICES_STR
        self.audio_format_val = AUDIO_FORMAT

        # data variables
        self.media = None
        self.feature_data = None
        self.dl_files = None

        self.setWindowTitle('yt_to_mp3')
        self.setGeometry(X, Y, WIDTH, HEIGHT)

        # Create widgets
        self.query_tx = QLabel('Query:')
        self.query_res = QLineEdit()
        self.limit_tx = QLabel('Limit:')
        self.limit_res = QLineEdit()
        self.features_tx = QLabel('Features:')
        self.features_res = QLineEdit()
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

        self.feature_data_tx_scroll = QScrollArea()
        self.feature_data_tx = QLabel('')

        self.feature_data_tx_scroll.setWidgetResizable(True)
        self.feature_data_tx_scroll.setFixedHeight(HEIGHT / 2)
        self.feature_data_tx_scroll.setWidget(self.feature_data_tx)

        self.widgets = [self.query_tx, self.query_res,
                        self.limit_tx, self.limit_res,
                        self.features_tx, self.features_res,
                        self.engine_tx, self.engine_res,
                        self.search_but,
                        self.choices_tx, self.choices_res,
                        self.filepath_tx, self.filepath_res,
                        self.audio_format_tx, self.audio_format_res,
                        self.download_but,
                        self.feature_data_tx_scroll]

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
        self.features_val = self.features_res.text() or FEATURES
        self.engine_val = self.engine_res.text() if self.engine_res.text() in ENGINES else ENGINE

        media = prc.search(self.engine_val, self.query_val, int(self.limit_val))
        feature_data = prc.get_features(self.engine_val, media, self.features_val)

        self.media = media
        self.feature_data = feature_data

        self.feature_data_val = json.dumps(feature_data, indent=4)
        self.feature_data_tx.setText(self.feature_data_val)

    def on_download(self):
        self.dl_filepath_val = self.filepath_res.text() or DL_FILEPATH
        self.choices_str_val = self.choices_res.text() or CHOICES_STR
        self.audio_format_val = self.audio_format_res.text() or AUDIO_FORMAT

        choices = [int(c) for c in self.choices_str_val.split(',')]
        urls = utils.get_urls(self.engine_val, self.media, choices)

        ydl_opts = YDL_OPTS
        ydl_opts['outtmpl'] = f'{self.dl_filepath_val}%(title)s.%(ext)s'

        conv_files = prc.download_and_convert_multithread(urls, ydl_opts, self.audio_format_val)
        self.dl_files = conv_files


def pyside_gui_deploy():
    app = QApplication(sys.argv)
    widget = YTWidget()
    widget.show()
    sys.exit(app.exec())
