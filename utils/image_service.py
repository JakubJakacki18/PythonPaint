from typing import Literal, Tuple

import numpy as np
from PyQt6.QtGui import QImage
from scipy.ndimage import generate_binary_structure, label

from utils.enums.color_channel import ColorChannel


class ImageService:
    @staticmethod
    def load_image_to_arr(image: QImage):
        width = image.width()
        height = image.height()
        bytes_per_line = image.bytesPerLine()
        ptr = image.bits()
        ptr.setsize(bytes_per_line * height)
        buffer = np.frombuffer(ptr, dtype=np.uint8).reshape((height, bytes_per_line))
        channels = 3
        arr = buffer[:, : width * channels].reshape((height, width, channels)).copy()
        return arr, width, height

    @staticmethod
    def binarization_of_image(
        arr: np.ndarray, max_value: int = 1, threshold: int = 127
    ) -> np.ndarray:
        gray_arr = ImageService.grayscale_of_image(arr)
        binarized_arr = np.where(gray_arr > threshold, max_value, 0).astype(np.uint8)
        return binarized_arr

    @staticmethod
    def grayscale_of_image(arr: np.ndarray) -> np.ndarray:
        gray = (
            0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
        ).astype(np.uint8)
        return gray

    @staticmethod
    def histogram_from_array(
        arr: np.ndarray, operation: ColorChannel = ColorChannel.GRAY
    ) -> np.ndarray:
        channel = operation.value if operation != ColorChannel.GRAY else 0
        hist, _ = np.histogram(arr[:, :, channel], bins=256, range=(0, 255))
        return hist

    @staticmethod
    def convert_to_3d_array(
        arr: np.ndarray, operation: ColorChannel = ColorChannel.GRAY
    ) -> np.ndarray:
        channel_map = {
            ColorChannel.RED: (1, 0, 0),
            ColorChannel.GREEN: (0, 1, 0),
            ColorChannel.BLUE: (0, 0, 1),
            ColorChannel.GRAY: (1, 1, 1),
        }
        r_mult, g_mult, b_mult = channel_map[operation]

        h, w = arr.shape
        result = np.zeros((h, w, 3), dtype=arr.dtype)
        result[:, :, 0] = arr * r_mult
        result[:, :, 1] = arr * g_mult
        result[:, :, 2] = arr * b_mult
        return result

    @staticmethod
    def isolate_channel(arr: np.ndarray, operation: ColorChannel) -> np.ndarray:
        mask = np.arange(3) != operation.value
        out = arr.copy()
        out[:, :, mask] = 0
        return out

    @staticmethod
    def otsu_threshold(arr: np.ndarray) -> int:
        pixels = arr.flatten()
        hist, bins = np.histogram(pixels, bins=256, range=(0, 256))
        total = pixels.size
        p = hist / total

        mean_total = np.sum(np.arange(256) * p)

        w0 = np.cumsum(p)
        w1 = 1 - w0

        mean0 = np.cumsum(np.arange(256) * p)
        mean1 = mean_total - mean0

        valid = (w0 > 0) & (w1 > 0)

        sigma_b2 = (
            (mean1[valid] / w1[valid] - mean0[valid] / w0[valid]) ** 2
            * w0[valid]
            * w1[valid]
        )
        threshold = int(np.argmax(sigma_b2))

        return threshold

    @staticmethod
    def entropy_threshold(arr: np.ndarray) -> int:
        gray = arr[:, :, 0].flatten()

        # Calculate histogram
        hist, _ = np.histogram(gray, bins=256, range=(0, 256))
        hist = hist.astype(float)

        # Normalize histogram to get probabilities
        total_pixels = hist.sum()
        prob = hist / total_pixels

        # Avoid log(0) by filtering out zero probabilities
        prob = np.where(prob > 0, prob, 1e-10)

        max_entropy = -np.inf
        optimal_threshold = 0

        # Try each possible threshold
        for t in range(1, 256):
            # Background class (0 to t-1)
            prob_bg = prob[:t]
            weight_bg = prob_bg.sum()

            # Foreground class (t to 255)
            prob_fg = prob[t:]
            weight_fg = prob_fg.sum()

            # Skip if either class is empty
            if weight_bg == 0 or weight_fg == 0:
                continue

            # Normalize probabilities within each class
            prob_bg_norm = prob_bg / weight_bg
            prob_fg_norm = prob_fg / weight_fg

            # Calculate entropy for each class
            entropy_bg = -np.sum(prob_bg_norm * np.log(prob_bg_norm + 1e-10))
            entropy_fg = -np.sum(prob_fg_norm * np.log(prob_fg_norm + 1e-10))

            # Total entropy (Kapur's criterion)
            total_entropy = entropy_bg + entropy_fg

            # Update if this is the maximum
            if total_entropy > max_entropy:
                max_entropy = total_entropy
                optimal_threshold = t

        return optimal_threshold

    @staticmethod
    def iterative_threshold(arr, epsilon=0.5):
        gray = arr[:, :, 0].flatten().astype(np.float32)
        T = gray.mean()

        while True:
            G1 = gray[gray <= T]
            G2 = gray[gray > T]

            if len(G1) == 0 or len(G2) == 0:
                break

            T_new = (G1.mean() + G2.mean()) / 2

            if abs(T_new - T) < epsilon:
                break

            T = T_new

        return int(T)

    @staticmethod
    def sauvola_binarization(
        arr: np.ndarray, window_size: int = 15, k: float = 0.5, R: float = 128
    ) -> np.ndarray:
        """
        Sauvola's local thresholding method.

        Args:
            arr: Grayscale image array of shape (width, height, 3) where r=g=b
            window_size: Size of local window (should be odd)
            k: Parameter that controls threshold (typically 0.5)
            R: Dynamic range of standard deviation (typically 128 for grayscale)

        Returns:
            Binary threshold map of shape (width, height)
        """
        from scipy.ndimage import uniform_filter

        # Extract single channel
        gray = arr[:, :, 0].astype(np.float32)

        # Calculate local mean
        local_mean = uniform_filter(gray, size=window_size, mode="reflect")

        # Calculate local standard deviation
        local_mean_sq = uniform_filter(gray**2, size=window_size, mode="reflect")
        local_std = np.sqrt(np.maximum(local_mean_sq - local_mean**2, 0))

        # Sauvola threshold: T = mean * (1 + k * ((std / R) - 1))
        threshold = local_mean * (1 + k * ((local_std / R) - 1))

        return (gray > threshold).astype(np.uint8) * 255

    @staticmethod
    def nilblack_binarization(
        arr: np.ndarray, window_size: int = 15, k: float = -0.2
    ) -> np.ndarray:
        """
        Niblack's local thresholding method.

        Args:
            arr: Grayscale image array of shape (width, height, 3) where r=g=b
            window_size: Size of local window (should be odd)
            k: Parameter that controls threshold value (typically -0.2 to -0.5)

        Returns:
            Binary threshold map of shape (width, height)
        """
        from scipy.ndimage import uniform_filter

        # Extract single channel
        gray = arr[:, :, 0].astype(np.float32)

        # Calculate local mean
        local_mean = uniform_filter(gray, size=window_size, mode="reflect")

        # Calculate local standard deviation
        local_mean_sq = uniform_filter(gray**2, size=window_size, mode="reflect")
        local_std = np.sqrt(np.maximum(local_mean_sq - local_mean**2, 0))

        # Niblack threshold: T = mean + k * std
        threshold = local_mean + k * local_std

        return (gray > threshold).astype(np.uint8) * 255

    @staticmethod
    def phansalkar_binarization(
        arr: np.ndarray,
        window_size: int = 15,
        k: float = 0.25,
        R: float = 0.5,
        p: float = 2.0,
        q: float = 10.0,
    ) -> np.ndarray:
        """
        Phansalkar's local thresholding method (improved for low contrast images).

        Args:
            arr: Grayscale image array of shape (width, height, 3) where r=g=b
            window_size: Size of local window (should be odd)
            k: Parameter (typically 0.25)
            R: Parameter (typically 0.5)
            p: Parameter (typically 2.0)
            q: Parameter (typically 10.0)

        Returns:
            Binary threshold map of shape (width, height)
        """
        from scipy.ndimage import uniform_filter

        # Extract single channel and normalize to [0, 1]
        gray = arr[:, :, 0].astype(np.float32) / 255.0

        # Calculate local mean
        local_mean = uniform_filter(gray, size=window_size, mode="reflect")

        # Calculate local standard deviation
        local_mean_sq = uniform_filter(gray**2, size=window_size, mode="reflect")
        local_std = np.sqrt(np.maximum(local_mean_sq - local_mean**2, 0))

        # Phansalkar threshold: T = mean * (1 + p * exp(-q * mean) + k * ((std / R) - 1))
        threshold = local_mean * (
            1 + p * np.exp(-q * local_mean) + k * ((local_std / R) - 1)
        )

        return (gray > threshold).astype(np.uint8) * 255

    @staticmethod
    def histogram_equalization(arr: np.ndarray, operation: ColorChannel) -> np.ndarray:
        histogram = ImageService.histogram_from_array(arr, operation)
        cdf = histogram.cumsum()
        if cdf.max() - cdf.min() == 0:
            return arr
        cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        channel = (
            operation.value
            if operation != ColorChannel.GRAY
            else ColorChannel.RED.value
        )
        channel_arr = arr[:, :, channel]
        equalized = cdf_normalized[channel_arr].astype(np.uint8)
        result_arr = ImageService.convert_to_3d_array(equalized, operation)

        return result_arr

    @staticmethod
    def histogram_extend(arr: np.ndarray, operation: ColorChannel) -> np.ndarray:
        channel = (
            operation.value
            if operation != ColorChannel.GRAY
            else ColorChannel.RED.value
        )
        channel_arr = arr[:, :, channel]
        min_val = float(channel_arr.min())
        max_val = float(channel_arr.max())
        if max_val == min_val:
            return arr

        stretched = (channel_arr - min_val) * (255.0 / (max_val - min_val))
        stretched = np.clip(stretched, 0, 255).astype(np.uint8)
        result_arr = ImageService.convert_to_3d_array(stretched, operation)
        return result_arr

    @staticmethod
    def sliding_window_view(
        channel: np.ndarray,
        kernel: np.ndarray,
        mode: Literal["edge", "constant"] = "edge",
    ):
        height, width = channel.shape
        kh, kw = kernel.shape
        pad_h = kh // 2
        pad_w = kw // 2

        padded = np.pad(channel, ((pad_h, pad_h), (pad_w, pad_w)), mode=mode)

        shape = (height, width, kh, kw)
        strides = (
            padded.strides[0],
            padded.strides[1],
            padded.strides[0],
            padded.strides[1],
        )

        windows = np.lib.stride_tricks.as_strided(
            padded, shape=shape, strides=strides, writeable=False
        )
        return windows

    @staticmethod
    def erosion(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        windows = ImageService.sliding_window_view(channel, kernel, mode="constant")
        mask = kernel == 1
        return np.all(windows[:, :, mask] == 255, axis=-1).astype(np.uint8) * 255

    @staticmethod
    def dilatation(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        windows = ImageService.sliding_window_view(channel, kernel, mode="constant")
        mask = kernel == 1
        return np.any(windows[:, :, mask] == 255, axis=-1).astype(np.uint8) * 255

    @staticmethod
    def hit_or_miss(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        windows = ImageService.sliding_window_view(channel, kernel, mode="constant")

        mask_obj = kernel == 1
        mask_bg = kernel == 0

        cond_obj = np.all(windows[:, :, mask_obj] == 255, axis=-1)
        cond_bg = np.all(windows[:, :, mask_bg] == 0, axis=-1)

        return (cond_obj & cond_bg).astype(np.uint8) * 255

    @staticmethod
    def opening(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        return ImageService.dilatation(ImageService.erosion(channel, kernel), kernel)

    @staticmethod
    def closing(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        return ImageService.erosion(ImageService.dilatation(channel, kernel), kernel)

    @staticmethod
    def thinning(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        return (channel & (255 - ImageService.hit_or_miss(channel, kernel))).astype(
            np.uint8
        )

    @staticmethod
    def thickening(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        return (channel | ImageService.hit_or_miss(channel, kernel)).astype(np.uint8)

    @staticmethod
    def convert_to_hsv(arr: np.ndarray) -> np.ndarray:
        img = arr.astype(np.float32)

        # Rozdzielenie kanałów (bez kopiowania pamięci - widok)
        r, g, b = img[..., 0], img[..., 1], img[..., 2]

        # 2. Obliczenie Max (Value), Min i Delta
        # Używamy np.maximum zamiast np.max dla szybkości na 3 kanałach
        max_v = np.maximum(np.maximum(r, g), b)
        min_v = np.minimum(np.minimum(r, g), b)
        df = max_v - min_v

        # 3. Obliczenie Hue (Barwa) - zakres 0-360
        # Inicjalizacja zerami
        h = np.zeros_like(max_v)

        # Maska pikseli, gdzie delta > 0 (dla szarości h=0)
        mask_df = df > 0

        # Maski dla dominujących kanałów (tylko tam, gdzie kolor nie jest szary)
        # Jeśli max_v == r -> (g - b) / df
        mask_r = (max_v == r) & mask_df
        h[mask_r] = (g[mask_r] - b[mask_r]) / df[mask_r]

        # Jeśli max_v == g -> 2 + (b - r) / df
        mask_g = (max_v == g) & (max_v != r) & mask_df
        h[mask_g] = 2.0 + (b[mask_g] - r[mask_g]) / df[mask_g]

        # Jeśli max_v == b -> 4 + (r - g) / df
        mask_b = (max_v == b) & (max_v != r) & (max_v != g) & mask_df
        h[mask_b] = 4.0 + (r[mask_b] - g[mask_b]) / df[mask_b]

        # Przeskalowanie do stopni (x 60)
        h *= 30.0

        # Obsługa ujemnych wartości Hue (np. gdy g < b w przypadku r_max)
        h[h < 0] += 180.0

        # 4. Obliczenie Saturation (Nasycenie) - zakres 0-255
        s = np.zeros_like(max_v)
        # S = 0 jeśli V = 0, w przeciwnym razie S = delta / max_v
        mask_v = max_v > 0
        # Mnożymy * 255 aby uzyskać zakres 0-255
        s[mask_v] = (df[mask_v] / max_v[mask_v]) * 255.0

        # 5. Value (Jasność) - zakres 0-255
        # Mamy już max_v, które jest w zakresie 0-255 (bo input był 0-255)
        v = max_v

        # 6. Złożenie kanałów z powrotem w jeden obraz
        # Złożenie i rzutowanie na bezpieczny typ (np. float32 dla dalszych obliczeń
        # lub uint8 jeśli chcemy wyświetlać, ale Hue wymaga >255, więc float jest bezpieczniejszy)

        # Uwaga: H jest 0-360, więc nie zmieści się w uint8.
        # Zwracamy jako float32, lub int16. Tu zostawiam float32 dla precyzji.
        hsv_arr = np.stack((h, s, v), axis=-1)

        return hsv_arr.astype(np.uint8).copy()

    @staticmethod
    def binarization_of_hsv_array(
        arr: np.ndarray,
        hue: Tuple[int, int],
        saturation: Tuple[int, int],
        brightness: Tuple[int, int],
    ) -> np.ndarray:
        h_channel = arr[:, :, 0]
        s_channel = arr[:, :, 1]
        b_channel = arr[:, :, 2]
        hue_min, hue_max = hue
        print(f"Typ danych tablicy wejściowej (arr.dtype): {arr.dtype}")
        print(f"Kształt tablicy: {arr.shape}")

        if hue_min <= hue_max:
            hue_mask = (h_channel >= hue_min) & (h_channel <= hue_max)
        else:
            hue_mask = (h_channel >= hue_min) | (h_channel <= hue_max)

        sat_min, sat_max = saturation
        saturation_mask = (s_channel >= sat_min) & (s_channel <= sat_max)

        val_min, val_max = brightness
        brightness_mask = (b_channel >= val_min) & (b_channel <= val_max)
        final_mask = hue_mask & saturation_mask & brightness_mask
        return final_mask.astype(np.uint8) * 255

    @staticmethod
    def count_pixels(arr, r, g, b) -> int:
        mask = np.all(arr == [r, g, b], axis=-1)
        return np.count_nonzero(mask)

    @staticmethod
    def get_largest_segment(arr: np.ndarray) -> np.ndarray:
        binary_input = arr[:, :, 0]
        struct = generate_binary_structure(rank=2, connectivity=2)

        # 2. Etykietowanie (Labeling) - to jest kluczowy algorytm CCL
        # labeled_array: tablica gdzie każdy piksel ma ID grupy (0, 1, 2, 3...)
        # num_features: liczba znalezionych grup
        labeled_array, num_features = label(binary_input > 0, structure=struct)

        # Szybkie wyjście, jeśli nie znaleziono żadnych obiektów (sam czarny obraz)
        if num_features == 0:
            return np.zeros_like(binary_input, dtype=np.uint8)

        # 3. Zliczanie wielkości grup (Histogram)
        # bincount zlicza ile razy występuje każda liczba w labeled_array.
        # .ravel() spłaszcza tablicę do 1D (wymagane dla bincount).
        sizes = np.bincount(labeled_array.ravel())

        # 4. Wyzerowanie tła
        # Indeks 0 w 'sizes' to liczba pikseli tła. Nie chcemy, żeby tło wygrało
        # jako "największy obiekt", więc ustawiamy jego wielkość na 0.
        sizes[0] = 0

        # 5. Znalezienie ID zwycięzcy
        # argmax zwraca indeks (czyli ID grupy) o największej wartości.
        max_label_id = sizes.argmax()

        # 6. Stworzenie maski wynikowej
        # Tworzymy tablicę True/False tam, gdzie ID zgadza się ze zwycięzcą
        largest_mask = (labeled_array == max_label_id).astype(np.uint8) * 255
        return np.stack((largest_mask, largest_mask, largest_mask), axis=-1)
