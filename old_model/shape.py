from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPointF, QRectF

from model.point import Point


class Shape:
    def __init__(self, pen: QtGui.QPen):
        self.pen = QtGui.QPen(pen)
        self.selected = False

    def draw(self, painter: QtGui.QPainter):
        raise NotImplementedError()

    def contains(self, point: QPointF) -> bool:
        return False

    def bounding_rect(self) -> QRectF:
        return QRectF()

    def move_by(self, point : Point):
        raise NotImplementedError()