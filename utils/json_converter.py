import json
from typing import Iterable

from model.point import Point


class JsonConverter:
    @staticmethod
    def save_points(points: Iterable[Point], filename="points.json"):
        data = [p.point_to_dict() for p in points]

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_points(filename="points.json"):
        with open(filename, "r") as f:
            data = json.load(f)
        return [Point.dict_to_point(pair_of_x_and_y) for pair_of_x_and_y in data]
