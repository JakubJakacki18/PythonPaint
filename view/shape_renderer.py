from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPen, QColor, QPainter, QPolygonF, QPainterPath, QFont

from model.ellipse import Ellipse
from model.free_draw import FreeDraw
from model.line import Line
from model.pen import Pen
from model.rectangle import Rectangle
from model.text import Text
from model.triangle import Triangle
from utils.point_converter import PointConverter


class ShapeRenderer:
    @staticmethod
    def draw_text(painter: QPainter,pen:Pen,text:Text):
        qt_pen = ShapeRenderer.initialize_pen(pen)
        font = QFont("Arial", 14)
        painter.setFont(font)
        painter.setPen(qt_pen)
        painter.drawText(PointConverter.convert_point_to_qpoint_f(text.p1,)[0],text.text)
        # painter.drawText(QRectF(text.p1.x,
        #                  text.p1.y,
        #                  text.p2.x-text.p1.x,
        #                  text.p2.y-text.p1.y),Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap,text.text)

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
    def draw_free(painter:QPainter, pen:Pen, free_draw : FreeDraw):
        qt_pen = ShapeRenderer.initialize_pen(pen)
        painter.setPen(qt_pen)
        path = QPainterPath()
        q_points = PointConverter.convert_point_to_qpoint_f(*free_draw.points_list)
        if q_points:
            # print(type(q_points[0]))
            path.moveTo(q_points[0])
            for q_point in q_points[1:]:
                path.lineTo(q_point)
        painter.drawPath(path)

    @staticmethod
    def initialize_pen(pen:Pen) -> QPen:
        q_color = QColor(*pen.color)
        qt_pen = QPen(q_color,pen.width,
                      Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap,
                      Qt.PenJoinStyle.RoundJoin)
        return qt_pen