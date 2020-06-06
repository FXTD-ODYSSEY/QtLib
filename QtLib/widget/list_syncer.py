# -*- coding: utf-8 -*-
"""
列表 滚动条 和 选择 item 同步
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-01 21:00:16'

class ListSyncer(object):
    protected = False

    def protected_decorator(func):
        def wrapper(self, *args, **kwargs):
            # NOTE 避免重复调用
            if self.protected:
                return
            self.protected = True
            func(self, *args, **kwargs)
            self.protected = False
        return wrapper

    def __init__(self, *args, **kwargs):
        # NOTE args 传入 ListWidget 列表，可以是层层嵌套的数据，下面的操作会自动过滤出 ListWidget 列表
        # NOTE flattern list https://stackoverflow.com/questions/17338913/flatten-list-of-list-through-list-comprehension
        widget_list = list(chain.from_iterable(item if isinstance(item, Iterable) and
                                               not isinstance(item, basestring) else [item] for item in args))

        self.widget_list = [widget for widget in widget_list if isinstance(
            widget, QtWidgets.QListWidget)]

        # NOTE 默认同步滚动
        if kwargs.get("scroll", True):
            self.scroll_list = [widget.verticalScrollBar()
                                for widget in self.widget_list]
            for scroll in self.scroll_list:
                # NOTE 默认 scroll_sync 参数不启用 | 滚动根据滚动值进行同步 | 反之则根据滚动百分比同步
                callback = partial(self.move_scrollbar, scroll) if kwargs.get(
                    "scroll_sync", False) else lambda value: [scroll.setValue(value) for scroll in self.scroll_list]
                scroll.valueChanged.connect(callback)

        # NOTE 同步选择 默认不同步
        if kwargs.get("selection", False):
            for widget in self.widget_list:
                callback = partial(self.item_selection, widget)
                widget.itemSelectionChanged.connect(callback)

    @protected_decorator
    def move_scrollbar(self, scroll, value):
        scroll.setValue(value)
        ratio = float(value)/scroll.maximum()
        for _scroll in self.scroll_list:
            # NOTE 跳过自己
            if scroll is _scroll:
                continue
            val = int(ratio*_scroll.maximum())
            _scroll.setValue(val)

    @protected_decorator
    def item_selection(self, widget):
        items = widget.selectedItems()
        row_list = [widget.row(item) for item in items]
        for _widget in self.widget_list:
            # NOTE 跳过自己
            if widget is _widget:
                continue
            _widget.clearSelection()
            for row in row_list:
                item = _widget.item(row)
                # NOTE 如果 item 存在选择 item
                if item:
                    item.setSelected(True)


if __name__ == "__main__":
    # NOTE 同步 ListWidget
    list_1 = QtWidgets.QListWidget()
    list_2 = QtWidgets.QListWidget()
    syncer = ListSyncer(list_1, list_2, selection=True)