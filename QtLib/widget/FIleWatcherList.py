# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-22 21:07:36'

"""

"""
import os
import sys
import json
import shutil
import hashlib
import tempfile
import traceback
from functools import partial

try:
    from Qt import QtGui
    from Qt import QtCore
    from Qt import QtWidgets
    from Qt.QtCompat import wrapInstance,QFileDialog
except:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    from PySide2.QtWidgets import QFileDialog

from ProgressDialog import IProgressDialog

class FileListWidget(QtWidgets.QListWidget):

    def __init__(self, parent , fileFilter=None):
        super(FileListWidget, self).__init__(parent)
        self.watcher = parent
        self.fileFilter = fileFilter
        
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.setAcceptDrops(True)

    def dragEnterEvent(self,event):
        u'''
        dragEnterEvent 文件拖拽的进入事件
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现文件拖拽加载效果
        
        Arguments:
            event {QDragEnterEvent} --  dropEnterEvent 固定的事件参数
        
        '''
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self,event):
        u'''
        dropEvent 拖拽文件添加item
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现文件拖拽加载效果
        
        Arguments:
            event {QDropEvent} -- dropEvent 固定的事件参数
        
        '''
        # Note 获取拖拽文件的地址
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path = (url.toLocalFile())
                _,ext = os.path.splitext(path)
                # Note 过滤已有的路径
                if ext in self.fileFilter or "*" in self.fileFilter:
                    self.watcher.addItem(path)
            
            self.watcher.saveJson()
            
        else:
            event.ignore()

    def dragMoveEvent(self,event):
        u'''
        dragMoveEvent 文件拖拽的移动事件
        
        # Note https://stackoverflow.com/questions/4151637/pyqt4-drag-and-drop-files-into-qlistwidget
        参考上述网址的 drag and drop 实现图片拖拽加载效果
        
        Arguments:
            event {QDragMoveEvent} --  dragMoveEvent 固定的事件参数
        
        '''
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    # def addItem(self,item):
    #     _item = item.text() if type(item) is QtWidgets.QListWidgetItem else item
    #     if not self.findItems(_item, QtCore.Qt.MatchContains):
    #         super(FileListWidget,self).addItem(item)

