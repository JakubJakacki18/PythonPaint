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
        x_min, y_min, x_max, y_max = self._calculate_min_max_values()

        current_width = x_max - x_min
        current_height = y_max - y_min

        if current_width == 0 and current_height == 0:
            return

        new_width = point.x - x_min
        new_height = point.y - y_min

        scale_x = new_width / current_width if current_width != 0 else 1
        scale_y = new_height / current_height if current_height != 0 else 1

        resized_points = []
        for p in self.points:

            resized_points.append(
                BezierCurve._scaling_of_point(p, x_min, y_min, scale_x, scale_y)
            )
        self.points = resized_points

    @staticmethod
    def _scaling_of_point(
        point: Point, x: float, y: float, scale_x: float, scale_y: float
    ) -> Point:
        dx = point.x - x
        dy = point.y - y

        new_x = x + dx * scale_x
        new_y = y + dy * scale_y
        return Point(new_x, new_y)

    def scale_by(self, scale_factor: float):
        if scale_factor == 0:
            return
        x_min, y_min, x_max, y_max = self._calculate_min_max_values()
        scaled_points = []
        for p in self.points:
            scaled_points.append(
                BezierCurve._scaling_of_point(
                    p, x_min, y_min, scale_factor, scale_factor
                )
            )
        self.points = scaled_points

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
