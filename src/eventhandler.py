#!/usr/bin/python3

def onClick(event):
	global mouseXLeft, mouseYLeft, draggedObject, nodes, connections
	destroyRightClickMenu()
	mouseXLeft = event.x_root
	mouseYLeft = event.y_root
	draggedObject = getObjectAtMouse()

	if draggedObject != None and draggedObject.getType() == 'nodebody':
		draggedObject = None

	render()

def onRelease(event):
	global dragging, draggedObject, nodes, status
	if dragging:
		if draggedObject != None:
			draggedObject.drop()
	else:
		obj = getObjectAtMouse()
		if obj != None:
			if status['type'].startswith("choose"):
				if obj.getType() == 'node':
					if status['type'] == 'choose_add':
						if nodes.index(obj) in status['nodeids']:
							status['connection'].addSrc(obj)
					elif status['type'] == 'choose_remove':
						if nodes.index(obj) in status['nodeids']:
							status['connection'].removeSrc(obj)
					else:
						die("wot?")
				resetStatus()
			else:
				obj.click(event.x_root, event.y_root)
	draggedObject = None
	dragging = False
	render()

def onDrag(event):
	global dragging, mouseXLeft, mouseYLeft, draggedObject, saved, nodes
	if draggedObject != None:
		draggedObject.drag(event.x_root - mouseXLeft, event.y_root - mouseYLeft)
		setSaved(False)
	mouseXLeft = event.x_root
	mouseYLeft = event.y_root
	dragging = True
	updateMouse(event)
	render()

def onRightClick(event):
	global mouseXRight, mouseYRight, dragging
	mouseXRight = event.x_root
	mouseYRight = event.y_root
	render()

def onRightRelease(event):
	global dragging, window, cursorX, cursorY, rightclickmenu
	destroyRightClickMenu()
	if dragging:
		dragging = False
	else:
		obj = getObjectAtMouse()
		if obj != None:
			obj.rightClick(event.x_root, event.y_root)
		else:
			rightclickmenu = tkinter.Menu(window, tearoff=0)
			rightclickmenu.add_command(label="Create Node", command=lambda: createNode(cursorX, cursorY))
			rightclickmenu.post(event.x_root, event.y_root)
	render()

def onRightDrag(event):
	global focus, mouseXRight, mouseYRight, dragging
	focus = (focus[0] + mouseXRight - event.x_root, focus[1] + mouseYRight - event.y_root)
	mouseXRight = event.x_root
	mouseYRight = event.y_root
	dragging = True
	updateMouse(event)
	render()

def handleKeyPress(arg):
	global status, cursor

	if "text" not in status.keys():
		return

	if arg == "Tab":
		cursor = status['cursor']
		setEditText(status['text'][:cursor] + "    " + status['text'][cursor:])
		status['cursor'] += 4
	elif arg == "Right":
		incCursor()
	elif arg == "Left":
		decCursor()
	elif arg == "Ctrl+Return":
		obj = status['object']
		if obj != None:
			obj.setText(status['text'])
			if obj.getType() == 'node':
				resetStatus()
			else:
				statusOpen(obj)
			setSaved(False)
	elif arg == "Escape":
		resetStatus()
	elif arg == "RemoveLeft":
		cursor = status['cursor']
		if cursor != 0:
			setEditText(status['text'][:cursor-1] + status['text'][cursor:])
			decCursor()
	elif arg == "RemoveRight":
		cursor = status['cursor']
		if cursor < len(status['text']):
			setEditText(status['text'][:cursor] + status['text'][cursor+1:])
	elif arg == "Return":
		cursor = status['cursor']
		setEditText(status['text'][:cursor] + '\n' + status['text'][cursor:])
		incCursor()
	elif arg != '' and arg in (string.printable + "ßöäüÄÖÜ\\"):
		cursor = status['cursor']
		setEditText(status['text'][:cursor] + arg + status['text'][cursor:])
		incCursor()
	render()

def onKeyPress(event):
	if event.keysym == 'backslash':
		handleKeyPress("\\")
	else:
		handleKeyPress(repr(event.char)[1:-1])

def updateMouse(event):
	global cursorX, cursorY
	cursorX, cursorY = screenToGamePos(event.x, event.y)
