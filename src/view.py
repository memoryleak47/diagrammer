#!/usr/bin/python

def gameToScreenPos(x, y):
	global focus
	ssize = getScreenSize()
	return ssize[0]/2 + x - focus[0], ssize[1]/2 + y - focus[1]

def screenToGamePos(x, y):
	global focus
	ssize = getScreenSize()
	return x - ssize[0]/2 + focus[0], y - ssize[1]/2 + focus[1]

def getScreenSize():
	global window
	return window.winfo_width(), window.winfo_height()
