#!/usr/bin/python3

def menu_new():
	if reallyDiscardContent():
		restart()

def menu_openFile():
	global window
	if reallyDiscardContent():
		restart(askopenfilename())

def menu_saveFile():
	global openfilename, nodes, connections
	if openfilename == None:
		openfilename = asksaveasfilename()
	saveFile(openfilename, nodes, connections)
	setSaved(True)

def menu_saveFileAs():
	global nodes, connections, openfilename
	openfilename = asksaveasfilename()
	saveFile(openfilename, nodes, connections)
	setSaved(True)

def menu_close():
	if reallyDiscardContent():
		sys.exit()
