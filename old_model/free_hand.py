from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPointF, QRectF
from old_model.shape import Shape

class Freehand:
    def __init__(self, path: QtGui.QPainterPath, pen: QtGui.QPen):
        super().__init__(pen)
        self.path = QtGui.QPainterPath(path)

    def draw(self, painter: QtGui.QPainter):
        painter.setPen(self.pen)
        painter.drawPath(self.path)


    # def contains(self, point: QPointF) -> bool:
    #     stroker = QtGui.QPainterPathStroker()
    #     stroker.setWidth(max(6, self.pen.widthF() + 2))
    #     stroked = stroker.createStroke(self.path)
    #     return stroked.contains(point)
    #
    # def bounding_rect(self) -> QRectF:
    #     return self.path.boundingRect()
    #
    # def move_by(self, dx: float, dy: float):
    #     tr = QtGui.QTransform()
    #     tr.translate(dx, dy)
    #     self.path = tr.map(self.path)