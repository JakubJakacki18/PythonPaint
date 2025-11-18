import numpy as np
from PyQt6.QtGui import QImage, QColor

from model.image import Image
from utils.image_transformation_operation import ImageTransformationOperation
from view.rgb_transformation_dialog import RgbTransformationDialog


class RgbTransformationDialogPresenter:
    def __init__(self, model: Image, view: RgbTransformationDialog):
        self.model = model
        self.view = view

    def init_images(self):
        self.view.set_images(self.model.image)

    def recalculate_image(self, operation, r, g, b):
        # image = QImage(self.model.image)
        # width = image.width()
        # height = image.height()
        #
        # for y in range(height):
        #     for x in range(width):
        #         color = QColor(image.pixel(x, y))
        #         r = min(color.red() + r, 255)
        #         g = min(color.green() + g, 255)
        #         b = min(color.blue() + b, 255)
        #         image.setPixelColor(x, y, QColor(r, g, b))
        #
        # return image
        arr, width, height = self._load_image_to_arr()
        match operation:
            case ImageTransformationOperation.ADD:
                arr = np.clip(arr + np.array([r, g, b], dtype=np.int16), 0, 255).astype(
                    np.uint8
                )
            case ImageTransformationOperation.SUBTRACT:
                arr = np.clip(arr - np.array([r, g, b], dtype=np.int16), 0, 255).astype(
                    np.uint8
                )
            case ImageTransformationOperation.DIVIDE:
                r = r if r != 0 else 1
                g = g if g != 0 else 1
                b = b if b != 0 else 1
                arr = np.clip(arr / np.array([r, g, b], dtype=np.int16), 0, 255).astype(
                    np.uint8
                )
            case ImageTransformationOperation.MULTIPLY:
                arr = np.clip(arr * np.array([r, g, b], dtype=np.int16), 0, 255).astype(
                    np.uint8
                )

        new_image = QImage(
            arr.data, width, height, 3 * width, QImage.Format.Format_RGB888
        )
        return new_image.copy()

    def change_brightness_of_image(self, brightness):
        args = (brightness,) * 3
        return self.recalculate_image(ImageTransformationOperation.ADD, *args)

    def update_original_image(self, current_image):
        self.model.image = current_image

    def transform_color_image_into_gray(self, method_number: int):
        arr, width, height = self._load_image_to_arr()
        match method_number:
            case 0:
                gray = np.mean(arr, axis=2).astype(np.uint8)
                gray_rgb = np.stack((gray, gray, gray), axis=2)
            case 1:
                gray = np.max(arr, axis=2).astype(np.uint8)
                gray_rgb = np.stack((gray, gray, gray), axis=2)
            case _:
                raise ValueError(f"Method number: {method_number} is not supported")
        new_image = QImage(
            gray_rgb.data, width, height, 3 * width, QImage.Format.Format_RGB888
        )
        return new_image.copy()

    def _load_image_to_arr(self):
        image = QImage(self.model.image)
        width = image.width()
        height = image.height()
        ptr = image.bits()
        ptr.setsize(image.height() * image.bytesPerLine())
        arr = np.frombuffer(ptr, np.uint8).reshape(
            (height, image.bytesPerLine() // 3, 3)
        )
        arr = arr[:, :width, :]
        return arr, width, height
