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
CONNECTIONCOLOR = "blue"

STDFONT = ("times", 10)
CODEFONT = ("Monospace", 10)
EDITFONT = ("Monospace", 7)

def die(msg):
	print(msg)
	sys.exit()
