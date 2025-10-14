from model.pen import Pen
from model.point import Point
from model.shape import Shape


class Text(Shape):
    def __init__(self,pen: Pen, p1 : Point):
        super().__init__(pen)
        self.text = str()
        self.p1 = p1

    def set_text(self,text:str):
        self.text += text

    def delete_last_character(self):
        self.text = self.text[:-1]