from PyQt6.QtCore import QPoint, pyqtSignal, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

class ColorGlWidget(QOpenGLWidget):
    colorPicked = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setMinimumSize(200, 200)
        self.rot_x = 30.0
        self.rot_y = 30.0
        self.last_pos = QPoint()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.3, 0.3, 0.3, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / max(1.0, h)
        glOrtho(-1.5 * aspect, 1.5 * aspect, -1.5, 1.5, -10, 10)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, ev):
        self.last_pos = ev.pos()
        if ev.button() == Qt.MouseButton.LeftButton:
            self.pick_color(ev.pos())

    def mouseMoveEvent(self, ev):
        pos = ev.position()
        dx = pos.x() - self.last_pos.x()
        dy = pos.y() - self.last_pos.y()
        self.rot_x += dx * 0.4
        self.rot_y += dy * 0.4
        self.last_pos = ev.pos()
        self.update()

    def pick_color(self, pos):
        img = self.grabFramebuffer()
        if img.isNull():
            return
        x = pos.x()
        y = pos.y()
        if x < 0 or y < 0 or x >= img.width() or y >= img.height():
            return
        c = QColor(img.pixel(x, y))
        picked = (c.redF(), c.greenF(), c.blueF())
        self.colorPicked.emit(picked)