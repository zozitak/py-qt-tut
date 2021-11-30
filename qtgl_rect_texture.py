import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
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
        glViewport(0,0,640,640)

    def paintGL(self):
        draw_my_rect()



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

def draw_my_rect():
    
                   #positions        colors               texture coords
    rectangle = [-0.9, -0.9, 0.0,   1.0, 0.0, 0.0,          0.0, 0.0,
            0.9, -0.9, 0.0,         0.0, 1.0, 0.0,          1.0, 0.0,
            0.9, 0.9, 0.0,          0.0, 0.0, 1.0,          1.0, 1.0,
            -0.9, 0.9, 0.0,         1.0, 1.0, 1.0,           0.0, 1.0]
   
    # convert to 32bit float

    rectangle = np.array(rectangle, dtype=np.float32)

    indices = [0,1,2,
              2,3,0]

    indices = np.array(indices, dtype = np.uint32)

    VERTEX_SHADER = """

           #version 330

           in vec3 position;
           in vec3 color;
           in vec2 InTexCoords;
           
           out vec3 newColor;
           out vec2 OutTexCoords;

           void main() {

            gl_Position = vec4(position, 1.0);
            newColor = color;
            OutTexCoords = InTexCoords;

             }


       """

    FRAGMENT_SHADER = """
        #version 330

         in vec3 newColor;
         in vec2 OutTexCoords;
         
         out vec4 outColor;
         uniform sampler2D samplerTex;

        void main() {

           outColor = texture(samplerTex, OutTexCoords);

        }

    """

    # Compile The Program and shaders

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))

    # Create Buffer object in gpu
    VBO = glGenBuffers(1)
    # Bind the buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 128, rectangle, GL_STATIC_DRAW)

    #Create EBO
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    # get the position from  shader
    position = 0
    glBindAttribLocation(shader,position,'position')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    # get the color from  shader
    color = 1 
    glBindAttribLocation(shader,color,'color')
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    texCoords = 2
    glBindAttribLocation(shader,texCoords,'InTexCoords')
    glVertexAttribPointer(texCoords,2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(texCoords)

    #Creating Texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # image = Image.open("resources/wood.jpg")
    # img_data = np.array(list(image.getdata()), np.uint8)
    ## better image code:
    try:
        image = Image.open("resources/wood.jpg")
    except IOError as err:
        print( '\n image not found \n msg: ', err , '\n' )
        sys.exit(1)
    #
    img_data = np.array( image , np.uint8 )
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    glUseProgram(shader)

    glClearColor(1.0, 0.0, 0.0, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)

    # Draw Rectangle

    glDrawElements(GL_TRIANGLES,6, GL_UNSIGNED_INT,  None)

if __name__ == '__main__':    
    app = QtWidgets.QApplication(sys.argv)    
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(Form)    
    ui.show()    
    sys.exit(app.exec_())