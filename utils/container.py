from dependency_injector import containers, providers

from model.canvas_model import CanvasModel
from model.ellipse import Ellipse
from model.free_draw import FreeDraw
from model.line import Line
from model.rectangle import Rectangle
from model.text import Text
from model.triangle import Triangle
from presenter import Presenter
from utils.tools import Tools
from view.main_window import View


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    model = providers.Singleton(CanvasModel)

    rectangle_factory = providers.Factory(Rectangle)
    line_factory = providers.Factory(Line)
    ellipse_factory = providers.Factory(Ellipse)
    text_factory = providers.Factory(Text)
    triangle_factory = providers.Factory(Triangle)
    free_draw_factory = providers.Factory(FreeDraw)

    shape_factories = providers.Object( {
        Tools.FREE_DRAW: free_draw_factory,
        Tools.TEXT: text_factory,
        Tools.RECTANGLE: rectangle_factory,
        Tools.LINE: line_factory,
        Tools.TRIANGLE: triangle_factory,
        Tools.ELLIPSE: ellipse_factory,
    })

    # Presenter
    presenter = providers.Singleton(
        Presenter,
        model=model,
        view =None,
        shape_factories=shape_factories,
    )

    view = providers.Singleton(View,presenter)