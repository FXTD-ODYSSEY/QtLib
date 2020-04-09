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

class IKeyBoardSignal(QtCore.QObject):
    """IKeyBoardSignal 监听键盘输入信号
    """
    pressed = QtCore.Signal(QtCore.QEvent)
    released = QtCore.Signal(QtCore.QEvent)

    def __init__(self,widget,key,config=None):
        super(IKeyBoardSignal,self).__init__()

        self.config = config if type(config) is dict else {}

        widget.installEventFilter(self)

        # NOTE 清理空格否则 KeySequence 不匹配
        self.key = key.replace(" ","")

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.KeyPress:
            KeySequence = QtGui.QKeySequence(event.key()+int(event.modifiers()))
            if KeySequence == QtGui.QKeySequence(self.key):
                self.pressed.emit(event)
        elif event.type() == QtCore.QEvent.KeyRelease:
            KeySequence = QtGui.QKeySequence(event.key()+int(event.modifiers()))
            if KeySequence == QtGui.QKeySequence(self.key):
                self.released.emit(event)
        elif event.type() == QtCore.QEvent.MouseButtonPress and self.config.get('focus',True):
            if not reciever.hasFocus():
                reciever.setFocus()

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

    ESignal = IKeyBoardSignal(label,"left",config={'focus':True})
    ESignal.pressed.connect(lambda:sys.stdout.write("Ctrl + E\n"))

    TSignal = IKeyBoardSignal(button," Ctrl + T ")
    TSignal.pressed.connect(lambda:sys.stdout.write("Ctrl + T\n"))

    container.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test()