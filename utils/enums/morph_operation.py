from enum import Enum


class MorphOperation(Enum):
    EROSION = 0
    DILATION = 1
    CLOSING = 2
    OPENING = 3
    HIT_OR_MISS = 4
    THINNING = 5
    THICKENING = 6
