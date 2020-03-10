# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-09 17:50:25'

"""
设置自定义的 drag drop 事件
"""
import sys
from Qt import QtCore, QtGui, QtWidgets

class QHoverSignal(QtCore.QObject):
    """QHoverSignal 监听键盘输入事件
    """
    entered = QtCore.Signal(QtCore.QEvent)
    leaved = QtCore.Signal(QtCore.QEvent)
    moved = QtCore.Signal(QtCore.QEvent)
   
    def __init__(self,widget):
        super(QHoverSignal,self).__init__()
        widget.installEventFilter(self)

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.HoverEnter:
            self.entered.emit(event)
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.leaved.emit(event)
        elif event.type() == QtCore.QEvent.HoverMove:
            self.moved.emit(event)

        return False

def test():

    app = QtWidgets.QApplication(sys.argv)

    container = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    container.setLayout(layout)

    label = QtWidgets.QLabel("Test Label")
    button = QtWidgets.QPushButton("Test Button")
    layout.addWidget(label)
    layout.addWidget(button)

    signal = QHoverSignal(button)
    signal.entered.connect(lambda:sys.stdout.write("entered\n"))
    signal.leaved.connect(lambda:sys.stdout.write("leaved\n"))
    # signal.moved.connect(lambda:sys.stdout.write("moved\n"))

    container.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test()