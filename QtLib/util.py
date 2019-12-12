# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 20:09:01'

"""
调用库
"""

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

def replaceWidget(src,dst):
    u"""replaceWidget 替换组件
    
    Parameters
    ----------
    src : QWidget
        源组件
    dst : QWidget
        目标组件
    
    Returns
    -------
    QWidget
        [description]
    """
    updateWidgetState(src,dst)
    layout = src.parent().layout()
    layout,index = getTargetLayoutIndex(layout,src)
    if not layout:
        print u"没有找到 %s 的 Layout，替换失败" % src
        return src

    layout.insertWidget(index,dst)
    src.setParent(None)
    
    return dst

def updateWidgetState(src,dst):
    u"""updateWidgetState 同步组件状态
    
    Parameters
    ----------
    src : QWidget
        源组件
    dst : QWidget
        目标组件
    """
    dst.setAcceptDrops(src.acceptDrops())
    dst.setAccessibleDescription(src.accessibleDescription())
    dst.setBackgroundRole(src.backgroundRole())
    dst.setBaseSize(src.baseSize())
    dst.setContentsMargins(src.contentsMargins())
    dst.setContextMenuPolicy(src.contextMenuPolicy())
    dst.setCursor(src.cursor())
    dst.setFocusPolicy(src.focusPolicy())
    dst.setFocusProxy(src.focusProxy())
    dst.setFont(src.font())
    dst.setForegroundRole(src.foregroundRole())
    dst.setGeometry(src.geometry())
    dst.setInputMethodHints(src.inputMethodHints())
    dst.setLayout(src.layout())
    dst.setLayoutDirection(src.layoutDirection())
    dst.setLocale(src.locale())
    dst.setMask(src.mask())
    dst.setMaximumSize(src.maximumSize())
    dst.setMinimumSize(src.minimumSize())
    dst.setMouseTracking(src.hasMouseTracking ())
    dst.setPalette(src.palette())
    dst.setParent(src.parent())
    dst.setSizeIncrement(src.sizeIncrement())
    dst.setSizePolicy(src.sizePolicy())
    dst.setStatusTip(src.statusTip())
    dst.setStyle(src.style())
    dst.setToolTip(src.toolTip())
    dst.setUpdatesEnabled(src.updatesEnabled())
    dst.setWhatsThis(src.whatsThis())
    dst.setWindowFilePath(src.windowFilePath())
    dst.setWindowFlags(src.windowFlags())
    dst.setWindowIcon(src.windowIcon())
    dst.setWindowIconText(src.windowIconText())
    dst.setWindowModality(src.windowModality())
    dst.setWindowOpacity(src.windowOpacity())
    dst.setWindowRole(src.windowRole())
    dst.setWindowState(src.windowState())


def getTargetLayoutIndex(layout,target):
    u"""getTargetLayoutIndex 获取目标 Layout 和 序号
    
    Parameters
    ----------
    layout : QLayout 
        通过 QLayout 递归遍历下属的组件
    target : QWidget
        要查询的组件
    
    Returns
    -------
    layout : QLayout
        查询组件所在的 Layout
    i : int
        查询组件所在的 Layout 的序号
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