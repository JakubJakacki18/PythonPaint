from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPointF

from old_model.canvas_model import CanvasModel
from old_model.free_hand import Freehand
from old_model.line import Line
from view.main_window import Ui_MainWindow

class Presenter:
    def __init__(self, model: CanvasModel, view: Ui_MainWindow ):
        self.model = model
        self.view = view
        self.tool = ""  # pen, line, rect, ellipse, select
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
        # elif self.tool == "rect":
        #     pen = QtGui.QPen(self.current_pen)
        #     self.drawing_shape = RectShape(QRectF(posf, posf), pen)
        #     self.model.add_shape(self.drawing_shape)
        # elif self.tool == "ellipse":
        #     pen = QtGui.QPen(self.current_pen)
        #     self.drawing_shape = EllipseShape(QRectF(posf, posf), pen)
        #     self.model.add_shape(self.drawing_shape)
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
        #     elif isinstance(self.drawing_shape, RectShape) or isinstance(self.drawing_shape, EllipseShape):
        #         r = QRectF(self.start_pos, posf).normalized()
        #         self.drawing_shape.rect = r
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


