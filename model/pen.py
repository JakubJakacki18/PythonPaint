from dataclasses import dataclass
from typing import Tuple


@dataclass
class Pen:
    color: Tuple[int, int, int] = (0, 0, 0)  # RGB
    width: float = 2.0
