from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(800, 600)
        self.setWindowTitle("Python Paint")

        self.label = QLabel()
        self.previousPoint = None

        self.canvas = QPixmap(QSize(600, 400))
        self.canvas.fill(QColor("white"))

        self.pen = QPen()
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.pen.setWidth(6)

        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self,event):
        position = event.pos()
        print(position)
        print(self.previousPoint)

        painter = QPainter(self.canvas)
        painter.setPen(self.pen)

        if self.previousPoint:
            painter.drawLine(self.previousPoint.x(), self.previousPoint.y(),position.x(), position.y())
        else:
            painter.drawPoint(position.x(),position.y())
            painter.drawPoint(position.x(),position.y())

        painter.end()

        self.label.setPixmap(self.canvas)
        self.previousPoint = position

    def mouseReleaseEvent(self, a0):
        self.previousPoint = None



#
#
# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec()


