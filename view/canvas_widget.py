from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QPointF

from model.point import Point
from utils.draw_map import DRAW_MAP


class CanvasWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.setMouseTracking(True)
        self.presenter = None

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_press(pos)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_move(pos)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_release(pos)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor('white'))
        if self.presenter:
            for shape in self.presenter.get_shapes():
                render_func = DRAW_MAP.get(type(shape))
                render_func(painter,self.presenter.current_pen ,shape)
    