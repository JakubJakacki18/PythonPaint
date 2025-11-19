from enum import Enum


class ImageFilterOperation(Enum):
    SOBEL_VERTICAL = 0
    SOBEL_HORIZONTAL = 1
    MEDIAN = 2
    SMOOTH = 3
    GAUSS = 4
    HIGH_PASS = 5
    CUSTOM = 6
