from math import hypot
from typing import List, Tuple

from model.pen import Pen
from model.point import Point
from model.shape import Shape
from typing import List, Tuple, Union


class BezierCurve(Shape):
    points: List[Point] = []

    def __init__(self, pen: Pen):
        super().__init__(pen)

    def get_points(self) -> Tuple[Point, ...]:
        return tuple(self.points)

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

    def contains(self, point: Point) -> bool:
        x_min, y_min, x_max, y_max = self._calculate_min_max_values()
        return x_min <= point.x <= x_max and y_min <= point.y <= y_max

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self._calculate_min_max_values()

    def _calculate_min_max_values(self):
        return (
            min(p.x for p in self.points),
            min(p.y for p in self.points),
            max(p.x for p in self.points),
            max(p.y for p in self.points),
        )

    def move_by(self, point: Point):
        for p in self.points:
            p += point

    def resize_by(self, point: Point):
        pass

    def rotate_by(self, angle: float, rotate_axis: Point):
        """Rotate all control points around the curve's center by the given angle"""
        if not self.points:
            return

        import math

        # Convert angle to radians
        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        # Rotate each point around the center
        rotated_points = []
        for point in self.points:
            # Translate point to origin
            x = point.x - rotate_axis.x
            y = point.y - rotate_axis.y

            # Apply rotation matrix
            new_x = x * cos_angle - y * sin_angle
            new_y = x * sin_angle + y * cos_angle

            # Translate back
            new_x += rotate_axis.x
            new_y += rotate_axis.y

            rotated_points.append(Point(new_x, new_y))

        # Update the points
        self.points = rotated_points
