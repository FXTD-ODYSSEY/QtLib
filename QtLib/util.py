# coding:utf-8
from __future__ import print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 20:09:01'

"""
util library
"""

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

import time
from functools import partial, wraps
from contextlib import contextmanager

# NOTE replaceWidget ----------------------------------------------------------------------------

def replaceWidget(src,dst):
    """replaceWidget 
    replace widget, typeically use for the QtDesigner widget replace to the Custorm widget

    :param src: source widget
    :type src: QWidget
    :param dst: target widget
    :type dst: QWidget
    :return: target widget
    :rtype: QWidget
    """    
    
    updateWidgetState(src,dst)
    layout = src.parent().layout()
    layout,index = getTargetLayoutIndex(layout,src)
    if not layout:
        print ("Could not find %s Layout" % src)
        return src

    layout.insertWidget(index,dst)
    src.setParent(None)
    
    return dst

def updateWidgetState(src,dst):
    """updateWidgetState 
    sync widget attribute

    :param src: source widget
    :type src: QWidget
    :param dst: target widget
    :type dst: QWidget
    """    

    if src.acceptDrops()           : dst.setAcceptDrops(src.acceptDrops())
    if src.accessibleDescription() : dst.setAccessibleDescription(src.accessibleDescription())
    if src.backgroundRole()        : dst.setBackgroundRole(src.backgroundRole())
    if src.baseSize()              : dst.setBaseSize(src.baseSize())
    if src.contentsMargins()       : dst.setContentsMargins(src.contentsMargins())
    if src.contextMenuPolicy()     : dst.setContextMenuPolicy(src.contextMenuPolicy())
    if src.cursor()                : dst.setCursor(src.cursor())
    if src.focusPolicy()           : dst.setFocusPolicy(src.focusPolicy())
    if src.focusProxy()            : dst.setFocusProxy(src.focusProxy())
    if src.font()                  : dst.setFont(src.font())
    if src.foregroundRole()        : dst.setForegroundRole(src.foregroundRole())
    if src.geometry()              : dst.setGeometry(src.geometry())
    if src.inputMethodHints()      : dst.setInputMethodHints(src.inputMethodHints())
    if src.layout()                : dst.setLayout(src.layout())
    if src.layoutDirection()       : dst.setLayoutDirection(src.layoutDirection())
    if src.locale()                : dst.setLocale(src.locale())
    if src.mask()                  : dst.setMask(src.mask())
    if src.maximumSize()           : dst.setMaximumSize(src.maximumSize())
    if src.minimumSize()           : dst.setMinimumSize(src.minimumSize())
    if src.hasMouseTracking ()     : dst.setMouseTracking(src.hasMouseTracking ())
    if src.palette()               : dst.setPalette(src.palette())
    if src.parent()                : dst.setParent(src.parent())
    if src.sizeIncrement()         : dst.setSizeIncrement(src.sizeIncrement())
    if src.sizePolicy()            : dst.setSizePolicy(src.sizePolicy())
    if src.statusTip()             : dst.setStatusTip(src.statusTip())
    if src.style()                 : dst.setStyle(src.style())
    if src.toolTip()               : dst.setToolTip(src.toolTip())
    if src.updatesEnabled()        : dst.setUpdatesEnabled(src.updatesEnabled())
    if src.whatsThis()             : dst.setWhatsThis(src.whatsThis())
    if src.windowFilePath()        : dst.setWindowFilePath(src.windowFilePath())
    if src.windowFlags()           : dst.setWindowFlags(src.windowFlags())
    if src.windowIcon()            : dst.setWindowIcon(src.windowIcon())
    if src.windowIconText()        : dst.setWindowIconText(src.windowIconText())
    if src.windowModality()        : dst.setWindowModality(src.windowModality())
    if src.windowOpacity()         : dst.setWindowOpacity(src.windowOpacity())
    if src.windowRole()            : dst.setWindowRole(src.windowRole())
    if src.windowState()           : dst.setWindowState(src.windowState())


def getTargetLayoutIndex(layout,target):
    """getTargetLayoutIndex 
    get the layout and index, interally use with replaceWidget function

    :param layout: input QLayout
    :type layout: QLayout
    :param target: input QWidget
    :type target: QWidget
    :return: layout , index
    :rtype: [QLayout,int]
    """        
    
    count = layout.count()
    for i in range(count):
        item = layout.itemAt(i).widget()
        if item == target:
            return layout,i
    else:
        for child in layout.children():
            layout,i = getTargetLayoutIndex(child,target)
            if layout:
                return layout,i
        return [None,None]

# NOTE traverseChildren ----------------------------------------------------------------------------

def traverseChildren(parent,childCallback=None,printCallback=None,indent=4,prefix="",log=False):
    """traverseChildren 
    Traverse into the widget children | print the children hierarchy
    
    :param parent: traverse widget
    :type parent: QWidget
    :param indent: indentation space, defaults to ""
    :type indent: str, optional
    :param log: print the data, defaults to False
    :type log: bool, optional
    """

    if callable(printCallback):
        printCallback(prefix,parent)
    elif log:
        print (prefix,parent)
        
    if not hasattr(parent,"children"):
        return

    prefix = "".join([" " for _ in range(indent)]) + prefix
    for child in parent.children():
        traverse_func = lambda:traverseChildren(child,indent=indent,prefix=prefix,childCallback=childCallback,printCallback=printCallback,log=log)
        if callable(childCallback) : 
            childCallback(child,traverse_func)
        else:
            traverse_func()

# NOTE logTime ----------------------------------------------------------------------------

def logTime(func=None, msg="elapsed time:"):
    """logTime 
    log function running time

    :param func: function get from decorators, defaults to None
    :type func: function, optional
    :param msg: default print message, defaults to "elapsed time:"
    :type msg: str, optional
    :return: decorator function return
    :rtype: dynamic type
    """            
    if not func:
        return partial(logTime,msg=msg)
    @wraps(func)
    def wrapper(*args, **kwargs):
        curr = time.time()
        res = func(*args, **kwargs)
        print(msg,time.time() - curr)
        return res
    return wrapper