class IFileWatcherList(QtWidgets.QWidget):

    old_md5_data = {}
    new_md5_data = {}

    def __init__(self,jsonName=None,fileFilter=None,excludeArray=None,getCurrentCallback=None):
        super(IFileWatcherList, self).__init__()
        
        self.jsonName = jsonName if jsonName else "%s.json" % self.__class__.__name__
        self.fileFilter = fileFilter if isinstance(fileFilter,list) else ["*"]
        self.File_List = FileListWidget(self,self.fileFilter)
        self.File_List.customContextMenuRequested.connect(
            self.fileItemRightClickEvent)
        
        self.Root_BTN = QtWidgets.QPushButton(u'获取文件目录路径', self)
        self.Root_BTN.clicked.connect(self.handleSetDirectory)
        self.File_BTN = QtWidgets.QPushButton(u'获取文件', self)
        self.File_BTN.clicked.connect(self.getFile)

        self.Button_Layout = QtWidgets.QHBoxLayout()
        self.Button_Layout.addWidget(self.Root_BTN)
        self.Button_Layout.addWidget(self.File_BTN)
        
        if callable(getCurrentCallback):
            self.Current_BTN = QtWidgets.QPushButton(u'获取当前打开的文件', self)
            self.Current_BTN.clicked.connect(partial(getCurrentCallback,self.File_List))
            self.Button_Layout.addWidget(self.Current_BTN)

        self.Main_Layout = QtWidgets.QVBoxLayout()
        self.Main_Layout.addWidget(self.File_List)
        self.Main_Layout.addLayout(self.Button_Layout)
        self.Main_Layout.setContentsMargins(0, 0, 0, 0)
        self.Main = QtWidgets.QWidget()
        self.Main.setLayout(self.Main_Layout)

        # NOTE 添加文件监视器功能
        self.watcher = QtCore.QFileSystemWatcher(self)
        self.watcher.directoryChanged.connect(self.handleDirectoryChanged)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.handleTimer)

        self.Exclude_Array = {".history", ".git", ".vscode"} if not isinstance(excludeArray,set) else excludeArray

        # NOTE 添加启动的路径为搜索路径
        self.handleSetDirectory(directory=os.path.dirname(__file__))

        # NOTE 添加 UI
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().addWidget(self.Main)

        self.loadJson()

    def fileItemRightClickEvent(self):
        self.menu = QtWidgets.QMenu(self)
        open_file_action = QtWidgets.QAction(u'打开文件路径', self)
        open_file_action.triggered.connect(self.openFileLocation)

        remove_action = QtWidgets.QAction(u'删除选择', self)
        remove_action.triggered.connect(self.fileRemoveItem)
        clear_action = QtWidgets.QAction(u'清空全部', self)
        clear_action.triggered.connect(self.itemClear)
        

        self.menu.addAction(open_file_action)
        self.menu.addSeparator()
        self.menu.addAction(remove_action)
        self.menu.addAction(clear_action)
        self.menu.popup(QtGui.QCursor.pos())

    def saveJson(self):
        
        data = {
            "path_list":[self.File_List.item(i).toolTip() for i in range(self.File_List.count())],
        }

        json_path = os.path.join(tempfile.gettempdir(),self.jsonName)

        with open(json_path,'w') as f:
            # json.dump(data,f,ensure_ascii=False)
            json.dump(data,f)
        
    def loadJson(self):

        json_path = os.path.join(tempfile.gettempdir(),self.jsonName)

        # if not os.path.exists(json_path):
        #     return

        try:
            with open(json_path,'r') as f:
                data = json.load(f,encoding="utf-8")
        except:
            os.remove(json_path)
            return
        
        for path in data["path_list"]:
            self.addItem(path)
    
    def itemClear(self):
        self.File_List.clear()
        self.saveJson()

    def fileRemoveItem(self):
        # NOTE 如果没有选择 直接删除当前项
        for item in self.File_List.selectedItems():
            row = self.File_List.row(item)
            item = self.File_List.takeItem(row)
            path = item.toolTip()
            if self.old_md5_data.has_key(path):
                del self.old_md5_data[path]
        self.saveJson()

    def openFileLocation(self):
        item = self.File_List.currentItem()
        path = item.toolTip()
        os.startfile(os.path.dirname(path))

    def getFile(self):
        path_list, _ = QFileDialog().getOpenFileNames(
            self, caption=u"获取Maya文件", filter="Maya Scene (*.ma *.mb);;所有文件 (*)")

        for path in path_list:
            self.addItem(path)

    def addItem(self,path):
        _, file_name = os.path.split(path)
        matches = self.File_List.findItems(file_name, QtCore.Qt.MatchExactly)
        if not matches:
            item = QtWidgets.QListWidgetItem(file_name)
            item.setToolTip(path)
            self.File_List.addItem(item)
        else:
            for match in matches:
                if path == match.toolTip():
                    break
            else:
                item = QtWidgets.QListWidgetItem(file_name)
                item.setToolTip(path)
                self.File_List.addItem(item)
        self.saveJson()

    def handleDirectoryChanged(self):
        """handleDirectoryChanged 路径下的文件发生了变化执行更新"""
        self.timer.stop()
        self._changed = True
        self.timer.start()

    def handleSetDirectory(self, directory=None):
        directory = directory if directory else QtWidgets.QFileDialog.getExistingDirectory(
            self)
        if directory:
            self.timer.stop()
            directories = self.watcher.directories()
            if directories:
                self.watcher.removePaths(directories)

            self._changed = False
            self.watcher.addPath(directory)
            self.updateList()
            self.timer.start()

    def handleTimer(self):
        if self._changed:
            self._changed = False
            self.updateList()

    def updateList(self):
        """updateList 更新列表"""
        self.new_md5_data = {}
        for directory in self.watcher.directories():
            for root, _, files in os.walk(directory):
                root = root.replace("\\", "/")
                # Note 过滤目录
                check = [x for x in root.split("/") if x in self.Exclude_Array]
                if len(check) > 0:
                    continue

                for item in IProgressDialog.loop(files,title=root,status=root):
                    file_name,ext = os.path.splitext(item)
                    if ext in self.fileFilter or "*" in self.fileFilter:
                        file_path = os.path.join(root, item).replace("\\", "/")
                        hash_value = self.get_md5(file_path)
                        self.new_md5_data[file_path] = hash_value

                        # Note 检查文件是否存在，如果不存在则添加新的路径
                        if self.old_md5_data.has_key(file_path):
                            # Note 根据md5 检查文件是否被修改
                            if self.old_md5_data[file_path] != hash_value:
                                self.old_md5_data[file_path] = hash_value
                                target_item = self.File_List.findItems(
                                    os.path.split(file_path)[1], QtCore.Qt.MatchContains)[0]
                                target_item.setText(item)
                                target_item.setToolTip(file_path)
                        else:
                            self.old_md5_data[file_path] = hash_value
                            self.addItem(file_path)
                            self.saveJson()


        # Note 检查文件是否被删除，被删除的从列表中去掉
        if len(self.new_md5_data) != len(self.old_md5_data):
            delete_list = []
            for key in self.old_md5_data:
                if key not in self.new_md5_data:
                    item = self.File_List.findItems(
                        os.path.split(key)[1], QtCore.Qt.MatchContains)
                    if item:
                        self.File_List.takeItem(self.File_List.row(item[0]))
                        delete_list.append(key)

            for key in delete_list:
                del self.old_md5_data[key]
            self.saveJson()


    def get_md5(self, file_path):
        BLOCKSIZE = 65536
        hl = hashlib.md5()
        with open(file_path, 'r') as f:
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hl.update(buf)
                buf = f.read(BLOCKSIZE)
        return hl.hexdigest()

def test():
    app = QtWidgets.QApplication([])
    watcher = IFileWatcherList(fileFilter=["*"])
    watcher.show()
    app.exec_()

if __name__ == "__main__":
    test()