from abc import ABC, abstractmethod
from typing import Tuple

from model.pen import Pen
from model.point import Point
from model.shape import Shape


class RectangleShape(Shape):
    def __init__(self,pen: Pen, p1: Point, p2: Point):
        super().__init__(pen)
        self.p1 = p1
        self.p2 = p2

    @abstractmethod
    def contains(self, point: Point) -> bool:
        pass

    def move_by(self, translation_vector: Point):
        self.p1 += translation_vector
        self.p2 += translation_vector

    def resize_by(self, point: Point):
        self.p2 = point

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self.p1.x, self.p1.y, self.p2.x, self.p2.y