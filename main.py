import sys
from PyQt6.QtWidgets import QApplication
from model.canvas_model import CanvasModel
from presenter import Presenter
from view.view import View

def main():
    app = QApplication(sys.argv)
    model = CanvasModel()
    presenter = Presenter(model, None)
    view = View(presenter)
    presenter.view = view
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()