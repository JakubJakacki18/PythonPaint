from enum import Enum

class PnmFormat(Enum):
    PBM_TEXT = "P1"
    PGM_TEXT = "P2"
    PPM_TEXT = "P3"
    PBM_BINARY = "P4"
    PGM_BINARY = "P5"
    PPM_BINARY = "P6"