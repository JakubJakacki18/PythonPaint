from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen, QColor, QPainter, QPolygonF

from model.ellipse import Ellipse
from model.line import Line
from model.pen import Pen
from model.rectangle import Rectangle
from model.triangle import Triangle


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
    def draw_triangle(painter : QPainter, pen:Pen, triangle: Triangle):
        qt_pen = ShapeRenderer.initialize_pen(pen)
        painter.setPen(qt_pen)
        a_vertex,b_vertex,c_vertex = triangle.get_vertex()
        polygon = QPolygonF([
            QPointF(int(a_vertex.x),int(a_vertex.y)),
            QPointF(int(b_vertex.x),int(b_vertex.y)),
            QPointF(int(c_vertex.x),int(c_vertex.y)),
        ])
        painter.drawPolygon(polygon)

    @staticmethod
    def draw_line(painter : QPainter, pen:Pen, line: Line):
        qt_pen = ShapeRenderer.initialize_pen(pen)
        painter.setPen(qt_pen)
        # print("Line: ",int(line.p1.x),int(line.p1.y),int(line.p2.x - line.p1.x),int(line.p2.y - line.p1.y))
        painter.drawLine(QPointF(int(line.p1.x),int(line.p1.y)),
                         QPointF(int(line.p2.x),int(line.p2.y)))
    @staticmethod
    def initialize_pen(pen:Pen) -> QPen:
        q_color = QColor(*pen.color)
        qt_pen = QPen(q_color,pen.width,
                      Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap,
                      Qt.PenJoinStyle.RoundJoin)
        return qt_pen