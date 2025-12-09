from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen

from model.point import Point
from utils.enums.advanced_tools import AdvancedTools
from view.base_canvas_widget import BaseCanvasWidget


class BezierCanvasWidget(BaseCanvasWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    @staticmethod
    def _bezier_point(t, points):
        n = len(points)
        pts = points.copy()

        while n > 1:
            new_pts = []
            for i in range(n - 1):
                x = (1 - t) * pts[i].x() + t * pts[i + 1].x()
                y = (1 - t) * pts[i].y() + t * pts[i + 1].y()
                new_pts.append(QPointF(x, y))
            pts = new_pts
            n -= 1

        return pts[0]

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

        painter.setPen(QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.DashLine))
        for i in range(len(qpoints) - 1):
            painter.drawLine(qpoints[i], qpoints[i + 1])

        painter.setPen(QPen(Qt.GlobalColor.red, 6))
        for pt in qpoints:
            painter.drawPoint(pt)

        painter.setPen(QPen(Qt.GlobalColor.blue, 2))
        if qpoints:
            prev = BezierCanvasWidget._bezier_point(0, qpoints)
            steps = 200

            for i in range(1, steps + 1):
                t = i / steps
                p = BezierCanvasWidget._bezier_point(t, qpoints)
                painter.drawLine(prev, p)
                prev = p

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_press(pos, event.button())
