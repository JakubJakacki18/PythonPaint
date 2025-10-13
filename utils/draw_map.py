from model.rectangle import Rectangle
from view.shape_renderer import ShapeRenderer

DRAW_MAP = {
    Rectangle: ShapeRenderer.draw_rectangle,
}