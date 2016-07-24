#!/usr/bin/python3

def openRightClickMenu(position):
	global window, rightclickmenu
	obj = getObjectAtMouse()
	rightclickmenu = tkinter.Menu(window, tearoff=0)
	if obj == None:
		rightclickmenu.add_command(label="Create Node", command=lambda: createNode(cursorX, cursorY))
	elif obj["type"] == "node":
		rightclickmenu.add_command(label="Delete Node", command=lambda: deleteNode(obj))
		rightclickmenu.add_command(label="Edit", command=lambda: editNode(obj))
		rightclickmenu.add_command(label="Add Connection", command=lambda: createConnection(obj))
	elif obj["type"] == "connection":
		rightclickmenu.add_command(label="Delete Connection", command=lambda: deleteConnection(obj))
		rightclickmenu.add_command(label="Add Source", command=lambda: chooseAddSource(obj))
		rightclickmenu.add_command(label="Remove Source", command=lambda: chooseRemoveSource(obj))
		rightclickmenu.add_command(label="Edit", command=lambda: editConnection(obj))
	elif obj['type'] == 'nodebody':
		rightclickmenu.add_command(label="Edit", command=lambda: editNodeBody(obj['node']))
	else:
		die("wot?")
	rightclickmenu.post(position[0], position[1])

def destroyRightClickMenu():
	global rightclickmenu
	if rightclickmenu != None:
		rightclickmenu.destroy()
		rightclickmenu = None

