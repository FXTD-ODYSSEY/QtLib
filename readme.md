# 前言

> &emsp;&emsp;开发一个 Qt 组件库是我一直以来的目标    
> &emsp;&emsp;去年的时候，基于 ui 文件的启发，我开发了一个简单的代码生成器，抓取 ui 文件的数据自动生成 py 文件代码    
> &emsp;&emsp;但是这种方式修改ui的时候很多 py 代码需要重新调整，使用起来非常不友好    
> &emsp;&emsp;后来我打算朝着节点话编程的方向去进行扩展，打算将代码生成器改写为节点式生成的效果。    

> &emsp;&emsp;后来讲过前辈的指点，开发一个 Python 库 才是一个最终的解决方案。    
> &emsp;&emsp;然而后续的因为各种忙，这个开发方案就一拖再拖了。。。。。。    

## todolist

- [ ] 第三方库调式
    - [x] 添加 Qt 库 - 兼容不同 python 的 Qt 库
    - [x] 添加 voluptuous 库 - 用于参数校验
    - [x] 添加 pyqtConfig 库 - 记录组件状态
        - [x] 添加 decorator 来快速遍历组件(组件用 objectName 记录)
    - [ ] 添加 dayu_widget 库 - AntDesign 前端组件库
- [ ] Singal扩展
    - [x] 添加 鼠标点击signal - 扩展组件的 单击 、 双击 信号槽
    - [x] 添加 键盘触发signal - 扩展组件的 快捷键 信号槽
    - [x] 添加 悬浮signal     - 扩展组件的 悬浮 信号槽
    - [ ] 添加 拖拽signal     - 扩展组件的 拖拽 信号槽