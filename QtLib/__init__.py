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
vendor_path = os.path.join(DIR,"_vendor")
sys.path.extend([os.path.join(vendor_path,folder) for folder in os.listdir(vendor_path)])

import Qt
import dayu_widgets
import singledispatch
