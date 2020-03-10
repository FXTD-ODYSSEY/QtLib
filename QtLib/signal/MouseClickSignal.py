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


class ClickTimer(QtCore.QTimer):

    clicked = QtCore.Signal(QtCore.QEvent)
    doubleClicked = QtCore.Signal(QtCore.QEvent)

    def __init__(self,dbTime=200):
        super(ClickTimer,self).__init__()
        self.event = None
        self.timer_count = 0
        self.setInterval(dbTime)
        self.timeout.connect(self.timerEvent)

    def timerEvent(self,event):
        self.timer_count += 1
        if self.timer_count > 1:
            self.stop()
            self.clicked.emit(self.event)
    
    def trigger(self,event):
        self.event = event
        if not self.isActive():
            self.start()
        else:
            # Note 说明双击了
            self.stop()
            self.doubleClicked.emit(event)

    def stop(self):
        self.timer_count = 0
        super(ClickTimer,self).stop()


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

    def __init__(self,widget,dbTime=100):
        super(QMouseClickSignal,self).__init__()
        self.setParent(widget)

        self.leftTimer = ClickTimer(dbTime)
        self.leftTimer.clicked.connect(lambda e: self.LClicked.emit(e))
        self.leftTimer.doubleClicked.connect(lambda e: self.DLClicked.emit(e))
        
        self.midTimer = ClickTimer(dbTime)
        self.midTimer.clicked.connect(lambda e: self.MClicked.emit(e))
        self.midTimer.doubleClicked.connect(lambda e: self.DMClicked.emit(e))
        
        self.rightTimer = ClickTimer(dbTime)
        self.rightTimer.clicked.connect(lambda e: self.RClicked.emit(e))
        self.rightTimer.doubleClicked.connect(lambda e: self.DRClicked.emit(e))

        self.x1Timer = ClickTimer(dbTime)
        self.x1Timer.clicked.connect(lambda e: self.X1Clicked.emit(e))
        self.x1Timer.doubleClicked.connect(lambda e: self.DX1Clicked.emit(e))

        self.x2Timer = ClickTimer(dbTime)
        self.x2Timer.clicked.connect(lambda e: self.X2Clicked.emit(e))
        self.x2Timer.doubleClicked.connect(lambda e: self.DX2Clicked.emit(e))
        
        self.clickSingal = {
            QtCore.Qt.LeftButton:self.leftTimer.trigger,
            QtCore.Qt.MidButton:self.midTimer.trigger,
            QtCore.Qt.RightButton:self.rightTimer.trigger,
            QtCore.Qt.XButton1:self.x1Timer.trigger,
            QtCore.Qt.XButton2:self.x2Timer.trigger,
        }

        self.releaseSingal = {
            QtCore.Qt.LeftButton:self.LReleased.emit,
            QtCore.Qt.MidButton:self.MReleased.emit,
            QtCore.Qt.RightButton:self.RReleased.emit,
            QtCore.Qt.XButton1:self.X1Released.emit,
            QtCore.Qt.XButton2:self.X2Released.emit,
        }

        if isinstance(widget,QtWidgets.QWidget):
            widget.mousePressEvent = partial(self.mousePressEvent,widget.mousePressEvent)
            widget.mouseReleaseEvent = partial(self.mouseReleaseEvent,widget.mouseReleaseEvent)
        else:
            # NOTE QWidget 自身带有双击事件监测，因此这里用 eventFilter 会变成三击才能触发
            widget.installEventFilter(self)

    def mousePressEvent(self,superFunc,event):
        superFunc(event)
        # Note 点击事件
        self.clickSingal.get(event.button())(event)
    
    def mouseReleaseEvent(self,superFunc,event):
        superFunc(event)
        self.releaseSingal.get(event.button())(event)

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.clickSingal.get(event.button())(event)
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