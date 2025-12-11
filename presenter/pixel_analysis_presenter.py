from enum import global_str
from typing import Optional, Tuple

import numpy as np
from PyQt6.QtGui import QImage

from model.image import Image
from utils.enums.color_channel import ColorChannel
from utils.image_service import ImageService
from view.pixel_analysis_dialog import PixelAnalysisDialog


class PixelAnalysisPresenter:
    def __init__(self, model: Image, view: PixelAnalysisDialog):
        self.model = model
        self.view = view
        self.hue_value: Optional[Tuple[int, int]] = None
        self.saturation_value: Optional[Tuple[int, int]] = None
        self.brightness_value: Optional[Tuple[int, int]] = None
        arr, self.width, self.height = ImageService.load_image_to_arr(self.model.image)
        self.hsv_arr = ImageService.convert_to_hsv(arr)

    def init_image(self):
        self.update_hsv_values()
        image, global_percentage, biggest_area_percentage = self.recalculate_image()
        self.view.set_image(image)
        self.view.update_percentage_labels(global_percentage, biggest_area_percentage)

    def update_hsv_values(self):
        self.hue_value, self.saturation_value, self.brightness_value = (
            self.view.get_hsv_range_values()
        )

    def recalculate_image(self):
        new_arr = ImageService.binarization_of_hsv_array(
            self.hsv_arr, self.hue_value, self.saturation_value, self.brightness_value
        )
        kernel = np.ones((3, 3), np.uint8)
        new_arr = ImageService.closing(new_arr, kernel)
        new_arr = ImageService.convert_to_3d_array(new_arr, ColorChannel.GRAY)
        global_percentage = (
            ImageService.count_pixels(new_arr, 255, 255, 255)
            / (self.width * self.height)
        ) * 100
        biggest_area_percentage = (
            ImageService.count_pixels(
                ImageService.get_largest_segment(new_arr), 255, 255, 255
            )
            / (self.width * self.height)
        ) * 100
        new_image = QImage(
            new_arr.data,
            self.width,
            self.height,
            3 * self.width,
            QImage.Format.Format_RGB888,
        )
        return new_image.copy(), global_percentage, biggest_area_percentage
