from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDialog
from view.color_window_ui import Ui_ColorWindow

class ColorDialog(QDialog, Ui_ColorWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._updating = False

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

        self.update_from_rgb()


    def update_from_rgb(self):
        if self._updating:
            return
        self._updating = True
        color = QColor(*self.get_rgb())
        self.update_cmyk(*color.getCmyk())
        self.update_hsv(*color.getHsv())
        self._updating = False
    def update_from_hsv(self):
        if self._updating:
            return
        self._updating = True
        color = QColor()
        color.setHsv(*self.get_hsv())
        self.update_cmyk(*color.getCmyk())
        self.update_rgb(*color.getRgb())
        self._updating = False
    def update_from_cmyk(self):
        if self._updating:
            return
        self._updating = True
        color = QColor()
        color.setCmyk(*self.get_cmyk())
        self.update_hsv(*color.getHsv())
        self.update_rgb(*color.getRgb())
        self._updating = False

    def update_rgb(self,r:int,g:int,b:int,_):
        self.rgbRedSpinBox.setValue(r)
        self.rgbGreenSpinBox.setValue(g)
        self.rgbBlueSpinBox.setValue(b)
    def update_hsv(self,h:int,s:int,v:int,_):
        self.hsvHueSpinBox.setValue(h)
        self.hsvSaturationSpinBox.setValue(s)
        self.hsvValueSpinBox.setValue(v)
    def update_cmyk(self,c:int,m:int,y:int,k:int,_):
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
        return h,s,v

    def get_cmyk(self) -> (int,int,int,int):
        c = self.cmykCyanSpinBox.value()
        m = self.cmykMagentaSpinBox.value()
        y = self.cmykYellowSpinBox.value()
        k = self.cmykBlackSpinBox.value()
        return c,m,y,k