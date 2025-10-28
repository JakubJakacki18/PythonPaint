import math

from view.color_gl_widget import ColorGlWidget
from OpenGL.GL import *



class ConeGlWidget(ColorGlWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotatef(self.rot_x, 0, 1, 0)
        glRotatef(self.rot_y, 1, 0, 0)

        # Draw an RGB cone: base is white -> center black; circumference hues map around
        slices = 80
        height = 1.0
        radius = 0.8
        # draw cone surface: color varies between (r,g,b) depending on angle and y
        for i in range(slices):
            a0 = (2.0 * math.pi * i) / slices
            a1 = (2.0 * math.pi * (i + 1)) / slices
            # color on rim: map angle to RGB roughly (could be HSV->RGB)
            rim0 = self._angle_to_rgb(a0)
            rim1 = self._angle_to_rgb(a1)
            glBegin(GL_TRIANGLES)
            # tip (white)
            glColor3f(0.0, 0.0, 0.0)
            glVertex3f(0.0, height, 0.0)
            # rim vertices
            glColor3f(*rim0); glVertex3f(radius * math.cos(a0), 0.0, radius * math.sin(a0))
            glColor3f(*rim1); glVertex3f(radius * math.cos(a1), 0.0, radius * math.sin(a1))
            glEnd()

        # draw base (disk) fade to black center
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1, 1, 1); glVertex3f(0.0, 0.0, 0.0)
        for i in range(slices + 1):
            a = (2.0 * math.pi * i) / slices
            glColor3f(*self._angle_to_rgb(a))
            glVertex3f(radius * math.cos(a), 0.0, radius * math.sin(a))
        glEnd()

    def _angle_to_rgb(self, a):
        # map angle [0..2pi) to RGB via HSV-like mapping (H->RGB)
        h = (a / (2 * math.pi)) % 1.0
        return hsv_to_rgb(h, 1.0, 1.0)


# small helper
def hsv_to_rgb(h, s, v):
    # h in [0,1]
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
    return 1, 1, 1
