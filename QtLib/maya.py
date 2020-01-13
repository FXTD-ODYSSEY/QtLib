# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-13 10:52:09'

"""
Get Maya Window
"""

from maya import cmds 
from maya import mel 
from maya import OpenMayaUI

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from Qt.QtCompat import wrapInstance

# NOTE Qt <-> Maya ----------------------------------------------------------------------------

def mayaToQT(name):
    """
    Maya -> QWidget

    :param str name: Maya name of an ui object
    :return: QWidget of parsed Maya name
    :rtype: QWidget
    """
    ptr = OpenMayaUI.MQtUtil.findControl( name )
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findLayout( name )    
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
    if ptr is not None:     
        return wrapInstance( long( ptr ), QtWidgets.QWidget )

def qtToMaya(widget):
    """
    QWidget -> Maya name

    :param QWidget widget: QWidget of a maya ui object
    :return: Maya name of parsed QWidget
    :rtype: str
    """
    return OpenMayaUI.MQtUtil.fullName(
        long(
            shiboken.getCppPointer(widget)[0]
        ) 
    )
    
# NOTE get Maya UI ----------------------------------------------------------------------------

def mayaWindow():
    """
    Get Maya's main window.
    
    :rtype: QMainWindow
    """
    window = OpenMayaUI.MQtUtil.mainWindow()
    window = wrapInstance(long(window), QtWidgets.QMainWindow)
    return window

def mayaMenu():
    """
    Get Maya's main menu bar.
    
    :rtype: QMenuBar
    """
    for m in mayaWindow().children():
        if type(m) == QMenuBar:
            return m

def getStatusLine():
    """
    Get the QWidget of Maya's status line. 
    
    :return: QWidget of Maya's status line
    :rtype: QWidget
    """
    gStatusLine = mel.eval("$tmpVar=$gStatusLine")
    return mayaToQT(gStatusLine)
    
# NOTE create Maya UI ----------------------------------------------------------------------------

def createUIComponentToolBar(ControlName="CustomToolBar"):
    """createUIComponentToolBar 
    create a Maya Component Tool Bar Widget
    
    :param ControlName: str, defaults to "CustomToolBar"
    :type ControlName: str, optional
    """        
    
    if cmds.workspaceControl(ControlName,ex=1):
        cmds.deleteUI(ControlName)

    help_line = mayaToQT("HelpLine")
    help_line.setObjectName("_HelpLine")

    mel.eval("""
    createUIComponentToolBar(
            "HelpLine", localizedUIComponentLabel("%s"), "", $gWorkAreaForm, "top", false);
    """ % ControlName)

    UIComponentToolBar = mayaToQT("HelpLine")
    UIComponentToolBar.setObjectName(ControlName)
    help_line.setObjectName("HelpLine")
    
    layout = UIComponentToolBar.layout()
    # NOTE add spacing
    layout.setContentsMargins(10,0,0,0)

    return UIComponentToolBar

