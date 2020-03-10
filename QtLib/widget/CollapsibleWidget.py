# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 15:26:12'

"""
https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input
"""
from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

from voluptuous import Schema,Required
from types import FunctionType
class ICollapsibleWidget( object ):
    config_schema = Schema({
        Required('duration', default=300): int,
        Required('toggle_mark', default=True): bool,
        'expand_callback' :FunctionType,
        'collapse_callback': FunctionType,
    })

    @staticmethod
    def install(btn,container,config={}):
        
        config = ICollapsibleWidget.config_schema(config)
        duration = config.get("duration")
        toggle_mark = config.get("toggle_mark")
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

                anim.setEndValue(ICollapsibleWidget.getHeightEndValue(container))
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

        func = lambda x:toggleFn(btn,anim)
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