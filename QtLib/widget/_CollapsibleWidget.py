# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 15:26:12'

"""
https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input
"""
from .. import Qt
from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

import sys
from functools import partial


class CollapsibleWidget( QtWidgets.QWidget ):
    def __init__(self):
        super( CollapsibleWidget, self ).__init__()
        
    @staticmethod
    def install(btn,container,duration=300,expand_callback=None,collapse_callback=None):

        maximumHeight = container.maximumHeight()

        anim = QtCore.QPropertyAnimation(container, "maximumHeight")
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(container.sizeHint().height())
        anim.finished.connect(lambda:container.setMaximumHeight(maximumHeight) if not btn._toggle else None)

        btn._toggle = False
        btn.setText(u"▼ %s"%btn.text())

        def toggleFn(btn,anim):
            if btn._toggle:
                btn._toggle = False
                anim.setDirection(QtCore.QAbstractAnimation.Forward)

                anim.setEndValue(CollapsibleWidget.getHeightEndValue(container))
                anim.start()
                btn.setText(u"▼%s"%btn.text()[1:])
                btn.setStyleSheet('font:normal')
                if expand_callback:
                    expand_callback()
            else:
                btn._toggle = True
                anim.setDirection(QtCore.QAbstractAnimation.Backward)
                anim.setEndValue(container.sizeHint().height())
                anim.start()
                btn.setText(u"■%s"%btn.text()[1:])
                btn.setStyleSheet('font:bold')
                if collapse_callback:
                    collapse_callback()

        func = partial(toggleFn,btn,anim)
        btn.clicked.connect(func)
        return func

    @staticmethod
    def getHeightEndValue(widget):

        parent = widget.parent()
        total_height = parent.height()

        height = 0
        for child in parent.children():
            if child == widget or not hasattr(child,"height"):
                continue
            
            height += child.height()

        prefer = widget.sizeHint().height()
        height = total_height - height
        return height if height > prefer else prefer

def test():
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    window.setLayout(layout)

    button = QtWidgets.QPushButton("test")
    button.setCheckable(True)
    layout.addWidget(button)

    container = QtWidgets.QWidget()
    container_layout = QtWidgets.QVBoxLayout()
    container.setLayout(container_layout)

    for i in range(5):
        btn = QtWidgets.QPushButton("test - %s" % i)
        container_layout.addWidget(btn)

    layout.addWidget(container)

    CollapsibleWidget.install(button,container)
    
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    test()