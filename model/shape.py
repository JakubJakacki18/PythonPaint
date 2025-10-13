# model/shape.py
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from model.point import Point
from model.pen import Pen


@dataclass
class Shape:
    pen: Pen
    selected: bool = False
    def contains(self, point: Point) -> bool:
        """Sprawdza, czy punkt znajduje się wewnątrz kształtu."""
        return False
        # raise NotImplementedError("Subklasa musi zaimplementować contains()")

    def resize_by(self, point: Point):
        raise NotImplementedError("Subklasa musi zaimplementować resize_by()")


    def bounding_box(self) -> Tuple[float, float, float, float]:
        """Zwraca prostokąt otaczający (x_min, y_min, x_max, y_max)."""
        raise NotImplementedError("Subklasa musi zaimplementować bounding_box()")

    def move_by(self, point: Point):
        raise NotImplementedError("Subklasa musi zaimplementować move_by()")




