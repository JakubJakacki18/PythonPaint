from PyQt6.QtWidgets import QDialog, QLabel, QSpinBox, QWidget, QGridLayout

from view.bezier_curve_dialog_ui import Ui_BezierCurveDialog


class BezierCurveDialog(QDialog, Ui_BezierCurveDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self.canvasPlaceholder.presenter = presenter

        self.levelSpinBox.valueChanged.connect(self.on_level_spin_box_changed)

        self.spin_box_x = []
        self.spin_box_y = []
        self.is_loading_from_json = False
        self.on_level_spin_box_changed()

        self.saveJsonButton.clicked.connect(self.presenter.save_json_file)
        self.loadJsonButton.clicked.connect(self.presenter.load_json_file)

    #
    # def on_level_spin_box_changed(self):
    #     current_value = self.levelSpinBox.value()
    #
    #
    #     for child in self.drawedPointsFrame.findChildren(QWidget):
    #         child.deleteLater()
    #
    #
    #
    #     old_layout = self.drawedPointsFrame.layout()
    #     if old_layout:
    #         QWidget().setLayout(old_layout)
    #
    #     layout = QGridLayout(self.drawedPointsFrame)
    #
    #
    #     for row in range(current_value):
    #         label_x = QLabel(f"x{row}: ")
    #
    #         spin_x = QSpinBox()
    #         spin_x.setRange(0, 999999)
    #         spin_x.setSingleStep(1)
    #         self.spin_box_x.append(spin_x)
    #
    #         label_y = QLabel(f"y{row}: ")
    #
    #         spin_y = QSpinBox()
    #         spin_y.setRange(0, 999999)
    #         spin_y.setSingleStep(1)
    #         self.spin_box_y.append(spin_y)
    #
    #         layout.addWidget(label_x, row, 0)
    #         layout.addWidget(spin_x, row, 1)
    #         layout.addWidget(label_y, row, 2)
    #         layout.addWidget(spin_y, row, 3)

    def on_level_spin_box_changed(self):
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
        if not self.is_loading_from_json:
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
            self.spin_box_x[index].setValue(int(point.x))
            self.spin_box_y[index].setValue(int(point.y))
        self.canvasPlaceholder.update()

    def on_load_json_file(self):
        self.is_loading_from_json = True
        points = self.presenter.get_points()
        self.levelSpinBox.setValue(len(points))
        self.update_spin_box_values()
        self.is_loading_from_json = False
