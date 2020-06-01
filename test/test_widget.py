import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__,"..","..")))
from QtLib.widget import CompleterComboBox
from QtLib.widget import CollapsibleWidget
from QtLib.widget import OverLayWidget
from QtLib.widget import ProgressDialog
from QtLib.widget import IFileWatcherList

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

app = QtWidgets.QApplication([])
watcher = IFileWatcherList(fileFilter=[".ma",".mb"])
watcher.show()
app.exec_()
# CollapsibleWidget.test()
# FileWatcherList.test()
# ExtendedComboBox.test()
# CompleterComboBox.test()