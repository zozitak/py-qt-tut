import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        label = QLabel("This is a PyQt5 window!")

        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

app = QApplication(sys.argv)

window = MainWindow()
#window.setWindowOpacity(0.3)
#window.setAttribute(Qt.WA_TranslucentBackground, True)
window.show()

sys.exit(app.exec_())
