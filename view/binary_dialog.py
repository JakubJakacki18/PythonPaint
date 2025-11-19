from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog

from view.binary_dialog_ui import Ui_BinaryDialog


class BinaryDialog(QDialog, Ui_BinaryDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self.current_image = None

    def set_images(self, image):
        self.current_image = image
        pixmap = QPixmap.fromImage(image)
        # self.imagePreviewWidget.editedImage.setPixmap(pixmap)
        # self.imagePreviewWidget.originalImage.setPixmap(pixmap)
