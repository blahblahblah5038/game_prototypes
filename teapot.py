from OpenGL import GL as gl
from OpenGL import GLU as glu
from OpenGL import GLUT as glut
import sys
import time

FPS = 60.0 #the ideal number of frames per second
PERIOD = 1.0/FPS*1000 #convert frequency to period and convert from s to ms.
print PERIOD

#/* set the clear colour (R, G, B, A) */
gl.glClearColor(0.0, 0.0, 0.0, 1.0);
  
#/* position and orient the camera */ 
glu.gluLookAt(0.0, 0.0, 10.0, 
    0.0, 0.0, 0.0,  
    0.0, 1.0, 0.0); 

rot = dict()
rot['x'] = 0.0
rot['y'] = 0.0
rot['z'] = 0.0

def redraw(ignored):
    glut.glutPostRedisplay()

def reshape(width, height):
  #/* set the viewport to the window width and height */
  gl.glViewport(0, 0, width, height);
  
  #/* load a projection matrix that matches the window aspect ratio */
  gl.glMatrixMode(gl.GL_PROJECTION);
  gl.glLoadIdentity();
  glu.gluPerspective(0, float(width)/float(height), 1.0, 100.0);

  #/* reset the modelview matrix */
  gl.glMatrixMode(gl.GL_MODELVIEW);

def keyboard(key, x, y):
    if key == '=':
        rot['x']=rot['x']+10.0
    if key == '-':
        rot['x']=rot['x']-10.0
    if key == ']':
        rot['y']=rot['y']+10.0
    if key == '[':
        rot['y']=rot['y']-10.0
    if key == '\'':
        rot['z']=rot['z']+10.0
    if key == ';':
        rot['z']=rot['z']-10.0

    if rot['x']>=360:
        rot['x'] = rot['x'] - 360.0
    if rot['x']<0:
        rot['x'] = rot['x'] + 360.0
    if rot['y']>=360:
        rot['y'] = rot['y'] - 360.0
    if rot['y']<0:
        rot['y'] = rot['y'] + 360.0
    if rot['z']>=360:
        rot['z'] = rot['z'] - 360.0
    if rot['z']<0:
        rot['z'] = rot['z'] + 360.0

def display():
    start = time.time()

    gl.glClear(gl.GL_COLOR_BUFFER_BIT |gl.GL_DEPTH_BUFFER_BIT) 

    gl.glPushMatrix()
    gl.glRotatef(rot['x'], 1.0, 0.0, 0.0)
    gl.glRotatef(rot['y'], 0.0, 1.0, 0.0)
    gl.glRotatef(rot['z'], 0.0, 0.0, 1.0)

    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, [1.0,1.0,1.0,1.0]);
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION,[0.4,0.0,-1.0,0.0]); 
    gl.glPopMatrix()

    gl.glPushMatrix()
    gl.glTranslate(-.5, 0, 0) 
    gl.glRotatef(rot['x'], 1.0, 0.0, 0.0)
    gl.glRotatef(rot['y'], 0.0, 1.0, 0.0)
    gl.glRotatef(rot['z'], 0.0, 0.0, 1.0)

    glut.glutSolidTeapot(.3)
    gl.glPopMatrix()

    gl.glPushMatrix()
    gl.glTranslate(.5, 0, 0) 
    gl.glRotatef(rot['x'], 1.0, 0.0, 0.0)
    gl.glRotatef(rot['y'], 0.0, 1.0, 0.0)
    gl.glRotatef(rot['z'], 0.0, 0.0, 1.0)

    glut.glutSolidTeapot(.3)
    glut.glutSwapBuffers()
    gl.glPopMatrix()

    end = time.time()

    per = max([0,PERIOD-end+start])
    glut.glutTimerFunc(int(per), redraw, 0)
    glut.glutSwapBuffers()

g_Width = 700
g_Height = 700

glut.glutInit(len(sys.argv), sys.argv)
glut.glutInitWindowSize (g_Width, g_Height)
glut.glutInitDisplayMode(glut.GLUT_RGBA|glut.GLUT_DOUBLE|glut.GLUT_DEPTH)
glut.glutCreateWindow('toon shading test')

gl.glEnable(gl.GL_LIGHTING)
gl.glEnable(gl.GL_LIGHT0)
gl.glEnable(gl.GL_DEPTH_TEST)

glut.glutDisplayFunc(display)
glut.glutReshapeFunc(reshape)
glut.glutKeyboardFunc(keyboard)

#/* define material properties */
material_ambient = [0.20, 0.20, 0.4];
material_diffuse = [0.60, 0.60, 0.90];
material_specular = [0.90, 0.90, 0.90];
material_shininess = 25.0;

#/* load material properties */
gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT, material_ambient);
gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, material_diffuse);
gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, material_specular);
gl.glMaterialf(gl.GL_FRONT, gl.GL_SHININESS, material_shininess);

glut.glutTimerFunc(int(PERIOD), redraw, 0)
glut.glutMainLoop()

