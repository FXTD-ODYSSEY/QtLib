# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-05-31 11:24:55'

from Qt import QtCore, QtWidgets


class IDivider(QtWidgets.QFrame):
    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(IDivider, self).__init__(parent)
        self.setFrameShape(
            QtWidgets.QFrame.HLine if QtCore.Qt.Horizontal else QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


