from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QPointF, QRect

from model.point import Point
from utils.draw_map import DRAW_MAP


class CanvasWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.presenter = None
        self.image = None

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
            self.presenter.handle_mouse_release()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor('white'))
        if self.image:
            painter.drawImage(0, 0, self.image)
        if not self.presenter:
            return
        for shape in self.presenter.get_shapes():
            render_func = DRAW_MAP.get(type(shape))
            render_func(painter,shape.pen ,shape)
            if self.presenter.selected_shape:
                painter.setPen(QtGui.QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
                x1, y1, x2, y2 = self.presenter.selected_shape.bounding_box()
                width=x2-x1
                height=y2-y1
                painter.drawRect(QRect(int(x1), int(y1), int(width), int(height)))

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        print("Kod klawisza:", event.key())
        print("Znak:", event.text())
        if self.presenter:
            self.presenter.handle_key_press(event)

    def set_image(self, image: QtGui.QImage):
        self.image = image
        self.update()
