from PyQt6.QtWidgets import QDialog, QLabel, QSpinBox

from view.bezier_curve_dialog_ui import Ui_BezierCurveDialog


class BezierCurveDialog(QDialog, Ui_BezierCurveDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter

        self.levelSpinBox.valueChanged.connect()

        self.spin_box_x = []
        self.spin_box_y = []

        self.on_level_spin_box_changed()

    def on_level_spin_box_changed(self):
        current_value = self.levelSpinBox.value()

        for child in self.drawedPointsFrame.findChildren():
            child.deleteLater()

        for row in range(current_value):
            label_x = QLabel(f"x{row}: ")

            spin_x = QSpinBox()
            spin_x.setRange(0, 999999)
            spin_x.setSingleStep(1)
            self.spin_box_x.append(spin_x)

            label_y = QLabel(f"y{row}: ")

            spin_y = QSpinBox()
            spin_y.setRange(0, 999999)
            spin_y.setSingleStep(1)
            self.spin_box_y.append(spin_y)
