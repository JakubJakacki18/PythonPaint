from typing import List, Tuple

from model.pen import Pen
from model.point import Point
from model.shape import Shape


class BezierCurve(Shape):
    points: List[Point]

    def __init__(self, pen: Pen):
        super().__init__(pen)

    def get_points(self) -> Tuple[Point,...]:
        return tuple(self.points)
