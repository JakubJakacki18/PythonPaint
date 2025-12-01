from functools import partial

import matplotlib.pyplot as plt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QDialog, QDialogButtonBox
import io

from utils.enums.binary_operation import BinaryOperation
from view.binary_dialog_ui import Ui_BinaryDialog


class BinaryDialog(QDialog, Ui_BinaryDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self.current_image = None
        self.value = 127
        self.current_operation = BinaryOperation.MANUAL

        self.thresholdSlider.valueChanged.connect(self.on_threshold_value_changed)

        self.radio_buttons = {
            self.sauvolaButton: BinaryOperation.SAUVOLA,
            self.phansalkarButton: BinaryOperation.PHANSALKAR,
            self.otsuButton: BinaryOperation.OTSU,
            self.percentButton: BinaryOperation.PERCENT,
            self.entropyButton: BinaryOperation.ENTROPY,
            self.manualButton: BinaryOperation.MANUAL,
            self.iterativeButton: BinaryOperation.ITERATIVE,
            self.nilblackButton: BinaryOperation.NILBLACK,
        }
        for radio_button, operation in self.radio_buttons.items():
            print(radio_button.text(), operation)
            radio_button.clicked.connect(
                partial(self.on_radio_button_clicked, operation)
            )

        self.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.update_image
        )

    def set_images(self, image, histogram):
        self.update_edited_image(image)
        self.update_histogram(histogram)

    def on_radio_button_clicked(self, operation: BinaryOperation):
        self.current_operation = operation
        match operation:
            case BinaryOperation.MANUAL:
                self.thresholdSlider.setVisible(True)
                self.thresholdSlider.setMaximum(255)
                self.thresholdSlider.setValue(127)
            case BinaryOperation.PERCENT:
                self.thresholdSlider.setVisible(True)
                self.thresholdSlider.setMaximum(100)
                self.thresholdSlider.setValue(50)
            case _:
                self.thresholdSlider.setVisible(False)
                pass

        self.update_images(operation)

    def update_images(self, operation):
        self.value = self.thresholdSlider.value()
        print(f"Threshold value: {self.value}")
        new_image, histogram = self.presenter.apply_binarization(operation, self.value)
        self.update_edited_image(new_image)
        self.update_histogram(histogram)

    def on_threshold_value_changed(self):
        self.update_images(self.current_operation)

    def update_edited_image(self, image):
        self.current_image = image
        pixmap = QPixmap.fromImage(image)
        self.originalImage.setPixmap(pixmap)

    def update_histogram(self, histogram):
        grap_pixmap = self.histogram_to_pixmap(histogram)
        self.histogramGraph.setPixmap(grap_pixmap)

    def histogram_to_pixmap(self, histogram) -> QPixmap:
        plt.figure(figsize=(4, 2), dpi=100)
        plt.bar(
            [0, 255], [histogram[0], histogram[255]], color=["blue", "red"], width=10
        )
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        qt_image = QImage.fromData(buf.read(), "PNG")
        pixmap = QPixmap.fromImage(qt_image)
        return pixmap

    def get_default_mode(self):
        return self.current_operation, self.value

    def update_image(self):
        self.presenter.update_original_image(self.current_image)
