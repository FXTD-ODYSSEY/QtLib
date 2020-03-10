# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-09 17:50:25'

"""
设置自定义的键盘触发事件
通过传入的 event.modifiers 还可以配合 辅助按键来触发不同的点击事件
"""
import sys
from functools import partial
from Qt import QtCore, QtGui, QtWidgets

class QMouseClickSignal(QtCore.QObject):
    """QMouseClickSignal 监听鼠标点击信号
    """
    # NOTE 点击事件
    LClicked   = QtCore.Signal(QtCore.QEvent)
    DLClicked  = QtCore.Signal(QtCore.QEvent)
    MClicked   = QtCore.Signal(QtCore.QEvent)
    DMClicked  = QtCore.Signal(QtCore.QEvent)
    RClicked   = QtCore.Signal(QtCore.QEvent)
    DRClicked  = QtCore.Signal(QtCore.QEvent)
    X1Clicked  = QtCore.Signal(QtCore.QEvent)
    DX1Clicked = QtCore.Signal(QtCore.QEvent)
    X2Clicked  = QtCore.Signal(QtCore.QEvent)
    DX2Clicked = QtCore.Signal(QtCore.QEvent)

    # NOTE 松开事件
    LReleased  = QtCore.Signal(QtCore.QEvent)
    MReleased  = QtCore.Signal(QtCore.QEvent)
    RReleased  = QtCore.Signal(QtCore.QEvent)
    X1Released = QtCore.Signal(QtCore.QEvent)
    X2Released = QtCore.Signal(QtCore.QEvent)

    def __init__(self,widget):
        super(QMouseClickSignal,self).__init__()
        self.setParent(widget)

        self.releaseSingal = {
            QtCore.Qt.LeftButton:self.LReleased.emit,
            QtCore.Qt.MidButton:self.MReleased.emit,
            QtCore.Qt.RightButton:self.RReleased.emit,
            QtCore.Qt.XButton1:self.X1Released.emit,
            QtCore.Qt.XButton2:self.X2Released.emit,
        }
        
        self.clickSingal = {
            QtCore.Qt.LeftButton:self.LClicked.emit,
            QtCore.Qt.MidButton:self.MClicked.emit,
            QtCore.Qt.RightButton:self.RClicked.emit,
            QtCore.Qt.XButton1:self.X1Clicked.emit,
            QtCore.Qt.XButton2:self.X2Clicked.emit,
        }

        self.DbClickSingal = {
            QtCore.Qt.LeftButton:self.DLClicked.emit,
            QtCore.Qt.MidButton:self.DMClicked.emit,
            QtCore.Qt.RightButton:self.DRClicked.emit,
            QtCore.Qt.XButton1:self.DX1Clicked.emit,
            QtCore.Qt.XButton2:self.DX2Clicked.emit,
        }

        widget.installEventFilter(self)

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.clickSingal.get(event.button())(event)
        elif event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
            self.DbClickSingal.get(event.button())(event)
        elif event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            self.releaseSingal.get(event.button())(event)
        return False

def test():
    app = QtWidgets.QApplication(sys.argv)

    label = QtWidgets.QLabel("Click Test")

    mouseSignal = QMouseClickSignal(label)
    mouseSignal.LClicked.connect(lambda e:sys.stdout.write("left click\n"))
    mouseSignal.LReleased.connect(lambda e:sys.stdout.write("left release\n"))
    mouseSignal.DLClicked.connect(lambda e:sys.stdout.write("double left click\n"))
    mouseSignal.MClicked.connect(lambda e:sys.stdout.write("middle click\n"))
    mouseSignal.DMClicked.connect(lambda e:sys.stdout.write("double middle click\n"))
    mouseSignal.RClicked.connect(lambda e:sys.stdout.write("right click\n"))
    mouseSignal.DRClicked.connect(lambda e:sys.stdout.write("double right click\n"))

    label.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test()