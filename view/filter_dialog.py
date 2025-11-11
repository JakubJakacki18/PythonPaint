from PyQt6.QtWidgets import QDialog

from view.filter_dialog_ui import Ui_FilterDialog


class FilterDialog(QDialog, Ui_FilterDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
