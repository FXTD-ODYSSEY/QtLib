# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-09 17:13:54'

"""

"""

from Qt import QtGui
from Qt import QtWidgets
from Qt import QtCore

class QOverLayWidget(QtWidgets.QWidget):

    def __init__(self, parent,config={}):
        super(QOverLayWidget,self).__init__(parent)
        transparent = config.get("transparent") if config.get("transparent") else True
        if transparent:
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
            self.setWindowFlags(QtCore.Qt.WindowTransparentForInput | QtCore.Qt.FramelessWindowHint)
            self.setFocusPolicy( QtCore.Qt.NoFocus )

        self.config = config
        parent.installEventFilter(self)

    def paintEvent(self, event):
        
        # NOTE https://stackoverflow.com/questions/51687692/how-to-paint-roundedrect-border-outline-the-same-width-all-around-in-pyqt-pysi
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)   

        rectPath = QtGui.QPainterPath()
        height = self.height() - 4
        rectF = QtCore.QRectF(2, 2, self.width()-4, height)
        
        # NOTE 绘制边界颜色
        border = self.config.get("border") if self.config.get("border") else True
        if border:
            border_color = self.config.get("border_color") if self.config.get("border_color") else QtGui.QColor(255, 0, 0, 255) 
            border_line = self.config.get("border_line") if self.config.get("border_line") else QtCore.Qt.SolidLine
            border_cap = self.config.get("border_cap") if self.config.get("border_cap") else QtCore.Qt.RoundCap
            border_round = self.config.get("border_round") if self.config.get("border_round") else QtCore.Qt.RoundJoin
            border_bevel = self.config.get("border_bevel") if self.config.get("border_bevel") else 15
            border_pen = self.config.get("border_pen") if self.config.get("border_pen") else False
                
            rectPath.addRoundedRect(rectF, border_bevel, border_bevel)
            painter.setPen(border_pen if border_pen else QtGui.QPen(border_color, 2, border_line ,border_cap, border_round))
            painter.drawPath(rectPath)

        rect = self.config.get("rect") if self.config.get("rect") else True
        if rect:
            rect_color = self.config.get("rect_color") if self.config.get("rect_color") else QtGui.QColor(0, 255, 0, 125) 
            rect_bevel = self.config.get("rect_bevel") if self.config.get("rect_bevel") else 15
            # NOTE 绘制背景颜色
            painter.setBrush(rect_color)
            painter.drawRoundedRect(rectF, rect_bevel, rect_bevel)
    
    def eventFilter(self, obj, event):
        if not obj.isWidgetType():
            return False
        
        if self.isVisible():
            self.setGeometry(obj.rect())
        elif event.type() == QtCore.QEvent.Resize:
            self.setGeometry(obj.rect())

        return False

def test():
    app = QtWidgets.QApplication([])
    button = QtWidgets.QPushButton("click")
    frame = QOverLayWidget(button)
    frame.hide()
    button.clicked.connect(lambda:frame.setVisible(not frame.isVisible()))
    button.show()
    app.exec_()

if __name__ == "__main__":
    test()