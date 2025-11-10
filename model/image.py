from typing import Optional, Any

#
# from PyQt6.QtCore import Qt

from model.pen import Pen
from model.point import Point
from model.rectangle_shape import RectangleShape


class Image(RectangleShape):
    def __init__(self, pen: Pen, p1: Point, p2: Optional[Point], image: Any):
        self.image = image
        self.p2 = Point(p1.x + self.image.width(), p1.y + self.image.height())
        super().__init__(pen, p1, self.p2)

    def contains(self, p: Point) -> bool:
        return (
            self.p1.x <= p.x <= self.p1.x + self.image.width()
            and self.p1.y <= p.y <= self.p1.y + self.image.height()
        )

    # def resize_by(self, point: Point):
    #     self.p2 = point
    #     self.image = self.image.scaled(
    #         int(self.p2.x - self.p1.x),
    #         int(self.p2.y - self.p1.y),
    #         Qt.AspectRatioMode.KeepAspectRatio,
    #         Qt.TransformationMode.SmoothTransformation,
    #     )
