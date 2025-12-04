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

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError(f"Nie można dzielić przez {type(other)}")
        try:
            new_x = self.x / other
            new_y = self.y / other
        except ZeroDivisionError:
            return self
        return Point(new_x, new_y)

    def point_to_dict(self) -> dict:
        return {"x": self.x, "y": self.y}

    @classmethod
    def dict_to_point(cls, dictionary) -> "Point":
        return Point(dictionary["x"], dictionary["y"])
