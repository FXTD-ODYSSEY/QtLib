# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 15:26:12'

"""
https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input
"""
import sys
from ..Qt import QtGui
from ..Qt import QtCore
from ..Qt import QtWidgets


class ExtendedCombo( QtWidgets.QComboBox ):
    def __init__( self,  parent = None):
        super( ExtendedCombo, self ).__init__( parent )

        self.setFocusPolicy( QtCore.Qt.StrongFocus )
        self.setEditable( True )
        self.completer = QtWidgets.QCompleter( self )

        # always show all completions
        self.completer.setCompletionMode( QtWidgets.QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = QtCore.QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( QtCore.Qt.CaseInsensitive )

        self.completer.setPopup( self.view() )

        self.setCompleter( self.completer )

        edit = self.lineEdit()
        # NOTE 取消按 Enter 生成新 item 的功能
        edit.returnPressed.disconnect()
        # edit.returnPressed.connect(self.enter)
        edit.textEdited[unicode].connect( self.pFilterModel.setFilterFixedString )
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    # def enter(self):
    #     print "enter"
    #     # text = self.lineEdit().text()
    #     # index = self.findText(text)
    #     # self.setCurrentIndex(index)
    #     # print text,index

    def setModel( self, model ):
        super(ExtendedCombo, self).setModel( model )
        self.pFilterModel.setSourceModel( model )
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        super(ExtendedCombo, self).setModelColumn( column )


    def view( self ):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
      if text:
        index = self.findText(text)
        self.setCurrentIndex(index)
        print index

def main():
    app = QtWidgets.QApplication(sys.argv)

    model = QtGui.QStandardItemModel()

    for i,word in enumerate( ['hola', 'adios', 'hello', 'good bye'] ):
        item = QtGui.QStandardItem(word)
        model.setItem(i, 0, item)

    combo = ExtendedCombo()
    combo.setModel(model)
    combo.setModelColumn(0)

    combo.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()