from enum import Enum

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from utils.image_transformation_operation import ImageTransformationOperation
from view.rgb_transformation_dialog_ui import Ui_RgbTransformationDialog


class RgbTransformationDialog(QDialog, Ui_RgbTransformationDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.brightnessPickerWidget = uic.loadUi("view/brightness_picker_widget.ui")
        self.rgbColorPickerWidget = uic.loadUi("view/rgb_color_picker_widget.ui")
        self.imagePreviewWidget = uic.loadUi("view/image_preview_widget.ui")
        self.imageFrame.layout().addWidget(self.imagePreviewWidget)
        self.current_image = None

        self.presenter = presenter

        self.math_operations_buttons = (
            self.addButton,
            self.multiplyButton,
            self.divideButton,
            self.minusButton,
        )
        self.current_panel = None
        self.all_operation_buttons = (
            *self.math_operations_buttons,
            self.brightnessButton,
            self.grayFirstButton,
            self.graySecondButton,
        )

        self.picked_operation_button = None
        self.picked_operation = None

        self.addButton.clicked.connect(self.add_button_pressed)
        self.multiplyButton.clicked.connect(self.multiply_button_pressed)
        self.divideButton.clicked.connect(self.divide_button_pressed)
        self.minusButton.clicked.connect(self.minus_button_pressed)
        self.brightnessButton.clicked.connect(self.brightness_button_pressed)
        self.grayFirstButton.clicked.connect(self.gray_first_button_pressed)
        self.graySecondButton.clicked.connect(self.gray_second_button_pressed)

        self.rgbColorPickerWidget.rgbRedSpinBox.valueChanged.connect(self.on_rgb_update)
        self.rgbColorPickerWidget.rgbGreenSpinBox.valueChanged.connect(
            self.on_rgb_update
        )
        self.rgbColorPickerWidget.rgbBlueSpinBox.valueChanged.connect(
            self.on_rgb_update
        )
        self.brightnessPickerWidget.brightnessSpinBox.valueChanged.connect(
            self.on_brightness_update
        )
        self.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.update_original_image
        )

    def untoggle_buttons(self, button):
        all_operations = list(self.all_operation_buttons)
        all_operations.remove(button)
        for button in all_operations:
            button.setChecked(False)

    def toggle_correct_picker(self, button):
        if button in self.math_operations_buttons:
            self.toggle_picker(self.rgbColorPickerWidget)
        elif button == self.brightnessButton:
            self.toggle_picker(self.brightnessPickerWidget)
        else:
            self.toggle_picker(None)

    def toggle_picker(self, panel):
        layout = self.pickerFrame.layout()
        if self.current_panel is not None:
            layout.removeWidget(self.current_panel)
            self.current_panel.setParent(None)
        if panel:
            layout.addWidget(panel)
            self.current_panel = panel

    def add_button_pressed(self):
        self.picked_operation_button = self.addButton
        self.handle_button_pressed()
        self.picked_operation = ImageTransformationOperation.ADD
        self.on_rgb_update()

    def multiply_button_pressed(self):
        self.picked_operation_button = self.multiplyButton
        self.handle_button_pressed()
        self.picked_operation = ImageTransformationOperation.MULTIPLY
        self.on_rgb_update()

    def divide_button_pressed(self):
        self.picked_operation_button = self.divideButton
        self.handle_button_pressed()
        self.picked_operation = ImageTransformationOperation.DIVIDE
        self.on_rgb_update()

    def minus_button_pressed(self):
        self.picked_operation_button = self.minusButton
        self.handle_button_pressed()
        self.picked_operation = ImageTransformationOperation.SUBTRACT
        self.on_rgb_update()

    def brightness_button_pressed(self):
        self.picked_operation_button = self.brightnessButton
        self.handle_button_pressed()
        self.on_brightness_update()

    def gray_first_button_pressed(self):
        self.picked_operation_button = self.grayFirstButton
        self.handle_button_pressed()
        self.on_grayscale_update(0)

    def gray_second_button_pressed(self):
        self.picked_operation_button = self.graySecondButton
        self.handle_button_pressed()
        self.on_grayscale_update(1)

    def handle_button_pressed(self):
        self.untoggle_buttons(self.picked_operation_button)
        self.toggle_correct_picker(self.picked_operation_button)

    def set_images(self, image):
        self.current_image = image
        pixmap = QPixmap.fromImage(image)
        self.imagePreviewWidget.editedImage.setPixmap(pixmap)
        self.imagePreviewWidget.originalImage.setPixmap(pixmap)

    def on_rgb_update(self):
        r = self.rgbColorPickerWidget.rgbRedSpinBox.value()
        g = self.rgbColorPickerWidget.rgbGreenSpinBox.value()
        b = self.rgbColorPickerWidget.rgbBlueSpinBox.value()
        if self.picked_operation is None:
            return
        new_image = self.presenter.recalculate_image(self.picked_operation, r, g, b)
        self.update_edited_image(new_image)

    def on_brightness_update(self):
        brightness = self.brightnessPickerWidget.brightnessSpinBox.value()
        new_image = self.presenter.change_brightness_of_image(brightness)
        self.update_edited_image(new_image)

    def on_grayscale_update(self, method):
        new_image = self.presenter.transform_color_image_into_gray(method)
        self.update_edited_image(new_image)

    def update_edited_image(self, new_image):
        self.current_image = new_image
        new_pixmap = QPixmap.fromImage(new_image)
        self.imagePreviewWidget.editedImage.setPixmap(new_pixmap)

    def update_original_image(self):
        self.presenter.update_original_image(self.current_image)
        pixmap = QPixmap.fromImage(self.current_image)
        self.imagePreviewWidget.originalImage.setPixmap(pixmap)
