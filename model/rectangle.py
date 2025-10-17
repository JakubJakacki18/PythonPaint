from typing import Tuple

from model.pen import Pen
from model.point import Point
from model.rectangle_shape import RectangleShape
from model.shape import Shape


class Rectangle(RectangleShape):
    def __init__(self,pen: Pen, p1: Point, p2: Point):
        super().__init__(pen, p1,p2)

    def contains(self, p: Point) -> bool:
        if self.p1.x <= p.x <= self.p2.x and self.p1.y <= p.y <= self.p2.y:
            return True
        return False