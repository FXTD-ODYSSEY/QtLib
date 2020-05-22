# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-07 09:23:32'
__version__ = '1.0.1'

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
