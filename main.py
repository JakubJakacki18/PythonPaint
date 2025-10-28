import sys
from PyQt6.QtWidgets import QApplication
from utils.container import Container


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