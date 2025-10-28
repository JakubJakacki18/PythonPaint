import copy
from unittest import case

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

from model.color_model import ColorModel
from model.ellipse import Ellipse
from model.free_draw import FreeDraw
from model.text import Text
from model.triangle import Triangle
from model.line import Line
from .dialog_presenter import DialogPresenter
from view.color_dialog import ColorDialog
from view.main_window import View
from model.canvas_model import CanvasModel
from model.pen import Pen
from model.point import Point
from model.rectangle import Rectangle
from utils.tools import Tools


class Presenter:
    def __init__(self, model: CanvasModel, view: View | None,shape_factories):
        self.model = model
        self.view = view
        self.tool = Tools.NONE
        self.shape_factories = shape_factories
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
        if self.tool in self.shape_factories:
            factory = self.shape_factories[self.tool]
            self.drawing_shape = factory(copy.deepcopy(self.current_pen), clicked_point)
            self.model.add_shape(self.drawing_shape)
            self.view.refresh()
            return
        match self.tool:
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
                print(f"Selected tool: {self.tool}")
                return
        self.view.refresh()

    def handle_mouse_release(self):
        if self.tool != Tools.TEXT:
            self.drawing_shape = None
        self.start_pos = None
        self.dragging = False
        self.selected_shape = None
        self.view.refresh()


    def handle_mouse_move(self, current_point : Point):
        if self.drawing_shape is not None and self.tool != Tools.TEXT:
            if self.tool == Tools.FREE_DRAW:
                self.drawing_shape.add_point(current_point)
            else:
                self.drawing_shape.resize_by(current_point)
        if self.selected_shape is not None and self.dragging:
            if self.tool == Tools.SELECT:
                translation_vector = Point(current_point.x - self.last_mouse_pos.x,
                                           current_point.y - self.last_mouse_pos.y)
                self.selected_shape.move_by(translation_vector)
            elif self.tool == Tools.SCALE:
                self.selected_shape.resize_by(current_point)
            else:
                raise Exception("Operation is forbidden")
            self.last_mouse_pos = current_point
        self.view.refresh()

    def handle_key_press(self,event):
        if self.drawing_shape is not None and self.tool == Tools.TEXT:
            if event.key() == Qt.Key.Key_Backspace:
                self.drawing_shape.delete_last_character()
            elif event.text().isprintable():
                self.drawing_shape.set_text(event.text())
        self.view.refresh()


    def get_shapes(self):
        return self.model.shapes

    def save_canvas(self, filename: str):
        self.view.save_pixmap(filename)

    def close(self):
        pass

    def open(self):
        pass

    def set_color(self):
        dialog_presenter = DialogPresenter(ColorModel(*self.current_pen.color),None)
        dialog = ColorDialog(dialog_presenter)
        dialog_presenter.view = dialog
        dialog.update_from_rgb()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            color = dialog_presenter.model
            print(color)
            self.current_pen = Pen((color.r,color.g,color.b),2)
            self.view.colorButton.setStyleSheet(f"background-color: rgb({color.r}, {color.g}, {color.b});")