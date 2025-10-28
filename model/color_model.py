from dataclasses import dataclass
from typing import Tuple


@dataclass
class ColorModel:
    r: int
    g: int
    b: int

    def to_float(self) -> Tuple[float, float, float]:
        return float(self.r / 255), float(self.g / 255), float(self.b / 255)

    def update_from_int_tuple(self, int_tuple: Tuple[int, int, int]) -> None:
        if len(int_tuple) ==3:
            self.r, self.g, self.b = int_tuple
        else:
            self.r, self.g, self.b, _= int_tuple


    def update_from_float_tuple(self, int_tuple: Tuple[float,float,float]) -> None:
        self.r, self.g, self.b = int(int_tuple[0]*255), int(int_tuple[1]*255), int(int_tuple[2]*255)