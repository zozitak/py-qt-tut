import sys
from PyQt5.QtCore import Qt, QUrl, QSize, QRect, QEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.minimized = False

        self.resize(600, 500)
        self.setWindowTitle('Wiki')
        web = QWebEngineView(self)
        web.load(QUrl('https://github.com/aerospaceresearch/visma/wiki'))
        web.resize(600, 500)
        web.show()

    def popupBrowser(self):
        w = QDialog(self)
        w.resize(600, 500)
        w.setWindowTitle('Wiki')
        web = QWebEngineView(w)
        web.load(QUrl('https://github.com/aerospaceresearch/visma/wiki'))
        web.resize(600, 500)
        web.show()
        w.show() 

    def popupBrowser2(self):
        w = QDialog(self)
        w.resize(600, 500)
        w.setWindowTitle('Wiki')
        url = 'https://github.com/tody411/PyIntroduction'
        browser = QWebEngineView(w)
        browser.load(QUrl(url))
        browser.show()
        w.show() 

def mainPyQt5():

    app = QApplication(sys.argv)
    window = MainWindow()
    #window.popupBrowser()
    #window.popupBrowser2()
    
    window.show()
    app.exec_()

    sys.exit(app.exec_()) 

if __name__ == "__main__":
    mainPyQt5()