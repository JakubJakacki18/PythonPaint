from model.bezier_curve import BezierCurve
from model.point import Point
from view.bezier_curve_dialog import BezierCurveDialog


class BezierCurveDialogPresenter:
    def __init__(self, model: BezierCurve, view: BezierCurveDialog | None):
        self.model = model
        self.view = view

    def get_points(self):
        points = self.model.get_points()
        return points


    def handle_mouse_press(self, clicked_point: Point):
        pass

    def handle_mouse_release(self):
        pass

    def handle_mouse_move(self, clicked_point: Point):
        pass
