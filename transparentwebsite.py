import sys
from PyQt5.QtCore import Qt, QUrl, QSize, QRect, QEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        # self.setWindowFlags(Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setAttribute(Qt.WA_NoSystemBackground,False)
        self.minimized = False
        
        #p = self.palette()
        #p.setColor(self.backgroundRole(),Qt.transparent)
        #self.setPalette(p)
        #self.setAutoFillBackground(True)

        self.browser = QWebEngineView()
        self.settings = self.browser.settings()
        #self.browser.setAttribute(Qt.WA_TranslucentBackground)
        #self.browser.setBackgroundRole(QPalette.NoRole)
        #self.browser.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self.settings.setAttribute(self.settings.ShowScrollBars,False)
        #self.browser.setUrl(QUrl("wwww.google.com"))
        self.browser.load(QUrl("wwww.google.com"))
        self.setCentralWidget(self.browser)
        ##        self.installEventFilter(self)
        self.browser.show()
        
    # def centerAndResize(self,ScreenNumber):
    #     desktop = qApp.desktop()
    #     availableSize = desktop.screenGeometry(ScreenNumber).size()
    #     width = availableSize.width()
    #     height = availableSize.height()
    #     newSize = QSize(width, height)
    #     self.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
    #                                         Qt.AlignCenter,
    #                                         newSize,
    #                                         desktop.screenGeometry(ScreenNumber)))
    ##############################################################
    ## Events
    ##############################################################
    ##    def eventFilter(self, obj, event):
    ##        
    ##        return super(MainWindow, self).eventFilter(obj, event) 
    
    def changeEvent(self,event):
        if event.type() == QEvent.WindowStateChange :
            if event.oldState() != Qt.WindowMinimized :
                self.showNormal()
    
    ##    def closeEvent(self, event):
    ##        print(event)
        
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
