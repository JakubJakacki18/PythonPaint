from functools import partial

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QWidget,
    QGridLayout,
)

from utils.enums.morph_operation import MorphOperation
from view.morph_dialog_ui import Ui_MorphDialog


class MorphDialog(QDialog, Ui_MorphDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self.imagePreviewWidget = uic.loadUi("view/image_preview_widget.ui")
        self.imageFrame.layout().addWidget(self.imagePreviewWidget)
        self.current_image = None

        self.radio_buttons = {
            self.dilatationButton: MorphOperation.DILATION,
            self.erosionButton: MorphOperation.EROSION,
            self.hitOrMissButton: MorphOperation.HIT_OR_MISS,
            self.closingButton: MorphOperation.CLOSING,
            self.openingButton: MorphOperation.OPENING,
        }

        self.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.update_original_image
        )

        for radio_button, operation in self.radio_buttons.items():
            print(radio_button.text(), operation)
            radio_button.clicked.connect(
                partial(self.on_radio_button_clicked, operation)
            )

        self.dimensionSpinBox.valueChanged.connect(self.set_dimensions)
        self.doubleSpinBoxes: list[list[QDoubleSpinBox]] = []
        self.set_dimensions()
        self.matrix = None
        self.dimensionFrame.hide()

    def set_images(self, image):
        self.current_image = image
        pixmap = QPixmap.fromImage(image)
        self.imagePreviewWidget.editedImage.setPixmap(pixmap)
        self.imagePreviewWidget.originalImage.setPixmap(pixmap)

    def on_radio_button_clicked(self, operation: MorphOperation):
        # if operation == MorphOperation.CUSTOM:
        #     self.dimensionFrame.show()
        # else:
        #     self.dimensionFrame.hide()

        self.dimensionFrame.show()

        new_image = self.presenter.apply_filter(operation, self.matrix)
        self.update_edited_image(new_image)

    def update_edited_image(self, new_image):
        self.current_image = new_image
        new_pixmap = QPixmap.fromImage(new_image)
        self.imagePreviewWidget.editedImage.setPixmap(new_pixmap)

    def set_dimensions(self):
        dimension = self.dimensionSpinBox.value()

        for child in self.spinBoxGridPlaceholderFrame.findChildren(QDoubleSpinBox):
            child.deleteLater()

        old_layout = self.spinBoxGridPlaceholderFrame.layout()
        if old_layout:
            QWidget().setLayout(old_layout)

        layout = QGridLayout(self.spinBoxGridPlaceholderFrame)

        self.doubleSpinBoxes = [
            [None for _ in range(dimension)] for _ in range(dimension)
        ]

        for row in range(dimension):
            for col in range(dimension):
                spin = QDoubleSpinBox()
                spin.setRange(-255, 255)
                spin.setDecimals(3)
                spin.setValue(0.0)

                spin.valueChanged.connect(self.on_spinbox_changed)
                layout.addWidget(spin, row, col)
                self.doubleSpinBoxes[row][col] = spin

    def on_spinbox_changed(self):
        self.matrix = self._get_matrix_values()

    def _get_matrix_values(self):
        return [[spin.value() for spin in row] for row in self.doubleSpinBoxes]

    def update_original_image(self):
        self.presenter.update_original_image(self.current_image)
        pixmap = QPixmap.fromImage(self.current_image)
        self.imagePreviewWidget.originalImage.setPixmap(pixmap)
