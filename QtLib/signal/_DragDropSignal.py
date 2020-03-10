# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-09 17:50:25'

"""
设置自定义的 drag drop 事件
"""
import sys
from functools import partial
from Qt import QtCore, QtGui, QtWidgets
from voluptuous import Schema,Required

class QDragDropSignal(QtCore.QObject):
    """QDragDropSignal 监听键盘输入事件
    """
    pressed = QtCore.Signal()
    released = QtCore.Signal()
    config_schema = Schema({
        Required('focus', default=True): bool,
    })
    def __init__(self,widget,config={}):
        super(QDragDropSignal,self).__init__()

        config = self.config_schema(config)

        # NOTE 点击添加 focus 事件 | 用于触发键盘事件
        widget.dragMoveEvent = partial(self.dragMoveEvent ,widget.dragMoveEvent)
        
        self.widget = widget

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.KeyPress:
            KeySequence = QtGui.QKeySequence(event.key()+int(event.modifiers()))
            if KeySequence == QtGui.QKeySequence(self.key):
                self.pressed.emit()
        elif event.type() == QtCore.QEvent.KeyRelease:
            KeySequence = QtGui.QKeySequence(event.key()+int(event.modifiers()))
            if KeySequence == QtGui.QKeySequence(self.key):
                self.released.emit()

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

    ESignal = QKeyBoardSignal(label,"Ctrl + E ",config={'focus':False})
    ESignal.pressed.connect(lambda:sys.stdout.write("Ctrl + E\n"))

    TSignal = QKeyBoardSignal(button," Ctrl + T ")
    TSignal.pressed.connect(lambda:sys.stdout.write("Ctrl + T\n"))

    container.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test()