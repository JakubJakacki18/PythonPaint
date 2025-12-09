from math import atan2, degrees
from typing import Callable, Optional

from PyQt6.QtCore import Qt
from mpl_toolkits.mplot3d.art3d import rotate_axes

from model.bezier_curve import BezierCurve
from model.point import Point
from utils.enums.advanced_tools import AdvancedTools
from utils.json_converter import JsonConverter
from view.bezier_curve_dialog import BezierCurveDialog


class BezierCurveDialogPresenter:
    def __init__(self, model: BezierCurve, view: BezierCurveDialog | None):
        self.model = model
        self.view = view
        self.dragging_index: Optional[int] = None
        self.rotate_axis: Optional[Point] = None
        self.start_position: Optional[Point] = None
        self.start_operation: bool = False
        self.current_tool = AdvancedTools.DRAW
        self._last_rotation_angle = None

        self.press_tool_handlers: dict[
            tuple[Qt.MouseButton, AdvancedTools], Callable
        ] = {
            (
                Qt.MouseButton.LeftButton,
                AdvancedTools.DRAW,
            ): self._handle_left_draw_pressed,
            (
                Qt.MouseButton.RightButton,
                AdvancedTools.DRAW,
            ): self._handle_right_draw_pressed,
            (
                Qt.MouseButton.LeftButton,
                AdvancedTools.ROTATE,
            ): self._handle_left_rotate_pressed,
            (
                Qt.MouseButton.RightButton,
                AdvancedTools.ROTATE,
            ): self._handle_right_rotate_pressed,
            (Qt.MouseButton.LeftButton, AdvancedTools.MOVE): self._handle_move_pressed,
            (
                Qt.MouseButton.LeftButton,
                AdvancedTools.SCALE,
            ): self._handle_scale_pressed,
        }
        self.move_tool_handlers: dict[AdvancedTools, Callable] = {
            AdvancedTools.MOVE: self._handle_move_moved,
            AdvancedTools.SCALE: self._handle_scale_moved,
            AdvancedTools.ROTATE: self._handle_rotate_moved,
            AdvancedTools.DRAW: self._handle_draw_moved,
        }

    def get_points(self):
        points = self.model.get_points()
        return points

    def on_tool_changed(self, tool):
        self.current_tool = tool

    def update_bezier_curve(self, points):
        self.model.set_points(points)

    def handle_mouse_press(self, clicked_point: Point, mouse_button: Qt.MouseButton):
        self.press_tool_handlers.get(
            (mouse_button, self.current_tool), lambda *_: None
        )(clicked_point)

    def handle_mouse_release(self):
        self.dragging_index = None
        self.start_position = None
        self.start_operation = False
        self.view.canvasPlaceholder.update()

    def handle_mouse_move(self, current_point: Point):
        self.move_tool_handlers.get(self.current_tool, lambda *_: None)(current_point)
        self.view.update_spin_box_values()
        self.view.canvasPlaceholder.update()

    def save_json_file(self):
        JsonConverter().save_points(self.get_points())

    def load_json_file(self):
        points = JsonConverter().load_points()
        self.model.set_points(points)
        self.view.load_values_from_presenter()

    def _handle_scale_pressed(self, clicked_point: Point):
        self.start_position = clicked_point

    def _handle_move_pressed(self, clicked_point: Point):
        self.start_position = clicked_point

    def _handle_left_rotate_pressed(self, clicked_point: Point):
        self.rotate_axis = clicked_point

    def _handle_left_draw_pressed(self, clicked_point: Point):
        selected_point_index = self.model.find_point(clicked_point)
        if selected_point_index is not None:
            self.dragging_index = selected_point_index
        else:
            self.dragging_index = None

    def _handle_right_draw_pressed(self, clicked_point: Point):
        if len(self.model.points) >= 10:
            return
        self.model.points.append(clicked_point)
        self.view.load_values_from_presenter()

    def _handle_right_rotate_pressed(self, clicked_point: Point):
        self.start_operation = True

    def _handle_move_moved(self, current_point: Point):
        if self.start_position is None:
            return
        translation_vector = Point(
            current_point.x - self.start_position.x,
            current_point.y - self.start_position.y,
        )
        self.model.move_by(translation_vector)
        self.start_position = current_point

    def _handle_scale_moved(self, current_point: Point):
        if self.start_position is None:
            return
        self.model.resize_by(current_point)

    def _handle_rotate_moved(self, current_point: Point):
        if not self.rotate_axis or not self.start_operation:
            return
        angle = degrees(
            atan2(
                current_point.y - self.rotate_axis.y,
                current_point.x - self.rotate_axis.x,
            )
        )
        print(angle)
        if self._last_rotation_angle is None:
            self._last_rotation_angle = angle
            return

        delta_angle = angle - self._last_rotation_angle

        self.model.rotate_by(delta_angle, self.rotate_axis)

        self._last_rotation_angle = angle

    def _handle_draw_moved(self, current_point: Point):
        if self.dragging_index is None:
            return
        self.model.update_value_of(self.dragging_index, current_point)

    def handle_key_press(self, event):
        pass
