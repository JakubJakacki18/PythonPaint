from typing import Tuple

from model.pen import Pen
from model.point import Point
from model.shape import Shape


class Line(Shape):
    def __init__(self, pen : Pen, p1 : Point, p2 : Point):
        super().__init__(pen)
        self.p1 = p1
        self.p2 = p2

    def resize_by(self, point: Point):
        self.p2 = point
