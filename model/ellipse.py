from typing import Tuple

from model.pen import Pen
from model.point import Point
from model.rectangle import Rectangle
from model.shape import Shape


class Ellipse(Rectangle):
    def __init__(self,pen:Pen, p1 : Point, p2 : Point):
        super().__init__(pen,p1,p2)

    def contains(self, p: Point) -> bool:
        if self.p1 == self.p2:
            return False
        center_point = (self.p1 + self.p2)/2
        cx = center_point.x
        cy = center_point.y
        rx = abs(self.p1.x - cx)
        ry = abs(self.p1.y - cy)

        px = (p.x - cx) / rx
        py = (p.y - cy) / ry
        return px * px + py * py <= 1.0