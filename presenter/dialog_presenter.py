from PyQt6.QtGui import QColor

from model.color_model import ColorModel
from view.color_dialog import ColorDialog


class DialogPresenter:
    def __init__(self, model : ColorModel, view : ColorDialog):
        self.model = model
        self.view = view
        self.dialog_color= None


    def on_color_picked(self, rgb_tuple):
        self.model.update_from_int_tuple(rgb_tuple)
        # self.view.colorLabel.setColor(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        self.view.colorLabel.setStyleSheet(
            f"background-color: rgb({rgb_tuple[0]}, {rgb_tuple[1]}, {rgb_tuple[2]});"
        )
        # self.update_preview()

    def on_ok(self):
        # commit selection and close dialog with accepted
        # self.view.selected_color = self.model.to_qcolor()
        self.view.accept()

    def on_cancel(self):
        self.view.selected_color = None
        self.view.reject()

    def on_color_picked_float(self, rgb_tuple):
        self.model.update_from_float_tuple(rgb_tuple)
        # self.view.colorLabel.setColor(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        self.view.colorLabel.setStyleSheet(
            f"background-color: rgb({self.model.r}, {self.model.g}, {self.model.b});"
        )
        self.view.init_color(self.model.r,self.model.g,self.model.b)




#
# class ColorPickerPresenter:
#     def __init__(self, model: ColorModel, view_dialog):
#         self.model = model
#         self.view = view_dialog
#
#         # connect view signals
#         self.view.cubeWidget.colorPicked.connect(self.on_color_picked)
#         self.view.coneWidget.colorPicked.connect(self.on_color_picked)
#         self.view.okButton.clicked.connect(self.on_ok)
#         self.view.cancelButton.clicked.connect(self.on_cancel)
#
        # initial sync
        # self.update_preview()



    # def update_preview(self):
    #     q = QColor.model
    #     self.view.preview_label.setPixmap(self._color_pixmap(q, 64, 64))


    # @staticmethod
    # def _color_pixmap(qcolor: QColor, w, h):
    #     img = QImage(w, h, QImage.Format.Format_RGB32)
    #     img.fill(qcolor)
    #     return QPixmap.fromImage(img)
