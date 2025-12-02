import numpy as np
from PyQt6.QtGui import QImage

from model.image import Image
from utils.enums.morph_operation import MorphOperation
from utils.image_service import ImageService
from view.morph_dialog import MorphDialog


class MorphDialogPresenter:
    def __init__(self, model: Image, view: MorphDialog):
        self.model = model
        self.view = view

    def init_images(self):
        self.view.set_images(self.model.image)

    def update_original_image(self, current_image):
        self.model.image = current_image

    def apply_filter(self, operation: MorphOperation, matrix):
        arr, width, height = ImageService.load_image_to_arr(self.model.image)

        red_channel = arr[:, :, 0]

        operation_dict = {
            operation.EROSION: ImageService.erosion,
            operation.DILATION: ImageService.dilation,
            operation.OPENING: ImageService.opening,
            operation.CLOSING: ImageService.closing,
            operation.HIT_OR_MISS: ImageService.hitOrMiss,
        }
        custom_matrix = np.array(matrix, dtype=np.float32)
        new_red_channel = operation_dict[operation](red_channel, custom_matrix)
        new_arr = ImageService.convert_to_3d_array(new_red_channel)
        new_image = QImage(
            new_arr.data, width, height, 3 * width, QImage.Format.Format_RGB888
        )
        return new_image.copy()
