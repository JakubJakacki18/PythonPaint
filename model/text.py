from model.pen import Pen
from model.point import Point
from model.rectangle import Rectangle


class Text(Rectangle):
    def __init__(self,pen: Pen, p1 : Point, p2: Point):
        super().__init__(pen,p1,p2)
        self.text = str()

    def set_text(self,text:str):
        self.text += text

    def delete_last_character(self):
        self.text = self.text[:-1]