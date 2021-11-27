import sys
import argparse

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngine import QWebEngineView
from PyQt5.QtWebEngine import QWebEnginePage


def parse_args():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="./try1.html")
    return parser.parse_known_args()[0]


if __name__ == '__main__':
    args = parse_args()
    app = QApplication(sys.argv)
    wv = QWebEngineView()

    wv.loadStarted.connect(lambda: print("Loading started"))
    wv.loadProgress.connect(lambda p: print("Loading progress: {}%".format(p)))
    wv.loadFinished.connect(lambda: print("Loading finished"))
    wv.setWindowFlags(Qt.FramelessWindowHint)
    wv.setAttribute(Qt.WA_TranslucentBackground, True)
    #wv.setStyleSheet("background:transparent;")

    wv.load(QUrl.fromUserInput(args.url))

    wv.setWindowOpacity(0.6)                                  # +++
    wv.setWindowFlags(Qt.WindowStaysOnBottomHint)             # +++

    wv.show()

    app.exec_()
