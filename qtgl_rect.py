import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtWidgets, QtOpenGL
from PIL import Image
import numpy as np


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()
        self.widget = glWidget()
        #self.button = QtWidgets.QPushButton('Test', self)
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(self.widget)
        #mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)

class glWidget(QGLWidget):
    texture_id = 0

    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 640)

    def initializeGL(self):
        glClearDepth(1.0)              
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()               
        glViewport(0,0,640,640)     
        gluPerspective(45.0,1.0,0.1, 100.0) 
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClearColor(0.5, 0.2, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, 0.0)
        glPolygonMode(GL_FRONT, GL_FILL)

        #draw rect 
        x1 = -5.0
        y1 = -5.0
        z1 = -0.1 
        width = x1 + 10.0 
        height = y1 + 10.0
        glColor(0.7,0.3,0.0)
        glBegin(GL_POLYGON)
        glVertex3f(x1, y1, z1)
        glVertex3f(width, y1, z1)
        glVertex3f(width, height, z1)
        glVertex3f(x1, height, z1)
        
        glEnd()
        glFlush()



def read_texture(filename):
    #Texture Creation
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    try:
        image = Image.open(filename)
    except IOError as err:
        print( '\n image not found \n msg: ', err , '\n' )
        sys.exit(1)
    #
    img_data = np.array( image , np.uint8 )

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)
    return texture_id

if __name__ == '__main__':    
    app = QtWidgets.QApplication(sys.argv)    
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(Form)    
    ui.show()    
    sys.exit(app.exec_())