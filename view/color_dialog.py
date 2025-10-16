from PyQt6.QtWidgets import QDialog
from view.color_window_ui import Ui_ColorWindow

class ColorDialog(QDialog, Ui_ColorWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
