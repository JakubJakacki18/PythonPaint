from model.bezier_curve import BezierCurve
from view.bezier_curve_dialog import BezierCurveDialog


class BezierCurveDialogPresenter:
    def __init__(self, model: BezierCurve, view: BezierCurveDialog | None):
        self.model = model
        self.view = view
