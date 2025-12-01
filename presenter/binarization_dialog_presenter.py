from PyQt6.QtGui import QImage

from model.image import Image
from utils.enums.binary_operation import BinaryOperation
from utils.image_service import ImageService
from view.binary_dialog import BinaryDialog
import numpy as np


class BinarizationDialogPresenter:
    def __init__(self, model: Image, view: BinaryDialog):
        self.model = model
        self.view = view

    def init_images(self):
        operation, value = self.view.get_default_mode()
        image, histogram = self.apply_binarization(operation, value)
        self.view.set_images(image, histogram)

    def update_original_image(self, current_image):
        self.model.image = current_image

    def apply_binarization(self, operation: BinaryOperation, value=None):
        arr, width, height = ImageService.load_image_to_arr(self.model.image)
        max_value = 255
        match operation:
            case BinaryOperation.MANUAL:
                if value is None:
                    raise ValueError("value cannot be None")
                new_arr = ImageService.binarization_of_image(arr, max_value, value)
            case BinaryOperation.PERCENT:
                if value is None:
                    raise ValueError("value cannot be None")
                threshold = np.percentile(arr, value)
                new_arr = ImageService.binarization_of_image(arr, max_value, threshold)
            case BinaryOperation.OTSU:
                threshold = ImageService.otsu_threshold(arr)
                new_arr = ImageService.binarization_of_image(arr, max_value, threshold)
            case BinaryOperation.NILBLACK:
                new_arr = ImageService.nilblack_binarization(arr)
            case BinaryOperation.ENTROPY:
                threshold = ImageService.entropy_threshold(arr)
                print("ENTROPY: ", threshold)
                new_arr = ImageService.binarization_of_image(arr, max_value, threshold)
            case BinaryOperation.ITERATIVE:
                threshold = ImageService.iterative_threshold(arr)
                print("ITERATIVE: ", threshold)
                new_arr = ImageService.binarization_of_image(arr, max_value, threshold)
            case BinaryOperation.PHANSALKAR:
                new_arr = ImageService.phansalkar_binarization(arr)
            case BinaryOperation.SAUVOLA:
                new_arr = ImageService.sauvola_binarization(arr)
            case _:
                pass
        new_arr = ImageService.convert_to_3d_array(new_arr)
        new_image = QImage(
            new_arr.data, width, height, 3 * width, QImage.Format.Format_RGB888
        )
        histogram = ImageService.histogram_from_array(new_arr)
        return new_image.copy(), histogram
