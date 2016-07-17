#!/usr/bin/python3

usage="Usage:\tdiagrammer [<file>]"

import sys
import tkinter
import tkinter.font as tkfont
import string
from tkinter.filedialog import *

PADDING = 6

BACKGROUNDCOLOR = "#AAAAAA"
HEADCOLOR = "red"
BODYCOLOR = "#AA5555"
EDITCOLOR = "white"

STDFONT = ("times", 12)
CODEFONT = ("Monospace", 12)
EDITFONT = ("Monospace", 10)

def die(msg):
	print(msg)
	sys.exit()
