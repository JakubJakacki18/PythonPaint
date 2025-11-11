from enum import Enum

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from view.rgb_transformation_dialog_ui import Ui_RgbTransformationDialog

# class Operation(Enum):
#     ADD= 0,
#     SUBTRACT= 1,
#     MULTIPLY= 2,
#     DIVIDE= 3,


class RgbTransformationDialog(QDialog, Ui_RgbTransformationDialog):
    def __init__(self, presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.brightnessPickerWidget = uic.loadUi("view/brightness_picker_widget.ui")
        self.rgbColorPickerWidget = uic.loadUi("view/rgb_color_picker_widget.ui")
        self.imagePreviewWidget = uic.loadUi("view/image_preview_widget.ui")
        self.imageFrame.layout().addWidget(self.imagePreviewWidget)

        self.presenter = presenter
        self.mathOperationsButtons = (
            self.addButton,
            self.multiplyButton,
            self.divideButton,
            self.minusButton,
        )
        self.currentPanel = None
        self.allOperationsButtons = (
            *self.mathOperationsButtons,
            self.brightnessButton,
            self.grayFirstButton,
            self.graySecondButton,
        )

        self.pickedOperationButton = None

        self.addButton.clicked.connect(lambda: self.add_button_pressed())
        self.multiplyButton.clicked.connect(lambda: self.multiply_button_pressed())
        self.divideButton.clicked.connect(lambda: self.divide_button_pressed())
        self.minusButton.clicked.connect(lambda: self.minus_button_pressed())
        self.brightnessButton.clicked.connect(lambda: self.brightness_button_pressed())
        self.grayFirstButton.clicked.connect(lambda: self.gray_first_button_pressed())
        self.graySecondButton.clicked.connect(lambda: self.gray_second_button_pressed())

    def untoggle_buttons(self, button):
        all_operations = list(self.allOperationsButtons)
        all_operations.remove(button)
        for button in all_operations:
            button.setChecked(False)

    def toggle_correct_picker(self, button):
        if button in self.mathOperationsButtons:
            self.toggle_picker(self.rgbColorPickerWidget)
        elif button == self.brightnessButton:
            self.toggle_picker(self.brightnessPickerWidget)
        else:
            self.toggle_picker(None)

    def toggle_picker(self, panel):
        layout = self.pickerFrame.layout()
        if self.currentPanel is not None:
            layout.removeWidget(self.currentPanel)
            self.currentPanel.setParent(None)
        if panel:
            layout.addWidget(panel)
            self.currentPanel = panel

    def add_button_pressed(self):
        self.pickedOperationButton = self.addButton
        self.handle_button_pressed()

    def multiply_button_pressed(self):
        self.pickedOperationButton = self.multiplyButton
        self.handle_button_pressed()

    def divide_button_pressed(self):
        self.pickedOperationButton = self.divideButton
        self.handle_button_pressed()

    def minus_button_pressed(self):
        self.pickedOperationButton = self.minusButton
        self.handle_button_pressed()

    def brightness_button_pressed(self):
        self.pickedOperationButton = self.brightnessButton
        self.handle_button_pressed()

    def gray_first_button_pressed(self):
        self.pickedOperationButton = self.grayFirstButton
        self.handle_button_pressed()

    def gray_second_button_pressed(self):
        self.pickedOperationButton = self.graySecondButton
        self.handle_button_pressed()

    def handle_button_pressed(self):
        self.untoggle_buttons(self.pickedOperationButton)
        self.toggle_correct_picker(self.pickedOperationButton)
