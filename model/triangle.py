from typing import Tuple

from model.pen import Pen
from model.point import Point
from model.rectangle_shape import RectangleShape


class Triangle(RectangleShape):
    def __init__(self,pen: Pen, p1: Point, p2: Point):
        super().__init__(pen, p1,p2)

    def contains(self, point: Point) -> bool:
        point_center_a, point_left_base_b, point_right_base_c = self.get_vertex()
        area_fun = lambda p1,p2,p3 : 0.5 * abs((p1.x * (p2.y - p3.y)
                                            + p2.x * (p3.y - p1.y)
                                            + p3.x * (p1.y - p2.y)))
        t = area_fun(point_center_a,point_left_base_b,point_right_base_c)
        t1 = area_fun(point,point_left_base_b,point_right_base_c)
        t2 = area_fun(point_center_a,point,point_right_base_c)
        t3 = area_fun(point_center_a,point_left_base_b,point)

        epsilon = 1e-6
        return abs(t - (t1 + t2 + t3)) < epsilon

    def get_vertex(self) -> Tuple[Point,Point,Point]:
        width = self.p2.x - self.p1.x
        point_center_a = Point(self.p1.x + width/2, self.p1.y)
        point_left_base_b = Point(self.p1.x, self.p2.y)
        point_right_base_c = Point(self.p2.x, self.p2.y)
        return point_center_a, point_left_base_b, point_right_base_c