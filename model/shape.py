# model/shape.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from model.point import Point
from model.pen import Pen


@dataclass
class Shape(ABC):
    pen: Pen
    selected: bool = False

    def contains(self, point: Point) -> bool:
        return False

    def resize_by(self, point: Point):
        raise NotImplementedError("Subklasa musi zaimplementować resize_by()")

    def bounding_box(self) -> Tuple[float, float, float, float]:
        raise NotImplementedError("Subklasa musi zaimplementować bounding_box()")

    def move_by(self, point: Point):
        raise NotImplementedError("Subklasa musi zaimplementować move_by()")



