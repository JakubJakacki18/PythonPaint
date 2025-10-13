from typing import Tuple

from model.pen import Pen
from model.point import Point
from model.shape import Shape


class Rectangle(Shape):
    def __init__(self,pen: Pen, p1: Point, p2: Point):
        super().__init__(pen)
        self.p1 = p1
        self.p2 = p2

    def contains(self, p: Point) -> bool:
        if self.p1.x <= p.x <= self.p2.x and self.p1.y <= p.y <= self.p2.y:
            return True
        return False

    def move_by(self, point: Point):
        self.p1 = Point(self.p1.x + point.x, self.p1.y + point.y)
        self.p2 = Point(self.p2.x + point.y, self.p2.y + point.y)

    def resize_by(self, point: Point):
        self.p2 = point

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self.p1.x, self.p1.y, self.p2.x, self.p2.y