from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt, QPointF, QRectF
from old_model.shape import Shape

class Line(Shape):
    def __init__(self, p1: QPointF, p2: QPointF, pen: QtGui.QPen):
        super().__init__(pen)
        self.p1 = QPointF(p1)
        self.p2 = QPointF(p2)

    def draw(self, painter: QtGui.QPainter):
        painter.setPen(self.pen)
        painter.drawLine(self.p1, self.p2)

    def contains(self, point: QPointF) -> bool:
        # distance from point to segment small enough?
        line = QtCore.QLineF(self.p1, self.p2)
        dist = line.distanceToPoint(point)
        return dist <= max(6, self.pen.widthF() + 2)

