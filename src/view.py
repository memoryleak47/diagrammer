#!/usr/bin/python

def gameToScreenPos(x, y):
	global focus
	return 400 + x - focus[0], 300 + y - focus[1]

def screenToGamePos(x, y):
	global focus
	return x - 400 + focus[0], y - 300 + focus[1]
