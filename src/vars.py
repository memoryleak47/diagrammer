#!/usr/bin/python3

usage="Usage:\tdiagrammer [<file>]"

import sys
import tkinter
import tkinter.font as tkfont
import string
from tkinter.filedialog import *

PADDING = 6
HEADCOLOR = "red"
BODYCOLOR = "grey"
EDITCOLOR = "blue"

STDFONT = ("times", 12)
CODEFONT = ("Monospace", 12)

def die(msg):
	print(msg)
	sys.exit()
