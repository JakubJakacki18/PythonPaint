import asyncio
import copy
import os
from unittest import case

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

from model.color_model import ColorModel
from model.ellipse import Ellipse
from model.free_draw import FreeDraw
from model.image import Image
from model.text import Text
from model.triangle import Triangle
from model.line import Line
from utils.commands import (
    InvokerQueue,
    ImportCommand,
    ExportCommand,
    AsyncLoopThread,
    OpenFileCommand,
)
from utils.pnm_importer import PnmImporter, PnmFormat
from view.filter_dialog import FilterDialog
from view.rgb_transformation_dialog import RgbTransformationDialog
from .color_picker_dialog_presenter import ColorPickerDialogPresenter
from view.color_dialog import ColorDialog
from view.main_window import View
from model.canvas_model import CanvasModel
from model.pen import Pen
from model.point import Point
from model.rectangle import Rectangle
from utils.tools import Tools
from .filter_dialog_presenter import FilterDialogPresenter
from .rgb_transformation_dialog_presenter import RgbTransformationDialogPresenter


class Presenter:
    def __init__(self, model: CanvasModel, view: View | None, shape_factories):
        self.model = model
        self.view = view
        self.tool = Tools.NONE
        self.shape_factories = shape_factories
        self.current_pen = Pen()
        self.width = 2
        self.drawing_shape = None
        self.start_pos = None
        self.dragging = False
        self.selected_shape = None
        self.last_mouse_pos = None
        self.command_queue = InvokerQueue()
        self.loop = AsyncLoopThread()

    def set_tool(self, tool: Tools):
        self.tool = tool
        self.drawing_shape = None
        self.model.clear_selection()
        self.selected_shape = None
        self.view.refresh()

    def handle_mouse_press(self, clicked_point: Point):
        self.start_pos = clicked_point
        if self.tool in self.shape_factories:
            factory = self.shape_factories[self.tool]
            self.drawing_shape = factory(self.current_pen, clicked_point)
            self.model.add_shape(self.drawing_shape)
            self.view.refresh()
            return
        match self.tool:
            case Tools.MOVE | Tools.SCALE:
                self.model.clear_selection()
                shape = self.model.shape_at(clicked_point)
                if shape:
                    self.view.toggle_photo_edit_options_enabled(False)
                    shape.selected = True
                    self.selected_shape = shape
                    self.dragging = True
                    self.last_mouse_pos = clicked_point
                else:
                    self.view.toggle_photo_edit_options_enabled(False)
                    self.selected_shape = None
            case Tools.SELECT:
                shape = self.model.shape_at(clicked_point)
                if shape:
                    shape.selected = True
                    self.selected_shape = shape
                    self.view.toggle_photo_edit_options_enabled(
                        isinstance(shape, Image)
                    )
                else:
                    self.selected_shape = None
                    self.view.toggle_photo_edit_options_enabled(False)
            case Tools.NONE | _:
                print(f"Selected tool: {self.tool}")
                return
        self.view.refresh()

    def handle_mouse_release(self):
        if self.tool == Tools.SELECT:
            return
        if self.tool != Tools.TEXT:
            self.drawing_shape = None
        self.start_pos = None
        self.dragging = False
        self.selected_shape = None
        self.view.refresh()

    def handle_mouse_move(self, current_point: Point):
        if self.drawing_shape is not None and self.tool != Tools.TEXT:
            if self.tool == Tools.FREE_DRAW:
                self.drawing_shape.add_point(current_point)
            else:
                self.drawing_shape.resize_by(current_point)
        if self.selected_shape is not None and self.dragging:
            if self.tool == Tools.MOVE:
                translation_vector = Point(
                    current_point.x - self.last_mouse_pos.x,
                    current_point.y - self.last_mouse_pos.y,
                )
                self.selected_shape.move_by(translation_vector)
            elif self.tool == Tools.SCALE:
                self.selected_shape.resize_by(current_point)
            else:
                raise Exception("Operation is forbidden")
            self.last_mouse_pos = current_point
        self.view.refresh()

    def handle_key_press(self, event):
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
        dialog_presenter = ColorPickerDialogPresenter(
            ColorModel(*self.current_pen.color), None
        )
        dialog = ColorDialog(dialog_presenter)
        dialog_presenter.view = dialog
        dialog.update_from_rgb()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            color = dialog_presenter.model
            self.current_pen = Pen((color.r, color.g, color.b), self.width)
            self.view.set_color_button(color.r, color.g, color.b)

    def filter_image(self):
        filter_presenter = FilterDialogPresenter(self.selected_shape, None)
        dialog = FilterDialog(filter_presenter)
        filter_presenter.view = dialog
        filter_presenter.init_images()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass

    def rgb_transformation_image(self):
        rgb_transformation_presenter = RgbTransformationDialogPresenter(
            self.selected_shape, None
        )
        dialog = RgbTransformationDialog(rgb_transformation_presenter)
        rgb_transformation_presenter.view = dialog
        rgb_transformation_presenter.init_images()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass

    def export_file(self, filename, selected_filter):
        if not filename:
            return
        base, ext = os.path.splitext(filename)
        selected_filter_lower = selected_filter.lower()

        if "pbm" in selected_filter_lower:
            new_ext = ".pbm"
        elif "ppm" in selected_filter_lower:
            new_ext = ".ppm"
        elif "pgm" in selected_filter_lower:
            new_ext = ".pgm"
        else:
            raise ValueError("Filter was not recognized")

        if not ext:
            ext = new_ext
            filename += ext
        elif new_ext != ext:
            raise ValueError("File extension does not match")

        if "text" in selected_filter_lower:
            mode = "text"
        elif "binary" in selected_filter_lower:
            mode = "binary"
        else:
            raise ValueError("Nie przekazano trybu exportu")
        mode_function = lambda p_text, p_binary: p_text if mode == "text" else p_binary
        match ext:
            case ".pbm":
                algorithm = mode_function(PnmFormat.PBM_TEXT, PnmFormat.PBM_BINARY)
            case ".ppm":
                algorithm = mode_function(PnmFormat.PPM_TEXT, PnmFormat.PPM_BINARY)
            case ".pgm":
                algorithm = mode_function(PnmFormat.PGM_TEXT, PnmFormat.PGM_BINARY)
            case _:
                raise ValueError("File extension does not match")
        arr, max_value = self.view.get_extracted_data_from_pixmap()

        self.loop.run_coroutine(
            self.command_queue.add_command(
                ExportCommand(filename, algorithm, arr, max_value)
            )
        )

    def open_file(self, filename: str):
        if not filename:
            return
        self.loop.run_coroutine(
            self.command_queue.add_command(OpenFileCommand(filename, self))
        )

    def import_file(self, filename: str):
        if not filename:
            return
        self.loop.run_coroutine(
            self.command_queue.add_command(ImportCommand(filename, self))
        )

    def add_image(self, image):
        image = Image(self.current_pen, Point(0, 0), None, image)
        self.model.add_shape(image)
        self.view.refresh()
