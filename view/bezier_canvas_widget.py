from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from view.base_canvas_widget import BaseCanvasWidget


class BezierCanvasWidget(BaseCanvasWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor('white'))
        if not self.presenter:
            return
        pass

