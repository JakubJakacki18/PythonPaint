import numpy as np
from PyQt6.QtGui import QImage

from model.image import Image
from utils.enums.image_filter_operation import ImageFilterOperation
from utils.image_service import ImageService
from view.filter_dialog import FilterDialog


class FilterDialogPresenter:
    def __init__(self, model: Image, view: FilterDialog):
        self.model = model
        self.view = view

    def init_images(self):
        self.view.set_images(self.model.image)

    def update_original_image(self, current_image):
        self.model.image = current_image

    @staticmethod
    def _normalize_kernel(kernel):
        s = kernel.sum()
        if s != 0:
            return kernel / s
        return kernel

    def apply_filter(self, operation: ImageFilterOperation, matrix=None):
        arr, width, height = ImageService.load_image_to_arr(self.model.image)

        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]

        match operation:
            case ImageFilterOperation.HIGH_PASS:
                high_pass_kernel = np.array(
                    [
                        [-1, -1, -1],
                        [-1, 9, -1],
                        [-1, -1, -1],
                    ],
                    dtype=np.float32,
                )
                r2 = convolve(r, high_pass_kernel)
                g2 = convolve(g, high_pass_kernel)
                b2 = convolve(b, high_pass_kernel)

            case ImageFilterOperation.SOBEL_VERTICAL:
                sobel_v = np.array(
                    [
                        [-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1],
                    ],
                    dtype=np.float32,
                )
                r2 = convolve(r, sobel_v)
                g2 = convolve(g, sobel_v)
                b2 = convolve(b, sobel_v)
            case ImageFilterOperation.SOBEL_HORIZONTAL:
                sobel_h = np.array(
                    [
                        [1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1],
                    ],
                    dtype=np.float32,
                )
                r2 = convolve(r, sobel_h)
                g2 = convolve(g, sobel_h)
                b2 = convolve(b, sobel_h)
            case ImageFilterOperation.SMOOTH:
                smooth_kernel = np.ones((3, 3), dtype=np.float32)
                r2 = convolve(r, smooth_kernel)
                g2 = convolve(g, smooth_kernel)
                b2 = convolve(b, smooth_kernel)
            case ImageFilterOperation.GAUSS:
                gauss_kernel = np.array(
                    [[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32
                )
                r2 = convolve(r, gauss_kernel)
                g2 = convolve(g, gauss_kernel)
                b2 = convolve(b, gauss_kernel)
            case ImageFilterOperation.MEDIAN:
                r2 = median_filter(r)
                g2 = median_filter(g)
                b2 = median_filter(b)
            case ImageFilterOperation.CUSTOM:
                if matrix is None:
                    return QImage(self.model.image)

                custom_matrix = np.array(matrix, dtype=np.float32)

                r2 = convolve(r, custom_matrix)
                g2 = convolve(g, custom_matrix)
                b2 = convolve(b, custom_matrix)
            case _:
                return QImage(self.model.image)

        result = np.stack([r2, g2, b2], axis=2)
        new_image = QImage(
            result.data, width, height, 3 * width, QImage.Format.Format_RGB888
        )
        return new_image.copy()


def convolve(channel, kernel):
    kh, kw = kernel.shape
    pad_h = kh // 2
    pad_w = kw // 2
    kernel = FilterDialogPresenter._normalize_kernel(kernel)

    padded = np.pad(channel, ((pad_h, pad_h), (pad_w, pad_w)), mode="edge")
    shape = (channel.shape[0], channel.shape[1], kh, kw)
    strides = (
        padded.strides[0],
        padded.strides[1],
        padded.strides[0],
        padded.strides[1],
    )

    windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)

    # broadcasting: (H,W,kh,kw) * (kh,kw) → suma → (H,W)
    out = np.einsum("ijkl,kl->ij", windows, kernel)

    return np.clip(out, 0, 255).astype(np.uint8)


def median_filter(channel, size=3):
    pad = size // 2
    padded = np.pad(channel, ((pad, pad), (pad, pad)), mode="edge")
    shape = (channel.shape[0], channel.shape[1], size, size)
    strides = (
        padded.strides[0],
        padded.strides[1],
        padded.strides[0],
        padded.strides[1],
    )
    windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)
    out = np.median(windows, axis=(2, 3))
    return out.astype(np.uint8)
