from abc import abstractmethod

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from model.point import Point


class BaseCanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.presenter = None

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_press(pos)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_move(pos)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        pos = Point(event.position().x(), event.position().y())
        if self.presenter:
            self.presenter.handle_mouse_release()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        print("Kod klawisza:", event.key())
        print("Znak:", event.text())
        if self.presenter:
            self.presenter.handle_key_press(event)

    @abstractmethod
    def paintEvent(self, event: QtGui.QPaintEvent):
        pass
