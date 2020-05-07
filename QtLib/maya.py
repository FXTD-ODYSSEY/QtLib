# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-13 10:52:09'

"""
Get Maya Window
"""
import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,'_vendor','Qt')
sys.path.insert(0,MODULE) if MODULE not in sys.path else None


from maya import cmds 
from maya import mel 
from maya import OpenMayaUI

from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import wrapInstance,getCppPointer

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
            getCppPointer(widget)[0]
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
        if type(m) == QtWidgets.QMenuBar:
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

    # NOTE 利用大小写不同生成 Maya 内置的 UIComponentToolBar 组件
    UIComponentToolBar = cmds.workspaceControl("HELPLINE")
    UIComponentToolBar.setObjectName(ControlName)
    
    layout = UIComponentToolBar.layout()
    # NOTE add spacing
    layout.setContentsMargins(10,0,0,0)

    return UIComponentToolBar

