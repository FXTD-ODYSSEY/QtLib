# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-09 17:50:25'

"""
设置自定义的键盘触发事件
"""
import sys
from functools import partial
from Qt import QtCore, QtGui, QtWidgets


class ClickTimer(QtCore.QTimer):

    clicked = QtCore.Signal()
    doubleClicked = QtCore.Signal()

    def __init__(self,dbTime=200):
        super(ClickTimer,self).__init__()
        self.timer_count = 0
        self.setInterval(dbTime)
        self.timeout.connect(self.timerEvent)

    def timerEvent(self,event):
        self.timer_count += 1
        if self.timer_count > 1:
            self.stop()
            self.clicked.emit()
    
    def trigger(self):
        if not self.isActive():
            self.start()
        else:
            # Note 说明双击了
            self.stop()
            self.doubleClicked.emit()

    def stop(self):
        self.timer_count = 0
        super(ClickTimer,self).stop()


class QMouseClickSignal(QtCore.QObject):
    """addExecuteShortcut 监听鼠标中键事件
    """
    LClicked = QtCore.Signal()
    MClicked = QtCore.Signal()
    RClicked = QtCore.Signal()
    DLClicked = QtCore.Signal()
    DMClicked = QtCore.Signal()
    DRClicked = QtCore.Signal()

    def __init__(self,widget,dbTime=100):
        super(QMouseClickSignal,self).__init__()
        self.setParent(widget)

        self.leftTimer = ClickTimer(dbTime)
        self.leftTimer.clicked.connect(lambda: self.LClicked.emit())
        self.leftTimer.doubleClicked.connect(lambda: self.DLClicked.emit())
        
        self.midTimer = ClickTimer(dbTime)
        self.midTimer.clicked.connect(lambda: self.MClicked.emit())
        self.midTimer.doubleClicked.connect(lambda: self.DMClicked.emit())
        
        self.rightTimer = ClickTimer(dbTime)
        self.rightTimer.clicked.connect(lambda: self.RClicked.emit())
        self.rightTimer.doubleClicked.connect(lambda: self.DRClicked.emit())
        
        if isinstance(widget,QtWidgets.QWidget):
            widget.mousePressEvent = partial(self.mousePressEvent,widget.mousePressEvent)
        else:
            # NOTE QWidget 自身带有双击事件监测，因此这里用 eventFilter 要变成三击才能触发
            widget.installEventFilter(self)

    def mousePressEvent(self,superFunc,event):
        superFunc(event)
        # Note 点击事件
        if event.button() == QtCore.Qt.LeftButton:
            self.leftTimer.trigger()
        if event.button() == QtCore.Qt.MidButton:
            self.midTimer.trigger()
        if event.button() == QtCore.Qt.RightButton:
            self.rightTimer.trigger()

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self.leftTimer.trigger()
            if event.button() == QtCore.Qt.MidButton:
                self.midTimer.trigger()
            if event.button() == QtCore.Qt.RightButton:
                self.rightTimer.trigger()
        return False

def test():
    app = QtWidgets.QApplication(sys.argv)

    label = QtWidgets.QLabel("Click Test")

    mouseSignal = QMouseClickSignal(label)
    mouseSignal.MClicked.connect(lambda:sys.stdout.write("middle click\n"))
    mouseSignal.DMClicked.connect(lambda:sys.stdout.write("double middle click\n"))
    mouseSignal.LClicked.connect(lambda:sys.stdout.write("left click\n"))
    mouseSignal.DLClicked.connect(lambda:sys.stdout.write("double left click\n"))
    mouseSignal.RClicked.connect(lambda:sys.stdout.write("right click\n"))
    mouseSignal.DRClicked.connect(lambda:sys.stdout.write("double right click\n"))

    label.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test()