from model.image import Image
from view.binary_dialog import BinaryDialog


class BinarizationDialogPresenter:
    def __init__(self, model: Image, view: BinaryDialog):
        self.model = model
        self.view = view

    def init_images(self):
        self.view.set_images(self.model.image)

    def update_original_image(self, current_image):
        self.model.image = current_image
