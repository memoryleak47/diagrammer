#!/usr/bin/python

def gameToScreenPos(position):
	global focus
	return 400 + position[0] - focus[0], 300 + position[1] - focus[1]

def screenToGamePos(position):
	global focus
	return position[0] - 400 + focus[0], position[1] - 300 + focus[1]
