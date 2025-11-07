import os

import numpy as np
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QImage

from utils.tools import Tools
from view.main_window_ui import Ui_MainWindow
class View(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.setupUi(self)
        self.presenter = presenter
        self.canvasPlaceholder.presenter = presenter
        self.navFrame.setFixedHeight(self.navFrame.sizeHint().height())
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

        self.actionSave.triggered.connect(lambda: self.save_file())
        self.actionOpen.triggered.connect(lambda: presenter.open())
        self.actionClose.triggered.connect(lambda: presenter.close())

        self.actionExport.triggered.connect(lambda: self.export_file_as())
        self.actionImport.triggered.connect(lambda: self.import_file())

        self.colorButton.clicked.connect(lambda: presenter.set_color())
        self.set_color_button(0,0,0)


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

    def save_file(self):
        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Zapisz rysunek jako obraz",
            "",
            "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)"
        )
        if not filename:
            return
        base, ext = os.path.splitext(filename)
        if not ext:
            if "png" in selected_filter.lower():
                filename += ".png"
            elif "jpg" in selected_filter.lower():
                filename += ".jpg"
            elif "bmp" in selected_filter.lower():
                filename += ".bmp"
        self.presenter.save_canvas(filename)

    def save_pixmap(self, filename: str):
        pixmap = QtGui.QPixmap(self.canvasPlaceholder.size())
        self.canvasPlaceholder.render(pixmap)
        pixmap.save(filename)

    def get_extracted_data_from_pixmap(self):
        pixmap = QtGui.QPixmap(self.canvasPlaceholder.size())
        self.canvasPlaceholder.render(pixmap)
        image = pixmap.toImage().convertToFormat(QtGui.QImage.Format.Format_RGB888)

        width = image.width()
        height = image.height()
        bytes_per_line = image.bytesPerLine()

        ptr = image.bits()
        ptr.setsize(bytes_per_line * height)

        buffer = np.frombuffer(ptr, dtype=np.uint8).reshape((height, bytes_per_line))

        if image.format() in (
                QtGui.QImage.Format.Format_RGB888,
                QtGui.QImage.Format.Format_BGR888
        ):
            channels = 3
            arr = buffer[:, :width * channels].reshape((height, width, channels)).copy()
        else:
            raise ValueError(f"Invalid pixmap format: {image.format()}")
        max_value = 255

        return arr, max_value



    def set_color_button(self,r:int,g:int,b:int):
        q_color = QtGui.QColor(r,g,b)
        self.colorButton.setStyleSheet(f"background-color: {q_color.name()};")

    def export_file_as(self):
        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Eksportuj rysunek jako",
            "",
            "PPM text(*.ppm);;PBM text(*.pbm);;PGM text(*.pgm);;PPM binary(*.ppm);;PBM binary(*.pbm);;PGM binary(*.pgm)"
        )
        if not filename:
            return
        self.presenter.export_file(filename,selected_filter)

    def import_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Importuj rysunek jako","","PPM (*.ppm);;PBM (*.pbm);;PGM (*.pgm)")
        self.presenter.import_file(filename)

    def draw_image(self,pixels,width,height,max_rgb_value):
        image = QImage(pixels,width,height,3 * width, QImage.Format.Format_RGB888)
        self.presenter.add_image(image)
        # self.canvasPlaceholder.set_image(image)
