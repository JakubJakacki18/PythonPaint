from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt, QPointF, QRectF
from old_model.shape import Shape

class EllipseShape(Shape):
    def __init__(self, rect: QRectF, pen: QtGui.QPen):
        super().__init__(pen)
        self.rect = QRectF(rect)

    def draw(self, painter: QtGui.QPainter):
        painter.setPen(self.pen)
        painter.drawEllipse(self.rect)
        if self.selected:
            painter.setPen(QtGui.QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
            painter.drawRect(self.bounding_rect())

    def contains(self, point: QPointF) -> bool:
        # normalize to unit circle test
        r = self.rect
        if r.width() == 0 or r.height() == 0:
            return False
        cx = r.center().x()
        cy = r.center().y()
        rx = r.width() / 2
        ry = r.height() / 2
        px = (point.x() - cx) / rx
        py = (point.y() - cy) / ry
        return px * px + py * py <= 1.0

    def bounding_rect(self) -> QRectF:
        return self.rect

    def move_by(self, dx: float, dy: float):
        self.rect.translate(dx, dy)
