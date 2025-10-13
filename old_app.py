import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPointF, QRectF

# ----------------------------
# old_model: przechowuje kształty
# ----------------------------
class Shape:
    def __init__(self, pen: QtGui.QPen):
        self.pen = QtGui.QPen(pen)
        self.selected = False

    def draw(self, painter: QtGui.QPainter):
        raise NotImplementedError()

    def contains(self, point: QPointF) -> bool:
        return False

    def bounding_rect(self) -> QRectF:
        return QRectF()

    def move_by(self, dx: float, dy: float):
        raise NotImplementedError()

class Freehand(Shape):
    def __init__(self, path: QtGui.QPainterPath, pen: QtGui.QPen):
        super().__init__(pen)
        self.path = QtGui.QPainterPath(path)

    def draw(self, painter: QtGui.QPainter):
        painter.setPen(self.pen)
        painter.drawPath(self.path)
        if self.selected:
            painter.setPen(QtGui.QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
            painter.drawRect(self.bounding_rect())

    def contains(self, point: QPointF) -> bool:
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(max(6, self.pen.widthF() + 2))
        stroked = stroker.createStroke(self.path)
        return stroked.contains(point)

    def bounding_rect(self) -> QRectF:
        return self.path.boundingRect()

    def move_by(self, dx: float, dy: float):
        tr = QtGui.QTransform()
        tr.translate(dx, dy)
        self.path = tr.map(self.path)

class Line(Shape):
    def __init__(self, p1: QPointF, p2: QPointF, pen: QtGui.QPen):
        super().__init__(pen)
        self.p1 = QPointF(p1)
        self.p2 = QPointF(p2)

    def draw(self, painter: QtGui.QPainter):
        painter.setPen(self.pen)
        painter.drawLine(self.p1, self.p2)
        if self.selected:
            painter.setPen(QtGui.QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
            painter.drawRect(self.bounding_rect())

    def contains(self, point: QPointF) -> bool:
        # distance from point to segment small enough?
        line = QtCore.QLineF(self.p1, self.p2)
        dist = line.distanceToPoint(point)
        return dist <= max(6, self.pen.widthF() + 2)

    def bounding_rect(self) -> QRectF:
        return QRectF(self.p1, self.p2).normalized()

    def move_by(self, dx: float, dy: float):
        self.p1 += QtCore.QPointF(dx, dy)
        self.p2 += QtCore.QPointF(dx, dy)

class RectShape(Shape):
    def __init__(self, rect: QRectF, pen: QtGui.QPen):
        super().__init__(pen)
        self.rect = QRectF(rect)

    def draw(self, painter: QtGui.QPainter):
        painter.setPen(self.pen)
        painter.drawRect(self.rect)
        if self.selected:
            painter.setPen(QtGui.QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
            painter.drawRect(self.bounding_rect())

    def contains(self, point: QPointF) -> bool:
        return self.rect.contains(point)

    def bounding_rect(self) -> QRectF:
        return self.rect

    def move_by(self, dx: float, dy: float):
        self.rect.translate(dx, dy)

class EllipseShape(Shape):
    def __init__(self, rect: QRectF, pen: QtGui.QPen):
        super().__init__(pen)
        self.rect = QRectF(rect)

    def draw(self, painter: QtGui.QPainter):
        painter.setPen(self.pen)
        painter.drawEllipse(self.rect)
        if self.selected:
            painter.setPen(QtGui.QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
            painter.drawRect(self.bounding_rect())

    def contains(self, point: QPointF) -> bool:
        # normalize to unit circle test
        r = self.rect
        if r.width() == 0 or r.height() == 0:
            return False
        cx = r.center().x()
        cy = r.center().y()
        rx = r.width() / 2
        ry = r.height() / 2
        px = (point.x() - cx) / rx
        py = (point.y() - cy) / ry
        return px * px + py * py <= 1.0

    def bounding_rect(self) -> QRectF:
        return self.rect

    def move_by(self, dx: float, dy: float):
        self.rect.translate(dx, dy)

class CanvasModel:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def remove_shape(self, shape: Shape):
        if shape in self.shapes:
            self.shapes.remove(shape)

    def clear_selection(self):
        for s in self.shapes:
            s.selected = False

    def shape_at(self, point: QPointF):
        # last shapes are on top -> iterate reversed
        for s in reversed(self.shapes):
            if s.contains(point):
                return s
        return None

# ----------------------------
# view: Okno i Canvas
# ----------------------------
class CanvasWidget(QtWidgets.QWidget):
    # signals
    mousePressed = QtCore.pyqtSignal(QtCore.QPointF, QtGui.QMouseEvent)
    mouseMoved = QtCore.pyqtSignal(QtCore.QPointF, QtGui.QMouseEvent)
    mouseReleased = QtCore.pyqtSignal(QtCore.QPointF, QtGui.QMouseEvent)
    paintRequested = QtCore.pyqtSignal()

    def __init__(self, presenter=None):
        super().__init__()
        self.presenter = presenter
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.setMouseTracking(True)
        self.setMinimumSize(600, 400)
        self._bg_color = QtGui.QColor('white')

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self._bg_color)
        if self.presenter:
            self.presenter.on_paint(painter)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        pt = event.position()
        self.mousePressed.emit(pt, event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        pt = event.position()
        self.mouseMoved.emit(pt, event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        pt = event.position()
        self.mouseReleased.emit(pt, event)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.setWindowTitle("PyQt6 Paint (MVP)")

        # toolbar
        toolbar = QtWidgets.QToolBar()
        self.addToolBar(toolbar)

        # tool actions
        self.action_pen = QtGui.QAction("Pen", self)
        self.action_line = QtGui.QAction("Line", self)
        self.action_rect = QtGui.QAction("Rect", self)
        self.action_ellipse = QtGui.QAction("Ellipse", self)
        self.action_select = QtGui.QAction("Select", self)
        self.action_delete = QtGui.QAction("Delete", self)

        toolbar.addAction(self.action_pen)
        toolbar.addAction(self.action_line)
        toolbar.addAction(self.action_rect)
        toolbar.addAction(self.action_ellipse)
        toolbar.addAction(self.action_select)
        toolbar.addAction(self.action_delete)

        # color and width
        toolbar.addSeparator()
        self.color_btn = QtWidgets.QPushButton("Color")
        self.width_spin = QtWidgets.QSpinBox()
        self.width_spin.setRange(1, 30)
        self.width_spin.setValue(2)
        toolbar.addWidget(self.color_btn)
        toolbar.addWidget(QtWidgets.QLabel("Width:"))
        toolbar.addWidget(self.width_spin)

        # central canvas
        self.canvas = CanvasWidget(presenter=self.presenter)
        self.setCentralWidget(self.canvas)

        # connect signals
        self.action_pen.triggered.connect(lambda: presenter.set_tool("pen"))
        self.action_line.triggered.connect(lambda: presenter.set_tool("line"))
        self.action_rect.triggered.connect(lambda: presenter.set_tool("rect"))
        self.action_ellipse.triggered.connect(lambda: presenter.set_tool("ellipse"))
        self.action_select.triggered.connect(lambda: presenter.set_tool("select"))
        self.action_delete.triggered.connect(lambda: presenter.delete_selected())

        self.color_btn.clicked.connect(self.choose_color)
        self.width_spin.valueChanged.connect(lambda v: presenter.set_width(v))

        # forward canvas events
        self.canvas.mousePressed.connect(lambda p, e: presenter.canvas_mouse_press(p, e))
        self.canvas.mouseMoved.connect(lambda p, e: presenter.canvas_mouse_move(p, e))
        self.canvas.mouseReleased.connect(lambda p, e: presenter.canvas_mouse_release(p, e))

    def choose_color(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.presenter.set_color(col)

    def refresh(self):
        self.canvas.update()

# ----------------------------
# Presenter: logika i obsługa
# ----------------------------
class Presenter:
    def __init__(self, model: CanvasModel, view: MainWindow):
        self.model = model
        self.view = view
        self.tool = "pen"  # pen, line, rect, ellipse, select
        self.current_pen = QtGui.QPen(QtGui.QColor('black'), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        self.drawing_shape = None
        self.start_pos = None
        self.dragging = False
        self.selected_shape = None
        self.last_mouse_pos = None

    def set_tool(self, tool_name: str):
        self.tool = tool_name
        # clear temporary drawing
        self.drawing_shape = None
        self.model.clear_selection()
        self.selected_shape = None
        self.view.refresh()

    def set_color(self, color: QtGui.QColor):
        self.current_pen.setColor(color)
        if self.selected_shape:
            self.selected_shape.pen.setColor(color)
            self.view.refresh()

    def set_width(self, w: int):
        self.current_pen.setWidth(w)
        if self.selected_shape:
            self.selected_shape.pen.setWidth(w)
            self.view.refresh()

    def delete_selected(self):
        if self.selected_shape:
            self.model.remove_shape(self.selected_shape)
            self.selected_shape = None
            self.view.refresh()

    # Canvas event handlers
    def canvas_mouse_press(self, pos: QPointF, event: QtGui.QMouseEvent):
        posf = QPointF(pos.x(), pos.y())
        self.start_pos = posf
        if self.tool == "pen":
            path = QtGui.QPainterPath(posf)
            pen = QtGui.QPen(self.current_pen)
            self.drawing_shape = Freehand(path, pen)
            self.model.add_shape(self.drawing_shape)
        elif self.tool == "line":
            pen = QtGui.QPen(self.current_pen)
            self.drawing_shape = Line(posf, posf, pen)
            self.model.add_shape(self.drawing_shape)
        elif self.tool == "rect":
            pen = QtGui.QPen(self.current_pen)
            self.drawing_shape = RectShape(QRectF(posf, posf), pen)
            self.model.add_shape(self.drawing_shape)
        elif self.tool == "ellipse":
            pen = QtGui.QPen(self.current_pen)
            self.drawing_shape = EllipseShape(QRectF(posf, posf), pen)
            self.model.add_shape(self.drawing_shape)
        elif self.tool == "select":
            # select topmost shape under cursor
            self.model.clear_selection()
            s = self.model.shape_at(posf)
            if s:
                s.selected = True
                self.selected_shape = s
                self.dragging = True
                self.last_mouse_pos = posf
            else:
                self.selected_shape = None
            self.view.refresh()

    def canvas_mouse_move(self, pos: QPointF, event: QtGui.QMouseEvent):
        posf = QPointF(pos.x(), pos.y())
        if self.tool == "pen" and self.drawing_shape and isinstance(self.drawing_shape, Freehand):
            self.drawing_shape.path.lineTo(posf)
            self.view.refresh()
        elif self.tool in ("line", "rect", "ellipse") and self.drawing_shape:
            if isinstance(self.drawing_shape, Line):
                self.drawing_shape.p2 = posf
            elif isinstance(self.drawing_shape, RectShape) or isinstance(self.drawing_shape, EllipseShape):
                r = QRectF(self.start_pos, posf).normalized()
                self.drawing_shape.rect = r
            self.view.refresh()
        elif self.tool == "select" and self.dragging and self.selected_shape:
            dx = posf.x() - self.last_mouse_pos.x()
            dy = posf.y() - self.last_mouse_pos.y()
            self.selected_shape.move_by(dx, dy)
            self.last_mouse_pos = posf
            self.view.refresh()

    def canvas_mouse_release(self, pos: QPointF, event: QtGui.QMouseEvent):
        posf = QPointF(pos.x(), pos.y())
        if self.tool in ("pen", "line", "rect", "ellipse"):
            # finalize
            self.drawing_shape = None
            self.start_pos = None
            self.view.refresh()
        elif self.tool == "select":
            self.dragging = False
            self.last_mouse_pos = None

    def on_paint(self, painter: QtGui.QPainter):
        # draw all shapes
        for s in self.model.shapes:
            s.draw(painter)

# ----------------------------
# Main
# ----------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    model = CanvasModel()
    presenter = Presenter(model, None)
    main_win = MainWindow(presenter)
    presenter.view = main_win
    main_win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
