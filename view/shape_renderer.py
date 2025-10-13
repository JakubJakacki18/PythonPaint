from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor, QPainter

from model.pen import Pen
from model.rectangle import Rectangle


class ShapeRenderer:
    @staticmethod
    def draw_rectangle(painter : QPainter, pen:Pen, rect:Rectangle):
        q_color = QColor(*pen.color)
        qt_pen = QPen(q_color,pen.width,
                      Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap,
                      Qt.PenJoinStyle.RoundJoin)
        painter.setPen(qt_pen)
        painter.drawRect(int(rect.p1.x),
                         int(rect.p1.y),
                         int(rect.p2.x-rect.p1.x),
                         int(rect.p2.y-rect.p1.y))
        # if self.selected:
        #     painter.setPen(QtGui.QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
        #     painter.drawRect(self.bounding_rect())
        pass
