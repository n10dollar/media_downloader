import sys
import json
from PySide6.QtWidgets import *

import yt_to_mp3 as ytm


class YTWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Basic PySide6 GUI")
        self.setGeometry(100, 100, 300, 200)
        
        # Create widgets
        self.query = QLabel("Enter search query:")
        self.query_res = QLineEdit()
        self.count = QLabel("Enter search count:")
        self.count_res = QLineEdit()
        self.search_but = QPushButton("Search")
        self.video_features = QLabel("placeholder")

        self.widgets = [self.query, self.query_res, self.count, self.count_res, self.search_but, self.video_features]

        # Connect button click event to a function
        self.search_but.clicked.connect(self.on_search)

        # Create layout and add widgets
        layout = QVBoxLayout()
        [layout.addWidget(widget) for widget in self.widgets]

        # Set the layout for the widget
        self.setLayout(layout)


    def on_search(self):
        query = self.query_res.text()
        count = self.count_res.text()

        features = ['title', 'publishedTime', 'duration', 'channel.name', 'channel.id']
        dlp_result, video_features = ytm.search_queries(query, features, int(count))
        vid_feat_str = json.dumps(video_features, indent=4)

        self.video_features.setText(vid_feat_str)



def pyside6_gui_deploy():
    app = QApplication(sys.argv)
    widget = YTWidget()
    widget.show()
    sys.exit(app.exec())