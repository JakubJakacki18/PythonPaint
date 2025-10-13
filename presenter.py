from unittest import case

from model.ellipse import Ellipse
from model.triangle import Triangle
from model.line import Line
from view.main_window import Ui_MainWindow
from view.view import View
from model.canvas_model import CanvasModel
from model.pen import Pen
from model.point import Point
from model.rectangle import Rectangle
from utils.tools import Tools


class Presenter:
    def __init__(self, model: CanvasModel, view: View ):
        self.model = model
        self.view = view
        self.tool = Tools.NONE
        self.current_pen = Pen()
        self.drawing_shape = None
        self.start_pos = None
        self.dragging = False
        self.selected_shape = None
        self.last_mouse_pos = None

    def set_tool(self, tool: Tools):
        self.tool = tool
        self.drawing_shape = None
        self.model.clear_selection()
        self.selected_shape = None
        self.view.refresh()

    def handle_mouse_press(self, clicked_point : Point):
        self.start_pos = clicked_point
        match self.tool:
            case Tools.FREE_DRAW:
                pass
            case Tools.RECTANGLE:
                self.drawing_shape = Rectangle(self.current_pen,clicked_point,clicked_point)
                self.model.add_shape(self.drawing_shape)
            case Tools.LINE:
                self.drawing_shape = Line(self.current_pen,clicked_point,clicked_point)
                self.model.add_shape(self.drawing_shape)
            case Tools.TRIANGLE:
                self.drawing_shape = Triangle(self.current_pen,clicked_point,clicked_point)
                self.model.add_shape(self.drawing_shape)
            case Tools.ELLIPSE:
                self.drawing_shape = Ellipse(self.current_pen, clicked_point, clicked_point)
                self.model.add_shape(self.drawing_shape)
            case Tools.SELECT | Tools.SCALE:
                self.model.clear_selection()
                shape = self.model.shape_at(clicked_point)
                if shape:
                    shape.selected = True
                    self.selected_shape = shape
                    self.dragging = True
                    self.last_mouse_pos = clicked_point
                else:
                    self.selected_shape = None
            case Tools.NONE | _:
                return
        self.view.refresh()
        pass

    def handle_mouse_release(self, released_point : Point):
        self.drawing_shape = None
        self.start_pos = None
        self.dragging = False
        self.selected_shape = None
        self.view.refresh()


    def handle_mouse_move(self, current_point : Point):
        if self.drawing_shape is not None:
            self.drawing_shape.resize_by(current_point)
        if self.selected_shape is not None and self.dragging:
            translation_vector = Point(current_point.x - self.last_mouse_pos.x,
                                current_point.y - self.last_mouse_pos.y)
            if self.tool == Tools.SELECT:
                self.selected_shape.move_by(translation_vector)
            elif self.tool == Tools.SCALE:
                self.selected_shape.resize_by(current_point)
            else:
                raise Exception("Operation is forbidden")
            self.last_mouse_pos = current_point
        self.view.refresh()


    def get_shapes(self):
        return self.model.shapes
