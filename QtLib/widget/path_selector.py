# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-05-31 08:01:14'

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets


class PathSelector(QtWidgets.QWidget):
    def __init__(self, parent=None, label=u"文件路径", button_text=u"浏览"):
        super(PathSelector, self).__init__(parent=parent)

        self.label = QtWidgets.QLabel(label)

        self.line = QtWidgets.QLineEdit()

        self.button = QtWidgets.QPushButton()
        self.button.setText(button_text)
        self.button.clicked.connect(self.browser_file)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        layout.addWidget(self.button)

    def browser_file(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Browser Folder')

        self.line.setText(path) if path else None


def test():
    app = QtWidgets.QApplication([])
    widget = PathSelector()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    test()
