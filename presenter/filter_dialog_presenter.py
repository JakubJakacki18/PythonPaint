from model.image import Image
from view.filter_dialog import FilterDialog


class FilterDialogPresenter:
    def __init__(self, model: Image, view: FilterDialog):
        self.model = model
        self.view = view
