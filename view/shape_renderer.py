from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor, QPainter

from model.ellipse import Ellipse
from model.pen import Pen
from model.rectangle import Rectangle


class ShapeRenderer:
    @staticmethod
    def draw_rectangle(painter : QPainter, pen:Pen, rect:Rectangle):
        qt_pen = ShapeRenderer.initialize_pen(pen)
        painter.setPen(qt_pen)
        painter.drawRect(int(rect.p1.x),
                         int(rect.p1.y),
                         int(rect.p2.x-rect.p1.x),
                         int(rect.p2.y-rect.p1.y))

    @staticmethod
    def draw_ellipse(painter : QPainter, pen:Pen, ellipse: Ellipse):
        qt_pen = ShapeRenderer.initialize_pen(pen)
        painter.setPen(qt_pen)
        painter.drawEllipse(int(ellipse.p1.x),
                         int(ellipse.p1.y),
                         int(ellipse.p2.x - ellipse.p1.x),
                         int(ellipse.p2.y - ellipse.p1.y))
    @staticmethod
    def initialize_pen(pen:Pen) -> QPen:
        q_color = QColor(*pen.color)
        qt_pen = QPen(q_color,pen.width,
                      Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap,
                      Qt.PenJoinStyle.RoundJoin)
        return qt_pen