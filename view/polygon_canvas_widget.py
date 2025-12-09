from PyQt6 import QtGui
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPen

from model.point import Point
from utils.enums.advanced_tools import AdvancedTools
from view.base_canvas_widget import BaseCanvasWidget


class PolygonCanvasWidget(BaseCanvasWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor("white"))

        if not self.presenter:
            return
        points = self.presenter.get_points()
        qpoints = [QPointF(point.x, point.y) for point in points]

        if self.presenter.current_tool == AdvancedTools.ROTATE and (
            point := self.presenter.rotate_axis
        ):
            painter.setPen(QPen(Qt.GlobalColor.blue, 6))
            painter.drawPoint(QPointF(point.x, point.y))

        painter.setPen(QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.SolidLine))
        for i in range(len(qpoints) - 1):
            painter.drawLine(qpoints[i], qpoints[i + 1])
        if len(qpoints) > 2:
            painter.drawLine(qpoints[-1], qpoints[0])
        painter.setPen(QPen(Qt.GlobalColor.red, 6))
        for pt in qpoints:
            painter.drawPoint(pt)

        painter.setPen(QPen(Qt.GlobalColor.blue, 2))

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_press(pos, event.button())
