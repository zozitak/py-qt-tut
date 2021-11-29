# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from PIL import Image

# vertex_code = """
#     attribute vec2 position;
#     attribute vec4 color;
#     varying vec4 v_color;
#     void main()
#     {
#     gl_Position = vec4(position, 0.0, 1.0);
#     v_color= color;
#     } 
#     """

# fragment_code = """
# varying vec4 v_color;
# void main()
# {
#   gl_FragColor = color;
# }
#     """

vertex_code = '''
layout(location = 0) in vec3 vertexPosition_modelspace;
layout(location = 1) in vec2 vertexUV;

out vec2 UV;

uniform mat4 MVP;

void main(){

    gl_Position =  MVP * vec4(vertexPosition_modelspace,1);

    UV = vertexUV;
}
'''

fragment_code = '''

in vec2 UV;

out vec3 color;

uniform sampler2D myTextureSampler;

void main(){

    color = texture( myTextureSampler, UV ).rgb;
}

'''

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
    glut.glutSwapBuffers()

def reshape(width,height):
    gl.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b':
        sys.exit( )

# GLUT init
# --------------------------------------
glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Hello world!')
glut.glutReshapeWindow(512,512)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

# Build data
# --------------------------------------
# data = np.zeros(4, [("position", np.float32, 2)])
# data['position'] = [(-1,+1), (+1,+1), (-1,-1), (+1,-1)]
data = np.zeros(4, [("position", np.float32, 2),
                    ("color",    np.float32, 4)])
data['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
data['color']    = (0,1,0,1), (1,1,0,1), (1,0,0,1), (0,0,1,1)

# Build texture 
# --------------------------------------
def load_JGP(res):
    img = Image.open(res)
    img_data = np.array(list(img.getdata()), np.int8)

    texture_id = 0
    texture_id = gl.glGenTextures(1, texture_id)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0,gl.GL_RGB, img.size[0], img.size[1], 0, gl.GL_BGR, gl.GL_UNSIGNED_BYTE, img_data)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    return texture_id

textureID = 0    
textureID = load_JGP("resources/wood.jpg")

# Build & activate program
# --------------------------------------
# Request a program and shader slots from GPU
program  = gl.glCreateProgram()
vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

# Set shaders source
gl.glShaderSource(vertex, vertex_code)
gl.glShaderSource(fragment, fragment_code)

# Compile shaders
gl.glCompileShader(vertex)
if not gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS):
    error = gl.glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Shader compilation error")
                
gl.glCompileShader(fragment)
gl.glCompileShader(fragment)
if not gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS):
    error = gl.glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Shader compilation error")                

# Attach shader objects to the program
gl.glAttachShader(program, vertex)
gl.glAttachShader(program, fragment)

# Build program
gl.glLinkProgram(program)
if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
    print(gl.glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')

# Get rid of shaders (no more needed)
gl.glDetachShader(program, vertex)
gl.glDetachShader(program, fragment)

# Make program the default program
gl.glUseProgram(program)

# Build buffer
# --------------------------------------

# Request a buffer slot from GPU
buffer = gl.glGenBuffers(1)

# Make this buffer the default one
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

# Upload data
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

# Bind the position attribute
# --------------------------------------
stride = data.strides[0]
offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)

# Upload the uniform color
# --------------------------------------
# loc = gl.glGetUniformLocation(program, "color")
# gl.glUniform4f(loc, 0.0, 0.0, 1.0, 1.0)
offset = ctypes.c_void_p(data.dtype["position"].itemsize)
loc = gl.glGetAttribLocation(program, "color")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

# Enter the mainloop
# --------------------------------------
glut.glutMainLoop()