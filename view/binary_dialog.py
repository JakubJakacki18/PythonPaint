from functools import partial

import numpy as np
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QDialog
import matplotlib.pyplot as plt
import io

from utils.binary_operation import BinaryOperation
from view.binary_dialog_ui import Ui_BinaryDialog


class BinaryDialog(QDialog, Ui_BinaryDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self.current_image = None
        self.value = 0


        self.radio_buttons = {
            self.sauvolaButton : BinaryOperation.SAUVOLA,
            self.phansalkarButton : BinaryOperation.PHANSALKAR,
            self.otsuButton : BinaryOperation.OTSU,
            self.percentButton : BinaryOperation.PERCENT,
            self.entropyButton : BinaryOperation.ENTROPY,


        }
        for radio_button, operation in self.radio_buttons.items():
            print(radio_button.text(), operation)
            radio_button.clicked.connect(
                partial(self.on_radio_button_clicked, operation)
            )


    def set_images(self, image):
        self.current_image = image
        pixmap = QPixmap.fromImage(image)
        self.originalImage.setPixmap(pixmap)

    def on_radio_button_clicked(self, operation : BinaryOperation):
        new_image = self.presenter.apply_filter(operation, self.value)
        self.update_edited_image(new_image)

    def update_edited_image(self, new_image):
        pass

    def update_histogram(self):
        pass


