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


class ICompleterComboBox( QtWidgets.QComboBox ):
    def __init__( self,  parent = None):
        super( ICompleterComboBox, self ).__init__( parent )

        self.setFocusPolicy( QtCore.Qt.StrongFocus )
        self.setEditable( True )
        self.completer = QtWidgets.QCompleter( self )

        # always show all completions
        self.completer.setCompletionMode( QtWidgets.QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = QtCore.QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( QtCore.Qt.CaseInsensitive )
        self.pFilterModel.setSourceModel( QtGui.QStandardItemModel() )

        self.completer.setPopup( self.view() )

        self.setCompleter( self.completer )

        edit = self.lineEdit()
        # NOTE 取消按 Enter 生成新 item 的功能
        edit.returnPressed.disconnect()
        edit.textEdited[unicode].connect( self.pFilterModel.setFilterFixedString )
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def clear(self):
        self.pFilterModel.setSourceModel( QtGui.QStandardItemModel() )
        super(ICompleterComboBox,self).clear()

    def addItems(self,texts):
        super(ICompleterComboBox,self).addItems(texts)
        for text in texts:
            self.addItem(text)

    def addItem(self,*args):
        super(ICompleterComboBox,self).addItem(*args)
        if len(args) == 2:
            _,text = args
        else:
            text = args[0]
        
        model = self.pFilterModel.sourceModel()
        
        item = QtGui.QStandardItem(text)
        model.setItem(model.rowCount(), item)

        if self.completer.model() != self.pFilterModel:
            self.completer.setModel(self.pFilterModel)


    def setModel( self, model ):
        super(ICompleterComboBox, self).setModel( model )
        self.pFilterModel.setSourceModel( model )
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        super(ICompleterComboBox, self).setModelColumn( column )


    def view( self ):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
      if text:
        index = self.findText(text)
        self.setCurrentIndex(index)

def test():

    app = QtWidgets.QApplication([])

    model = QtGui.QStandardItemModel()

    for i,word in enumerate( ['hola', 'adios', 'hello', 'good bye'] ):
        item = QtGui.QStandardItem(word)
        model.setItem(i, item)

    combo = ICompleterComboBox()
    combo.setModel(model)
    combo.setModelColumn(0)

    combo.show()

    app.exec_()

if __name__ == "__main__":
    test()