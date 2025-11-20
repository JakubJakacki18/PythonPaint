import numpy as np
import pytest
from PyQt6.QtGui import QImage

from presenter.filter_dialog_presenter import FilterDialogPresenter
from utils.image_filter_operation import ImageFilterOperation


class TestImageFiltering:
    @pytest.fixture(autouse=True)
    def setup(self):
        path_to_file = "test.bmp"
        self.image = QImage(path_to_file)
        assert self.image is not None
        self.presenter = FilterDialogPresenter(self.image, None)


    def _test_image_filtering(self):
        new_image = self.presenter.apply_filter(ImageFilterOperation.HIGH_PASS)




