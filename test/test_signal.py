import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__,"..","..")))
from QtLib.signal import MouseClickSignal
from QtLib.signal import KeyBoardSignal
from QtLib.signal import HoverSignal

MouseClickSignal.test()
# HoverSignal.test()
# KeyBoardSignal.test()