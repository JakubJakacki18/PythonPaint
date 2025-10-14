from model.ellipse import Ellipse
from model.free_draw import FreeDraw
from model.line import Line
from model.rectangle import Rectangle
from model.triangle import Triangle
from view.shape_renderer import ShapeRenderer

DRAW_MAP = {
    Rectangle: ShapeRenderer.draw_rectangle,
    Ellipse: ShapeRenderer.draw_ellipse,
    Triangle: ShapeRenderer.draw_triangle,
    Line: ShapeRenderer.draw_line,
    FreeDraw : ShapeRenderer.draw_free

}