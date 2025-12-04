from math import hypot
from typing import List, Tuple

from model.pen import Pen
from model.point import Point
from model.shape import Shape


class BezierCurve(Shape):
    points: List[Point] = []

    def __init__(self, pen: Pen):
        super().__init__(pen)

    def get_points(self) -> Tuple[Point, ...]:
        return tuple(self.points)

    def set_points(self, points: List[Tuple[int, int]]) -> None:
        self.points = [Point(x, y) for x, y in points]

    def find_point(self, point: Point, tolerance: float = 8.0) -> int | None:
        for i, p in enumerate(self.points):
            if hypot(point.x - p.x, point.y - p.y) <= tolerance:
                return i
        return None

    def update_value_of(self, dragging_index: int, clicked_point: Point):
        self.points[dragging_index] = clicked_point
