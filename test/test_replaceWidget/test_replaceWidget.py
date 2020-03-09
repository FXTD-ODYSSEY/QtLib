# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 20:41:45'

"""
ui替换测试
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__,'..','..','..')))

from QtLib import Qt
from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from Qt.QtCompat import loadUi
from Qt.QtCompat import QFileDialog
from Qt.QtCompat import wrapInstance

# from QtLib import util
from QtLib.util import replaceWidget

class AnimSpliterWindow(QtWidgets.QWidget):
    """
    AnimSpliterWindow 摄像机设置界面的摄像机Item
    """
    def __init__(self):
        super(AnimSpliterWindow,self).__init__()

        DIR = os.path.dirname(__file__)
        ui_file = os.path.join(DIR,"ui","test_replaceWidget.ui")
        loadUi(ui_file,self)

        # self.Character_Combo = replaceWidget(self.Character_Combo,QtWidgets.QLabel("Character_Combo"))
        self.Create_BTN = replaceWidget(self.Create_BTN,QtWidgets.QLabel("Create_BTN"))
        self.Clear_BTN = replaceWidget(self.Clear_BTN,QtWidgets.QLabel("Clear_BTN"))

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = AnimSpliterWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()