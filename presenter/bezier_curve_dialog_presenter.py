from model.bezier_curve import BezierCurve
from model.point import Point
from utils.json_converter import JsonConverter
from view.bezier_curve_dialog import BezierCurveDialog


class BezierCurveDialogPresenter:
    def __init__(self, model: BezierCurve, view: BezierCurveDialog | None):
        self.model = model
        self.view = view
        self.dragging_index = None

    def get_points(self):
        points = self.model.get_points()
        return points

    def update_bezier_curve(self, points):
        self.model.set_points(points)

    def handle_mouse_press(self, clicked_point: Point):
        selected_point_index = self.model.find_point(clicked_point)

        if selected_point_index is not None:
            self.dragging_index = selected_point_index
        else:
            self.dragging_index = None

    def handle_mouse_release(self):
        self.dragging_index = None
        self.view.canvasPlaceholder.update()

    def handle_mouse_move(self, clicked_point: Point):
        if self.dragging_index is None:
            return
        self.model.update_value_of(self.dragging_index, clicked_point)
        self.view.update_spin_box_values()
        self.view.canvasPlaceholder.update()

    def save_json_file(self):
        JsonConverter().save_points(self.get_points())

    def load_json_file(self):
        points = JsonConverter().load_points()
        self.model.set_points(points)
        self.view.on_load_json_file()
