from model.pen import Pen
from model.point import Point
from model.shape import Shape


class FreeDraw(Shape):
    def __init__(self, pen : Pen, point: Point):
        super().__init__(pen)
        self.points_list = [point]

    def add_point(self, point: Point):
        self.points_list.append(point)