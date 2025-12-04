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

    from typing import List, Tuple, Union

    def set_points(self, points: Union[List[Point], List[Tuple[int, int]]]) -> None:
        if not points:
            self.points = []
            return

        if isinstance(points[0], Point):
            self.points = points
        elif isinstance(points[0], tuple):
            self.points = [Point(x, y) for x, y in points]
        else:
            raise TypeError("Unsupported type for set_points")

    def find_point(self, point: Point, tolerance: float = 8.0) -> int | None:
        for i, p in enumerate(self.points):
            if hypot(point.x - p.x, point.y - p.y) <= tolerance:
                return i
        return None

    def update_value_of(self, dragging_index: int, clicked_point: Point):
        self.points[dragging_index] = clicked_point
