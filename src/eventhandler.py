#!/usr/bin/python3

def foldExcept(obj):
	global nodes, connections

	for thingy in nodes + connections:
		if obj != thingy:
			thingy['status'] = 'closed'
	if editdata['object'] != obj:
		resetEditdata()

def onClick(event):
	global mouseXLeft, mouseYLeft, draggedObject, nodes, connections, editdata
	destroyRightClickMenu()
	mouseXLeft = event.x_root
	mouseYLeft = event.y_root
	draggedObject = getObjectAtMouse()

	if draggedObject != None and draggedObject['type'] == 'nodebody':
		draggedObject = None

	foldExcept(draggedObject)

def onRelease(event):
	global dragging, draggedObject, choosedata, nodes
	if dragging == False:
		obj = getObjectAtMouse()
		if choosedata['type'] != 'none':
			if obj != None and obj['type'] == 'node':
				if choosedata['type'] == 'remove':
					if nodes.index(obj) in choosedata['connection']['from'] and nodes.index(obj) != choosedata['connection']['to']:
						choosedata['connection']['from'].remove(nodes.index(obj))
				elif choosedata['type'] == 'add':
					if nodes.index(obj) not in choosedata['connection']['from'] and nodes.index(obj) != choosedata['connection']['to']:
						choosedata['connection']['from'].append(nodes.index(obj))
			resetChooseData()
		else:
			if obj != None and (obj['type'] == "node" or obj['type'] == "connection"):
				if obj['status'] == 'closed':
					obj['status'] = "open"
				elif obj['status'] == 'open':
					obj['status'] = "closed"

				if obj['type'] == 'connection':
					repositionConnection(obj)
		draggedObject = None
	else:
		if draggedObject != None:
			onDrop(draggedObject)
	dragging = False

def onDrop(thingy):
	global connections, nodes
	if thingy['type'] == 'connection':
			repositionConnection(thingy)

def onDrag(event):
	global dragging, mouseXLeft, mouseYLeft, draggedObject, saved, nodes
	if draggedObject != None:
		move(draggedObject, (event.x_root - mouseXLeft, event.y_root - mouseYLeft))
		setSaved(False)
	mouseXLeft = event.x_root
	mouseYLeft = event.y_root
	dragging = True
	updateMouse(event)

def onRightClick(event):
	global mouseXRight, mouseYRight
	mouseXRight = event.x_root
	mouseYRight = event.y_root

def onRightRelease(event):
	global dragging, window, cursorX, cursorY
	destroyRightClickMenu()
	if dragging == False:
		openRightClickMenu((event.x_root, event.y_root))
	dragging = False

def onRightDrag(event):
	global focus, mouseXRight, mouseYRight, dragging
	focus = (focus[0] + mouseXRight - d['x_root'], focus[1] + mouseYRight - d['y_root'])
	mouseXRight = event.x_root
	mouseYRight = event.y_root
	dragging = True
	updateMouse(event)

def handleKeyPress(arg):
	global editdata, cursor

	if editdata['text'] == None:
		return

	if arg == "Tab":
		cursor = editdata['cursor']
		setEditText(editdata['text'][:cursor] + "    " + editdata['text'][cursor:])
		editdata['cursor'] += 4
	elif arg == "Right":
		incCursor()
	elif arg == "Left":
		decCursor()
	elif arg == "Ctrl+Return":
		obj = editdata['object']
		if obj != None:
			if obj['type'] == 'node':
				obj['head'] = editdata['text']
				resetEditdata()
				repositionConnections(obj)
			elif obj['type'] == 'nodebody':
				obj['node']['body'] = editdata['text']
				resetEditdata()
			elif obj['type'] == 'connection':
				obj['body'] = editdata['text']
				resetEditdata()
			else:
				die("onKeyPress(): Ctrl+Return: editdata['object']['type'] is unknown")
			setSaved(False)
	elif arg == "Escape":
		resetEditdata()
	elif arg == "RemoveLeft":
		cursor = editdata['cursor']
		if cursor != 0:
			setEditText(editdata['text'][:cursor-1] + editdata['text'][cursor:])
			decCursor()
	elif arg == "RemoveRight":
		cursor = editdata['cursor']
		if cursor < len(editdata['text']):
			setEditText(editdata['text'][:cursor] + editdata['text'][cursor+1:])
	elif arg == "Return":
		cursor = editdata['cursor']
		setEditText(editdata['text'][:cursor] + '\n' + editdata['text'][cursor:])
		incCursor()
	elif arg != '' and arg in (string.printable + "ßöäüÄÖÜ\\"):
		cursor = editdata['cursor']
		setEditText(editdata['text'][:cursor] + arg + editdata['text'][cursor:])
		incCursor()

def onKeyPress(event):
	if event.keysym == 'backslash':
		handleKeyPress("\\")
	else:
		handleKeyPress(repr(event.char)[1:-1])

def updateMouse(event):
	global cursorX, cursorY
	cursorX, cursorY = screenToGamePos((event.x, event.y))
