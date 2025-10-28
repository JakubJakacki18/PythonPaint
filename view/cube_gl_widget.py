from PyQt6.QtCore import pyqtSignal, QPoint, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

from view.color_gl_widget import ColorGlWidget


class CubeGlWidget(ColorGlWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotatef(self.rot_x, 0, 1, 0)
        glRotatef(self.rot_y, 1, 0, 0)

        glBegin(GL_QUADS)
        # +X face (red varying)
        glColor3f(1, 0, 0); glVertex3f(0.5, -0.5, -0.5)
        glColor3f(1, 1, 0); glVertex3f(0.5, 0.5, -0.5)
        glColor3f(1, 1, 1); glVertex3f(0.5, 0.5, 0.5)
        glColor3f(1, 0, 1); glVertex3f(0.5, -0.5, 0.5)

        # -X
        glColor3f(0, 0, 0); glVertex3f(-0.5, -0.5, -0.5)
        glColor3f(0, 1, 0); glVertex3f(-0.5, 0.5, -0.5)
        glColor3f(0, 1, 1); glVertex3f(-0.5, 0.5, 0.5)
        glColor3f(0, 0, 1); glVertex3f(-0.5, -0.5, 0.5)

        # +Y
        glColor3f(0, 1, 0); glVertex3f(-0.5, 0.5, -0.5)
        glColor3f(1, 1, 0); glVertex3f(0.5, 0.5, -0.5)
        glColor3f(1, 1, 1); glVertex3f(0.5, 0.5, 0.5)
        glColor3f(0, 1, 1); glVertex3f(-0.5, 0.5, 0.5)

        # -Y
        glColor3f(0, 0, 0); glVertex3f(-0.5, -0.5, -0.5)
        glColor3f(1, 0, 0); glVertex3f(0.5, -0.5, -0.5)
        glColor3f(1, 0, 1); glVertex3f(0.5, -0.5, 0.5)
        glColor3f(0, 0, 1); glVertex3f(-0.5, -0.5, 0.5)

        # +Z
        glColor3f(0, 0, 1); glVertex3f(-0.5, -0.5, 0.5)
        glColor3f(1, 0, 1); glVertex3f(0.5, -0.5, 0.5)
        glColor3f(1, 1, 1); glVertex3f(0.5, 0.5, 0.5)
        glColor3f(0, 1, 1); glVertex3f(-0.5, 0.5, 0.5)

        # -Z
        glColor3f(0, 0, 0); glVertex3f(-0.5, -0.5, -0.5)
        glColor3f(0, 1, 0); glVertex3f(-0.5, 0.5, -0.5)
        glColor3f(1, 1, 0); glVertex3f(0.5, 0.5, -0.5)
        glColor3f(1, 0, 0); glVertex3f(0.5, -0.5, -0.5)
        glEnd()
