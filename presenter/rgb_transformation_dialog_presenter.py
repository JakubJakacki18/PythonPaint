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
        image = QImage(self.model.image)
        width = image.width()
        height = image.height()
        ptr = image.bits()
        ptr.setsize(image.height() * image.bytesPerLine())
        arr = np.frombuffer(ptr, np.uint8).reshape(
            (height, image.bytesPerLine() // 3, 3)
        )
        arr = arr[:, :width, :]
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
