from OpenGL import GL as gl
from OpenGL import GLU as glu
from OpenGL import GLUT as glut
#from OpenGLContext import testingcontext
#BaseContext = testingcontext.getInteractive()
#from gl.arrays import vbo as glVbo
#from OpenGLContext import arrays as glContextArrays
from  OpenGL.GL import shaders

import sys
import time

#class TestContext(BaseContext):
#    def OnInit(self):
#        print 'init base context'

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
    g_Width = width;
    g_Height = height;
    gl.glUniform2f(uniform_WindowSize, g_Width, g_Height);
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

    glut.glutSolidTeapot(.29)
    gl.glPopMatrix()

    gl.glPushMatrix()
    gl.glTranslate(.5, 0, 0) 
    gl.glRotatef(rot['x'], 1.0, 0.0, 0.0)
    gl.glRotatef(rot['y'], 0.0, 1.0, 0.0)
    gl.glRotatef(rot['z'], 0.0, 0.0, 1.0)

    glut.glutSolidTeapot(.29)
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

gl.glClearColor(.5,.5,.5,0)


vertex = shaders.compileShader(
    """
    varying vec4 pos;
    varying vec4 color;
    varying vec3 vertex_light_position;
    varying vec3 vertex_light_half_vector;
    varying vec3 vertex_normal;
 
    void main(){
        pos = gl_Position = gl_ModelViewProjectionMatrix*gl_Vertex;
        
        vertex_normal = normalize(gl_NormalMatrix * gl_Normal);
        vertex_light_position = normalize(gl_LightSource[0].position.xyz);
        vertex_light_half_vector = normalize(gl_LightSource[0].halfVector.xyz);
        
        gl_FrontColor=gl_Color;
        color = gl_Color;
    }""", gl.GL_VERTEX_SHADER)

fragment = shaders.compileShader("""
    varying vec4 pos;
    varying vec4 color;
    varying vec3 vertex_light_position;
    varying vec3 vertex_light_half_vector;
    varying vec3 vertex_normal;

    uniform sampler2D samp;
    uniform vec2 WindowSize;

    vec4 toon_color(vec4 tcolor)
    {
        vec4 retcolor;
        if(pos.x<0) retcolor = tcolor;
        else{
            vec4 tcolor_noalpha = tcolor;
            tcolor_noalpha.a = 0;
            float len = length(tcolor_noalpha);
            vec4 tcolor_norm = normalize(tcolor_noalpha);
            if(len>.8) {
                retcolor = tcolor_norm;
                tcolor_norm.a = 1.0;
            } else if(len>.5) {
                retcolor = .7*tcolor_norm;
                tcolor_norm.a = 1.0;
            } else if(len>.3) {
                retcolor = .2*tcolor_norm;
                tcolor_norm.a = 1.0;
            } else {
                retcolor = .1*tcolor_norm; 
                tcolor_norm.a = 1.0;
            }
        }
        return retcolor;
    }

    void main(){
        float diffuse_value = max(dot(vertex_normal, vertex_light_position), 0.0);

        vec4 diffuse_color = gl_FrontMaterial.diffuse*gl_LightSource[0].diffuse;
        vec4 ambient_color = gl_FrontMaterial.ambient * gl_LightSource[0].ambient + gl_LightModel.ambient * gl_FrontMaterial.ambient;
        vec4 specular_color = gl_FrontMaterial.specular * gl_LightSource[0].specular * pow(max(dot(vertex_normal, vertex_light_half_vector), 0.0) , gl_FrontMaterial.shininess);

        //vec4 pos = gl_FragCoord;
        vec4 tcolor = diffuse_color*diffuse_value+ambient_color+specular_color;

        if(pos.x>0&& pos.y>0)
        {
            int k = 5;
            vec4 adjacency[5][5];
            for(int i = 0; i<k; i++)
            {
                int ci = gl_PointCoord.x*WindowSize.x+i-k/2;
                for(int j = 0; j<k; j++)
                {
                    int cj = gl_PointCoord.y*WindowSize.y+j-k/2;
                    if(ci>k/2&&ci<WindowSize.x-k/2-1&&cj>k/2&&cj<WindowSize.y-k/2-1)
                    {
                        vec2 coord;
                        coord.x = ci/WindowSize.x;
                        coord.y = ci/WindowSize.y;
                        adjacency[ci-k/2][cj-k/2]=toon_color(tex2D(samp,coord));
                    }
                }
            }
            
            float sig = 1;
            float norm = 0;
            vec4 final_color;
            for(int i = 0; i<k; i++)
            {
                for(int j = 0; j<k; j++)
                {
                    float mltlen = length(adjacency[i][j]);
                    float mlt = exp(-mltlen*mltlen/(sig*sig));
                    norm = norm + mlt;
                    final_color = final_color+adjacency[i][j]*.1;
                    //final_color = final_color+vec4(1.0,0.0,0.0,0.0)/25.0;
                }       
            }
            final_color = final_color/norm;
            gl_FragColor = final_color;
            //gl_FragColor = adjacency[k/2][k/2];
        }
        else
        {
            gl_FragColor = toon_color(tcolor);
        }
    }""", gl.GL_FRAGMENT_SHADER)

shader = shaders.compileProgram(vertex,fragment)
uniform_WindowSize = gl.glGetUniformLocation(shader,'WindowSize');

gl.glUseProgram(shader)
gl.glUniform2f(uniform_WindowSize, g_Width, g_Height);

glut.glutTimerFunc(int(PERIOD), redraw, 0)
glut.glutMainLoop()

