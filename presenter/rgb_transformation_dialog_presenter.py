from model.image import Image
from view.rgb_transformation_dialog import RgbTransformationDialog


class RgbTransformationDialogPresenter:
    def __init__(self, model: Image, view: RgbTransformationDialog):
        self.model = model
        self.view = view
