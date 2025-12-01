import io
from functools import partial

from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDialog, QDialogButtonBox
from matplotlib import pyplot as plt

from utils.enums.color_channel import ColorChannel
from view.histogram_dialog_ui import Ui_HistogramDialog


class HistogramDialog(QDialog, Ui_HistogramDialog):

    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self.current_image = None
        self.current_operation = ColorChannel.GRAY

        self.radio_buttons = {
            self.grayButton: ColorChannel.GRAY,
            self.redButton: ColorChannel.RED,
            self.greenButton: ColorChannel.GREEN,
            self.blueButton: ColorChannel.BLUE,
        }
        for radio_button, operation in self.radio_buttons.items():
            print(radio_button.text(), operation)
            radio_button.clicked.connect(
                partial(self.on_radio_button_clicked, operation)
            )

        self.equalizeButton.clicked.connect(self.invoke_equalize_histogram)
        self.extendButton.clicked.connect(self.invoke_extend_histogram)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.update_image
        )

    def set_images(self, image, histogram):
        self.update_edited_image(image)
        self.update_histogram(histogram)

    def invoke_extend_histogram(self):
        self.update_images(self.presenter.extend_histogram)

    def invoke_equalize_histogram(self):
        self.update_images(self.presenter.equalize_histogram)

    def on_radio_button_clicked(self, operation: ColorChannel):
        self.current_operation = operation
        self.update_images(self.presenter.set_channel)

    def update_images(self, function):
        new_image, histogram = function(self.current_operation)
        self.update_edited_image(new_image)
        self.update_histogram(histogram)

    def update_edited_image(self, image):
        self.current_image = image
        pixmap = QPixmap.fromImage(image)
        self.originalImage.setPixmap(pixmap)

    def update_histogram(self, histogram):
        grap_pixmap = self.histogram_to_pixmap(histogram)
        self.histogramGraph.setPixmap(grap_pixmap)

    def histogram_to_pixmap(self, histogram) -> QPixmap:

        color = {
            ColorChannel.RED: "red",
            ColorChannel.GREEN: "green",
            ColorChannel.BLUE: "blue",
        }.get(self.current_operation, "red")

        plt.figure(figsize=(4, 2), dpi=100)
        plt.plot(histogram, color=color)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        qt_image = QImage.fromData(buf.read(), "PNG")
        pixmap = QPixmap.fromImage(qt_image)
        return pixmap

    def get_default_mode(self):
        return self.current_operation

    def update_image(self):
        self.presenter.update_original_image(self.current_image)
