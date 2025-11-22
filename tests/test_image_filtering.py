import numpy as np
import pytest
from PyQt6.QtGui import QImage

from model.image import Image
from model.pen import Pen
from model.point import Point
from presenter.filter_dialog_presenter import FilterDialogPresenter
from utils.image_filter_operation import ImageFilterOperation


class TestImageFiltering:
    @pytest.fixture(autouse=True)
    def setup(self):
        black = [0,0,0]
        white = [255,255,255]
        self.array = np.array([[white,white,white,white,white],
                          [black,white,white,white,black],
                          [white,white,black,white,white],
                          [white,white,black,white,white],
                          [white,white,white,white,white]],dtype=np.uint8)

        q_image = QImage(self.array.data, self.array.shape[1], self.array.shape[0], self.array.shape[1] * 3, QImage.Format.Format_RGB888).copy()
        self.image = Image(Pen(),Point(0,0),Point(0,0),q_image)
        assert self.image is not None
        self.presenter = FilterDialogPresenter(self.image, None)


    def test_image_smoothing(self):
        print("Image: ",self.presenter._load_image_to_arr(self.image.image))
        new_image = self.presenter.apply_filter(ImageFilterOperation.SMOOTH)
        arr, _, _ = self.presenter._load_image_to_arr(new_image)
        print("Image after changes:",arr)
        expected_output = [[198,226,255,226,198],
                      [198,198,226,198,198],
                      [198,170,198,170,198],
                      [255,198,198,198,255],
                      [255,226,226,226,255]]

        expected_arr = self._get_rgb_np_array(expected_output)
        assert np.array_equal(arr, expected_arr)
        
    def test_image_sharpening(self):
        print("Image: ", self.presenter._load_image_to_arr(self.image.image))
        new_image = self.presenter.apply_filter(ImageFilterOperation.HIGH_PASS)
        arr, _, _ = self.presenter._load_image_to_arr(new_image)
        print("Image after changes:", arr)
        assert np.array_equal(arr, self.array)

    def test_image_median_filter(self):
        new_image = self.presenter.apply_filter(ImageFilterOperation.MEDIAN)
        arr, _, _ = self.presenter._load_image_to_arr(new_image)
        expected_output = [[255, 255, 255, 255, 255],
                           [255, 255, 255, 255, 255],
                           [255, 255, 255, 255, 255],
                           [255, 255, 255, 255, 255],
                           [255, 255, 255, 255, 255]]

        expected_arr = self._get_rgb_np_array(expected_output)
        assert np.array_equal(arr,expected_arr)

        



    def _get_rgb_np_array(self, array):
        new_array = []
        for row in array:
            row_list = []
            for col in row:
                row_list.append([col,col,col])
            new_array.append(row_list)
        return np.array(new_array,dtype=np.uint8)






