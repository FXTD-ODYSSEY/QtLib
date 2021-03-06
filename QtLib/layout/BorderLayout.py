#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from Qt import QtCore, QtWidgets


class ItemWrapper(object):
    def __init__(self, i, p):
        self.item = i
        self.position = p


class IBorderLayout(QtWidgets.QLayout):
    West, North, South, East, Center = range(5)
    MinimumSize, SizeHint = range(2)

    def __init__(self, parent=None, margin=0, spacing=-1):
        super(IBorderLayout, self).__init__(parent)

        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.list = []

    def __del__(self):
        l = self.takeAt(0)
        while l:
            l = self.takeAt(0)

    def addItem(self, item):
        self.add(item, IBorderLayout.West)

    def addWidget(self, widget, position):
        self.add(QtWidgets.QWidgetItem(widget), position)

    def expandingDirections(self):
        return QtCore.Qt.Horizontal | QtCore.Qt.Vertical

    def hasHeightForWidth(self):
        return False

    def count(self):
        return len(self.list)

    def itemAt(self, index):
        if index < len(self.list):
            return self.list[index].item

        return None

    def minimumSize(self):
        return self.calculateSize(IBorderLayout.MinimumSize)

    def setGeometry(self, rect):
        center = None
        eastWidth = 0
        westWidth = 0
        northHeight = 0
        southHeight = 0
        centerHeight = 0

        super(IBorderLayout, self).setGeometry(rect)

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position

            if position == IBorderLayout.North:
                item.setGeometry(QtCore.QRect(rect.x(), northHeight,
                        rect.width(), item.sizeHint().height()))    

                northHeight += item.geometry().height() + self.spacing()

            elif position == IBorderLayout.South:
                item.setGeometry(QtCore.QRect(item.geometry().x(),
                        item.geometry().y(), rect.width(),
                        item.sizeHint().height()))

                southHeight += item.geometry().height() + self.spacing()

                item.setGeometry(QtCore.QRect(rect.x(),
                        rect.y() + rect.height() - southHeight + self.spacing(),
                        item.geometry().width(), item.geometry().height()))

            elif position == IBorderLayout.Center:
                center = wrapper

        centerHeight = rect.height() - northHeight - southHeight

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position

            if position == IBorderLayout.West:
                item.setGeometry(QtCore.QRect(rect.x() + westWidth,
                        northHeight, item.sizeHint().width(), centerHeight))    

                westWidth += item.geometry().width() + self.spacing()

            elif position == IBorderLayout.East:
                item.setGeometry(QtCore.QRect(item.geometry().x(),
                        item.geometry().y(), item.sizeHint().width(),
                        centerHeight))

                eastWidth += item.geometry().width() + self.spacing()

                item.setGeometry(QtCore.QRect(rect.x() + rect.width() - eastWidth + self.spacing(),
                        northHeight, item.geometry().width(),
                        item.geometry().height()))

        if center:
            center.item.setGeometry(QtCore.QRect(westWidth, northHeight,
                    rect.width() - eastWidth - westWidth, centerHeight))

    def sizeHint(self):
        return self.calculateSize(IBorderLayout.SizeHint)

    def takeAt(self, index):
        if index >= 0 and index < len(self.list):
            layoutStruct = self.list.pop(index)
            return layoutStruct.item

        return None

    def add(self, item, position):
        self.list.append(ItemWrapper(item, position))

    def calculateSize(self, sizeType):
        totalSize = QtCore.QSize()

        for wrapper in self.list:
            position = wrapper.position
            itemSize = QtCore.QSize()

            if sizeType == IBorderLayout.MinimumSize:
                itemSize = wrapper.item.minimumSize()
            else: # sizeType == BorderLayout.SizeHint
                itemSize = wrapper.item.sizeHint()

            if position in (IBorderLayout.North, IBorderLayout.South, IBorderLayout.Center):
                totalSize.setHeight(totalSize.height() + itemSize.height())

            if position in (IBorderLayout.West, IBorderLayout.East, IBorderLayout.Center):
                totalSize.setWidth(totalSize.width() + itemSize.width())

        return totalSize


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        centralWidget = QtWidgets.QTextBrowser()
        centralWidget.setPlainText("Central widget")

        layout = IBorderLayout()
        layout.addWidget(centralWidget, IBorderLayout.Center)

        # Because BorderLayout doesn't call its super-class addWidget() it
        # doesn't take ownership of the widgets until setLayout() is called.
        # Therefore we keep a local reference to each label to prevent it being
        # garbage collected too soon.
        label_n = self.createLabel("North")
        layout.addWidget(label_n, IBorderLayout.North)

        label_w = self.createLabel("West")
        layout.addWidget(label_w, IBorderLayout.West)

        label_e1 = self.createLabel("East 1")
        layout.addWidget(label_e1, IBorderLayout.East)

        label_e2 = self.createLabel("East 2")
        layout.addWidget(label_e2, IBorderLayout.East)

        label_s = self.createLabel("South")
        layout.addWidget(label_s, IBorderLayout.South)

        self.setLayout(layout)

        self.setWindowTitle("Border Layout")

    def createLabel(self, text):
        label = QtWidgets.QLabel(text)
        label.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        return label


def test():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())    

if __name__ == '__main__':
    test()