from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QPointF, QRect

from model.image import Image
from model.point import Point
from utils.draw_map import DRAW_MAP
from view.base_canvas_widget import BaseCanvasWidget


class CanvasWidget(BaseCanvasWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor('white'))
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
