import sys
from PyQt6.QtWidgets import QApplication
from model.canvas_model import CanvasModel
from presenter import Presenter
from utils.container import Container
from view.main_window import View

def main():
    app = QApplication(sys.argv)
    container = Container()
    presenter = container.presenter()
    view = container.view()
    presenter.view = view
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()