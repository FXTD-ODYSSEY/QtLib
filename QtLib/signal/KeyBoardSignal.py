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

class QKeyBoardSignal(QtCore.QObject):
    """AddExecuteShortcut 监听键盘输入事件
    """
    keyTriggered = QtCore.Signal()
    def __init__(self,widget,key):
        super(QKeyBoardSignal,self).__init__()
        widget.installEventFilter(self)

        # NOTE 点击添加 focus 事件 | 用于触发键盘事件
        widget.mousePressEvent = partial(self.mousePressEvent,widget.mousePressEvent)
        
        self.widget = widget
        self.key = key.replace(" ","")

    def mousePressEvent(self,superFunc,event):
        superFunc(event)
        if not self.widget.hasFocus():
            self.widget.setFocus()
        
    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            KeySequence = QtGui.QKeySequence(key+int(event.modifiers()))
            if KeySequence == QtGui.QKeySequence(self.key):
                self.keyTriggered.emit()

        return False

def test():

    app = QtWidgets.QApplication(sys.argv)

    container = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    container.setLayout(layout)

    label = QtWidgets.QLabel("Ctrl+E")
    button = QtWidgets.QPushButton("Ctrl+T")
    layout.addWidget(label)
    layout.addWidget(button)

    ESignal = QKeyBoardSignal(label,"Ctrl + E ")
    ESignal.keyTriggered.connect(lambda:sys.stdout.write("Ctrl + E\n"))

    TSignal = QKeyBoardSignal(button," Ctrl + T ")
    TSignal.keyTriggered.connect(lambda:sys.stdout.write("Ctrl + T\n"))

    container.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test()