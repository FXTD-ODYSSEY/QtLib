# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-13 15:01:18'
__version__ = '1.0.0'

"""
QtLib for python
"""
import os
import sys
DIR = os.path.dirname(__file__)

try:
    import Qt
except ImportError:
    sys.path.append(os.path.join(DIR,"_vendor"))
    import Qt