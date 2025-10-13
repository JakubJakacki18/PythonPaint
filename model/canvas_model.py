from model.point import Point
from model.shape import Shape

class CanvasModel:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape : Shape):
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape):
        if shape in self.shapes:
            self.shapes.remove(shape)

    def clear_selection(self):
        for s in self.shapes:
            s.selected = False

    def shape_at(self, p: Point):
        for s in reversed(self.shapes):
            if s.contains(p):
                return s
        return None