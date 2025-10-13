from old_model.shape import Shape
from PyQt6.QtCore import QPointF


class CanvasModel:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape):
        if shape in self.shapes:
            self.shapes.remove(shape)

    def clear_selection(self):
        for s in self.shapes:
            s.selected = False

    def shape_at(self, point: QPointF):
        # last shapes are on top -> iterate reversed
        for s in reversed(self.shapes):
            if s.contains(point):
                return s
        return None