from PyQt6 import QtWidgets

from utils.tools import Tools
from view.main_window import Ui_MainWindow
class View(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.setupUi(self)
        self.presenter = presenter
        self.canvasPlaceholder.presenter = presenter
        self.secondaryBarFrame.hide()

        self.drawButton.clicked.connect(lambda: self.toggle_secondary_bar_frame(True))
        self.scaleButton.clicked.connect(lambda: self.toggle_scale_button())
        self.moveButton.clicked.connect(lambda: self.toggle_move_button())
        self.textButton.clicked.connect(lambda: self.toggle_text_button())

        self.freeDrawButton.clicked.connect(lambda: presenter.set_tool(Tools.FREE_DRAW))
        self.lineDrawButton.clicked.connect(lambda: presenter.set_tool(Tools.LINE))
        self.triangleDrawButton.clicked.connect(lambda: presenter.set_tool(Tools.TRIANGLE))
        self.ellipseDrawButton.clicked.connect(lambda: presenter.set_tool(Tools.ELLIPSE))
        self.rectangleDrawButton.clicked.connect(lambda: presenter.set_tool(Tools.RECTANGLE))


    def refresh(self):
        self.canvasPlaceholder.update()

    def toggle_secondary_bar_frame(self, is_visible : bool):
        self.secondaryBarFrame.setVisible(is_visible)

    def toggle_move_button(self):
        self.toggle_secondary_bar_frame(False)
        self.presenter.set_tool(Tools.SELECT)

    def toggle_scale_button(self):
        self.toggle_secondary_bar_frame(False)
        self.presenter.set_tool(Tools.SCALE)

    def toggle_text_button(self):
        self.toggle_secondary_bar_frame(False)
        self.presenter.set_tool(Tools.TEXT)