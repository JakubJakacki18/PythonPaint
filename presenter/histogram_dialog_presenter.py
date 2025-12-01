from PyQt6.QtGui import QImage
from model.image import Image
from utils.enums.color_channel import ColorChannel
from utils.image_service import ImageService
from view.histogram_dialog import HistogramDialog


class HistogramDialogPresenter:
    def __init__(self, model: Image, view: HistogramDialog):
        self.model = model
        self.view = view

    def init_images(self):
        operation = self.view.get_default_mode()
        image, histogram = self.set_channel(operation)
        self.view.set_images(image, histogram)

    def update_original_image(self, current_image):
        self.model.image = current_image

    def equalize_histogram(self, operation: ColorChannel):
        original_arr, _, _ = ImageService.load_image_to_arr(self.model.image)
        arr = ImageService.histogram_equalization(original_arr, operation)
        return self.set_channel(operation, arr)

    def extend_histogram(self, operation: ColorChannel):
        original_arr, _, _ = ImageService.load_image_to_arr(self.model.image)
        arr = ImageService.histogram_extend(original_arr, operation)
        return self.set_channel(operation, arr)

    def set_channel(self, operation: ColorChannel, arr=None):
        if arr is None:
            arr, width, height = ImageService.load_image_to_arr(self.model.image)
        else:
            width = arr.shape[1]
            height = arr.shape[0]
        match operation:
            case ColorChannel.RED:
                new_arr = ImageService.isolate_channel(arr, operation.RED)
                histogram = ImageService.histogram_from_array(new_arr, ColorChannel.RED)
            case ColorChannel.GREEN:
                new_arr = ImageService.isolate_channel(arr, operation.GREEN)
                histogram = ImageService.histogram_from_array(
                    new_arr, ColorChannel.GREEN
                )
            case ColorChannel.BLUE:
                new_arr = ImageService.isolate_channel(arr, operation.BLUE)
                histogram = ImageService.histogram_from_array(
                    new_arr, ColorChannel.BLUE
                )
            case ColorChannel.GRAY:
                new_arr = ImageService.grayscale_of_image(arr)
                new_arr = ImageService.convert_to_3d_array(new_arr)
                histogram = ImageService.histogram_from_array(new_arr)
        new_image = QImage(
            new_arr.data, width, height, 3 * width, QImage.Format.Format_RGB888
        )
        return new_image.copy(), histogram
