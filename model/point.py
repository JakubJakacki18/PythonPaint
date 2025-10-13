from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def __iadd__(self, other):
        if not isinstance(other, Point):
            raise TypeError()
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError()
        return Point(self.x + other.x, self.y + other.y)
