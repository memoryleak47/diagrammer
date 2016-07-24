#!/usr/bin/python3

def destroyRightClickMenu():
	global rightclickmenu
	if rightclickmenu != None:
		rightclickmenu.destroy()
		rightclickmenu = None

