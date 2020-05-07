# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 15:26:12'

"""
https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input
"""
import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == 'QtLib'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,'QtLib','_vendor','Qt')
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

from Qt import QtGui, QtWidgets, QtCore

class ICollapsibleWidget( object ):

    @classmethod
    def install(cls,btn,container,config=None):
        
        config = config if type(config) is dict else {}
        duration = config.get("duration",300)
        toggle_mark = config.get("toggle_mark",True)
        expand_callback = config.get("expand_callback")
        collapse_callback = config.get("collapse_callback")

        anim = QtCore.QPropertyAnimation(container, "maximumHeight")
        
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(container.sizeHint().height())
        anim.finished.connect(lambda:container.setMaximumHeight(16777215) if not btn.toggle else None)

        btn.toggle = False
        if toggle_mark:
            btn.setText(u"▼ %s"%btn.text())
        def toggleFn(btn,anim):
            if btn.toggle:
                btn.toggle = False
                anim.setDirection(QtCore.QAbstractAnimation.Forward)

                anim.setEndValue(cls.getHeightEndValue(container))
                anim.start()
                if toggle_mark:
                    btn.setText(u"▼%s"%btn.text()[1:])
                btn.setStyleSheet('font:normal')
                if expand_callback:
                    expand_callback()
            else:
                btn.toggle = True
                anim.setDirection(QtCore.QAbstractAnimation.Backward)
                anim.setEndValue(container.sizeHint().height())
                anim.start()
                if toggle_mark:
                    btn.setText(u"■%s"%btn.text()[1:])
                    btn.setStyleSheet('font:bold')
                if collapse_callback:
                    collapse_callback()

        func = lambda *args:toggleFn(btn,anim)
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

        widget.updateGeometry()
        prefer = widget.sizeHint().height()
        height = total_height - height
        return height if height > prefer else prefer

def test():
    app = QtWidgets.QApplication([])

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

    ICollapsibleWidget.install(button,container,{"toggle_mark":False})
    
    window.show()

    app.exec_()

if __name__ == "__main__":
    test()