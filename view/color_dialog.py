from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDialog
from view.color_window_ui import Ui_ColorWindow
from view.cone_gl_widget import ConeGlWidget
from view.cube_gl_widget import CubeGlWidget


class ColorDialog(QDialog, Ui_ColorWindow):
    def __init__(self,presenter, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._updating = False
        self.presenter = presenter

        self.rgbRedSpinBox.valueChanged.connect(self.update_from_rgb)
        self.rgbGreenSpinBox.valueChanged.connect(self.update_from_rgb)
        self.rgbBlueSpinBox.valueChanged.connect(self.update_from_rgb)

        self.hsvHueSpinBox.valueChanged.connect(self.update_from_hsv)
        self.hsvSaturationSpinBox.valueChanged.connect(self.update_from_hsv)
        self.hsvValueSpinBox.valueChanged.connect(self.update_from_hsv)

        self.cmykCyanSpinBox.valueChanged.connect(self.update_from_cmyk)
        self.cmykMagentaSpinBox.valueChanged.connect(self.update_from_cmyk)
        self.cmykYellowSpinBox.valueChanged.connect(self.update_from_cmyk)
        self.cmykBlackSpinBox.valueChanged.connect(self.update_from_cmyk)
        self.cubeOpenGlWidget.colorPicked.connect(self.presenter.on_color_picked_float)
        self.coneOpenGlWidget.colorPicked.connect(self.presenter.on_color_picked_float)




    def update_from_rgb(self):
        if self._updating:
            return
        self._updating = True
        color = QColor(*self.get_rgb())
        self.update_cmyk(*color.getCmyk())
        self.update_hsv(*color.getHsv())
        self.presenter.on_color_picked(color.getRgb())
        self._updating = False

    def update_from_hsv(self):
        if self._updating:
            return
        self._updating = True
        color = QColor()
        color.setHsv(*self.get_hsv())
        self.update_cmyk(*color.getCmyk())
        self.update_rgb(*color.getRgb())
        self.presenter.on_color_picked(color.getRgb())
        self._updating = False
    def update_from_cmyk(self):
        if self._updating:
            return
        self._updating = True
        color = QColor()
        color.setCmyk(*self.get_cmyk())
        self.update_hsv(*color.getHsv())
        self.update_rgb(*color.getRgb())
        self.presenter.on_color_picked(color.getRgb())
        self._updating = False

    def update_rgb(self,r:int,g:int,b:int,_):
        self.rgbRedSpinBox.setValue(r)
        self.rgbGreenSpinBox.setValue(g)
        self.rgbBlueSpinBox.setValue(b)

    def update_hsv(self,h:int,s:int,v:int,_):
        print("update hsv",h,s,v,_)
        proc = lambda x: int(x/255*100)
        s_proc=proc(s)
        v_proc=proc(v)

        self.hsvHueSpinBox.setValue(h)
        self.hsvSaturationSpinBox.setValue(s_proc)
        self.hsvValueSpinBox.setValue(v_proc)

    def update_cmyk(self,c:int,m:int,y:int,k:int,_):
        print("update cmyk:",c,m,y,k)
        self.cmykCyanSpinBox.setValue(c)
        self.cmykMagentaSpinBox.setValue(m)
        self.cmykYellowSpinBox.setValue(y)
        self.cmykBlackSpinBox.setValue(k)

    def get_rgb(self) -> (int,int,int):
        r = self.rgbRedSpinBox.value()
        g = self.rgbGreenSpinBox.value()
        b = self.rgbBlueSpinBox.value()
        return r,g,b

    def get_hsv(self) -> (int,int,int):
        h = self.hsvHueSpinBox.value()
        s = self.hsvSaturationSpinBox.value()
        v = self.hsvValueSpinBox.value()
        proc = lambda x: int(x/100*255)
        s_proc = proc(s)
        v_proc = proc(v)
        print("hsv",h,s_proc,v_proc)
        return h,s_proc,v_proc

    def get_cmyk(self) -> (int,int,int,int):
        c = self.cmykCyanSpinBox.value()
        m = self.cmykMagentaSpinBox.value()
        y = self.cmykYellowSpinBox.value()
        k = self.cmykBlackSpinBox.value()
        proc = lambda x: int(x/100*255)
        return proc(c),proc(m),proc(y),proc(k)

    def init_color(self,r:int,g:int,b:int):
        color = QColor(r,g,b)
        self.update_cmyk(*color.getCmyk())
        self.update_hsv(*color.getHsv())
        self.update_rgb(*color.getRgb())


