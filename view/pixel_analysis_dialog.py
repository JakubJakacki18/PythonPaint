from typing import Tuple, Optional

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QSizePolicy

from view.pixel_analysis_dialog_ui import Ui_PixelAnalysisDialog


class PixelAnalysisDialog(QDialog, Ui_PixelAnalysisDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = presenter
        self._init_sliders()
        self.current_image = None
        self.current_pixmap = None
        self.hue_value: Tuple[int, int] = (0, 180)
        self.saturation_value: Tuple[int, int] = (0, 255)
        self.brightness_value: Tuple[int, int] = (0, 255)

        self.image.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image.setMinimumSize(1, 1)
        self.image.setScaledContents(False)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _init_sliders(self):

        self.hueSlider.setOrientation(Qt.Orientation.Horizontal)
        self.hueSlider.setMinimum(0)
        self.hueSlider.setMaximum(180)
        self.hueSlider.setValue((0, 180))

        self.brightnessSlider.setOrientation(Qt.Orientation.Horizontal)
        self.brightnessSlider.setMinimum(0)
        self.brightnessSlider.setMaximum(255)
        self.brightnessSlider.setValue((0, 255))

        self.saturationSlider.setOrientation(Qt.Orientation.Horizontal)
        self.saturationSlider.setMinimum(0)
        self.saturationSlider.setMaximum(255)
        self.saturationSlider.setValue((0, 255))

        self.hueSlider.valueChanged.connect(self.update_hue)
        self.saturationSlider.valueChanged.connect(self.update_saturation)
        self.brightnessSlider.valueChanged.connect(self.update_brightness)

    def set_image(self, image):
        self.current_image = image
        pixmap = QPixmap.fromImage(image)
        self.current_pixmap = pixmap
        self.set_pixmap(pixmap)

    def set_pixmap(self, pixmap):
        size = self.frame_2.size()
        pixmap = pixmap.scaled(
            size.width(),
            size.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image.setPixmap(pixmap)

    def resizeEvent(self, event):
        if self.current_pixmap:
            self.set_pixmap(self.current_pixmap)
        super().resizeEvent(event)

    def update_hue(self):
        self.hue_value = self.hueSlider.value()
        self.update_image()
        self.update_info_range()

    def update_saturation(self):
        self.saturation_value = self.saturationSlider.value()
        self.update_image()
        self.update_info_range()

    def update_brightness(self):
        self.brightness_value = self.brightnessSlider.value()
        self.update_image()
        self.update_info_range()

    def get_hsv_range_values(self):
        return self.hue_value, self.saturation_value, self.brightness_value

    def update_image(self):
        if not self.presenter:
            return
        self.presenter.update_hsv_values()
        image, global_value, biggest_area_value = self.presenter.recalculate_image()
        self.set_image(image)
        self.update_percentage_labels(global_value, biggest_area_value)

    def update_percentage_labels(self, global_value, biggest_area_value):
        self.globalValueLabel.setText(f"{global_value:.0f}%")
        self.biggestAreaValueLabel.setText(f"{biggest_area_value:.0f}%")

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self.presenter.init_image)

    def update_info_range(self):
        hue, saturation, brightness = self.get_hsv_range_values()
        self.hueInfoRange.setText(f"{hue[0]*2} - {hue[1]*2}")
        self.saturationInfoRange.setText(f"{saturation[0]} - {saturation[1]}")
        self.brightnessInfoRange.setText(f"{brightness[0]} - {brightness[1]}")