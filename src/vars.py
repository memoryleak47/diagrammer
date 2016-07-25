#!/usr/bin/python3

usage="Usage:\tdiagrammer [<file>]"

import sys
import tkinter
import tkinter.font as tkfont
import string
from tkinter.filedialog import *

PADDING = 6
CONNECTIONSIZE = 12

BACKGROUNDCOLOR = "#AAAAAA"
CHOOSEHEADCOLOR = "#FF7755"
HEADCOLOR = "#FF0000"
BODYCOLOR = "#AA5555"
EDITCOLOR = "white"
EMPTYCONNECTIONCOLOR = "#4444AA"
CONNECTIONCOLOR = "blue"

STDFONT = ("times", 10)
CODEFONT = ("Monospace", 10)
EDITFONT = ("Monospace", 7)

def die(msg):
	print(msg)
	sys.exit()
