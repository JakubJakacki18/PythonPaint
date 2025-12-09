from functools import partial

from PyQt6.QtCore import QSignalBlocker
from PyQt6.QtWidgets import QDialog, QLabel, QSpinBox, QWidget, QGridLayout, QVBoxLayout

from model.point import Point
from utils.enums.advanced_tools import AdvancedTools
from view.bezier_curve_dialog_ui import Ui_BezierCurveDialog


class BezierCurveDialog(QDialog, Ui_BezierCurveDialog):
    def __init__(self, presenter, canvas_class, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self.canvasPlaceholder = canvas_class(self)
        layout = QVBoxLayout(self.canvasFrame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvasPlaceholder)

        self.canvasPlaceholder.presenter = presenter
        self.current_tool = AdvancedTools.DRAW
        self.levelSpinBox.valueChanged.connect(self.on_level_spin_box_changed)
        self.executeButton.clicked.connect(self.execute_transition)

        self.spin_box_x = []
        self.spin_box_y = []
        self.is_all_spinbox_values_known = False
        self.on_level_spin_box_changed()

        self.saveJsonButton.clicked.connect(self.presenter.save_json_file)
        self.loadJsonButton.clicked.connect(self.presenter.load_json_file)

        self.radio_buttons = {
            self.drawButton: AdvancedTools.DRAW,
            self.rotateButton: AdvancedTools.ROTATE,
            self.scaleButton: AdvancedTools.SCALE,
            self.moveButton: AdvancedTools.MOVE,
        }

        for radio_button, tool in self.radio_buttons.items():
            print(radio_button.text(), tool)
            radio_button.clicked.connect(partial(self.on_radio_button_clicked, tool))

    def on_level_spin_box_changed(
        self,
    ):
        new_value = self.levelSpinBox.value()
        old_value = len(self.spin_box_x)

        layout = self.drawedPointsFrame.layout()
        if layout is None:
            layout = QGridLayout(self.drawedPointsFrame)

        if new_value > old_value:
            for row in range(old_value, new_value):
                label_x = QLabel(f"x{row}:")
                spin_x = QSpinBox()
                spin_x.setRange(0, 999999)

                label_y = QLabel(f"y{row}:")
                spin_y = QSpinBox()
                spin_y.setRange(0, 999999)

                layout.addWidget(label_x, row, 0)
                layout.addWidget(spin_x, row, 1)
                layout.addWidget(label_y, row, 2)
                layout.addWidget(spin_y, row, 3)

                self.spin_box_x.append(spin_x)
                self.spin_box_y.append(spin_y)

                spin_x.valueChanged.connect(self.on_spinbox_changed)
                spin_y.valueChanged.connect(self.on_spinbox_changed)

        elif new_value < old_value:
            for row in range(new_value, old_value):
                spin_x = self.spin_box_x.pop()
                spin_y = self.spin_box_y.pop()

                spin_x.deleteLater()
                spin_y.deleteLater()

                item_x_label = layout.itemAtPosition(row, 0)
                item_y_label = layout.itemAtPosition(row, 2)

                if item_x_label:
                    item_x_label.widget().deleteLater()

                if item_y_label:
                    item_y_label.widget().deleteLater()
        if not self.is_all_spinbox_values_known:
            self.on_spinbox_changed()

    def _get_matrix_values(self):
        combined_spin_boxes = zip(self.spin_box_x, self.spin_box_y)
        return [
            (spix_x.value(), spix_y.value()) for spix_x, spix_y in combined_spin_boxes
        ]

    def on_spinbox_changed(self):
        self.presenter.update_bezier_curve(self._get_matrix_values())
        self.canvasPlaceholder.update()

    def update_spin_box_values(self):
        points = self.presenter.get_points()
        for index, point in enumerate(points):
            with (
                QSignalBlocker(self.spin_box_x[index]),
                QSignalBlocker(self.spin_box_y[index]),
            ):
                self.spin_box_x[index].setValue(int(point.x))
                self.spin_box_y[index].setValue(int(point.y))
        self.canvasPlaceholder.update()

    def load_values_from_presenter(self):
        self.is_all_spinbox_values_known = True
        points = self.presenter.get_points()
        self.levelSpinBox.setValue(len(points))
        self.update_spin_box_values()
        self.is_all_spinbox_values_known = False

    def on_radio_button_clicked(self, tool: AdvancedTools):
        self.current_tool = tool
        self.presenter.on_tool_changed(tool)

    def set_rotate_axis_value(self, rotate_x_value: int, rotate_y_value: int):
        self.rotateCoordinatesXSpinBox.setValue(rotate_x_value)
        self.rotateCoordinatesYSpinBox.setValue(rotate_y_value)

    def execute_transition(self):
        offset_x = self.offsetXSpinBox.value()

        if (offset_y := self.offsetYSpinBox.value()) or offset_x:
            self.presenter.move_shape(Point(offset_x, offset_y))

        if (scale_value := self.scaleSpinBox.value()) != 1:
            self.presenter.scale_shape(scale_value)

        rotate_axis = Point(
            self.rotateCoordinatesXSpinBox.value(),
            self.rotateCoordinatesYSpinBox.value(),
        )
        degree = self.degreeSpinBox.value()
        if (rotate_axis.x > 0 or rotate_axis.y > 0) and degree:
            self.presenter.rotate_shape(rotate_axis, degree)

        self.canvasPlaceholder.update()
        self.reset_spin_boxes()

    def reset_spin_boxes(self):
        self.offsetXSpinBox.setValue(0)
        self.offsetYSpinBox.setValue(0)
        self.scaleSpinBox.setValue(1)
        self.degreeSpinBox.setValue(0)
