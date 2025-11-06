from typing import Optional, Any

from model.pen import Pen
from model.point import Point
from model.rectangle_shape import RectangleShape


class Image(RectangleShape):
    def __init__(self,pen: Pen, p1: Point, p2: Optional[Point],image : Any):
        self.image=image
        super().__init__(pen, p1,p2)

    def contains(self, p: Point) -> bool:
        return self.p1.x <= p.x <= self.p1.x+self.image.width() and self.p1.y <= p.y <= self.p1.y+self.image.height()