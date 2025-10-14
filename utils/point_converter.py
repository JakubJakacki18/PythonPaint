from typing import Tuple, List

from PyQt6.QtCore import QPoint, QPointF

from model.point import Point


class PointConverter:
    @staticmethod
    def convert_point_to_qpoint(*points : Point) -> list[QPoint]:
        return [QPoint(int(point.x),int(point.y)) for point in points]

    @staticmethod
    def convert_point_to_qpoint_f(*points : Point) -> list[QPointF]:
        return [QPointF(point.x,point.y) for point in points]

