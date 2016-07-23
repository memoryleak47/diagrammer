#!/usr/bin/python3

def onClick(event):
	global mouseXLeft, mouseYLeft, draggedObject, nodes, connections, editdata
	destroyPopup()
	d = event.__dict__
	mouseXLeft = d['x_root']
	mouseYLeft = d['y_root']
	draggedObject = getObjectAtMouse()

	if draggedObject != None and draggedObject['type'] == 'nodebody':
		draggedObject = None

	# close everything, which is not focused
	for thingy in nodes + connections:
		if draggedObject != thingy:
			thingy['status'] = 'closed'
	if editdata['object'] != draggedObject:
		resetEditdata()

def onRelease(event):
	global dragging, draggedObject, choosedata, nodes
	if dragging == False:
		obj = getObjectAtMouse()
		if choosedata['type'] != 'none':
			if obj != None and obj['type'] == 'node':
				if choosedata['type'] == 'remove':
					if nodes.index(obj) in choosedata['connection']['from']:
						choosedata['connection']['from'].remove(nodes.index(obj))
				elif choosedata['type'] == 'add':
					if nodes.index(obj) not in choosedata['connection']['from']:
						choosedata['connection']['from'].append(nodes.index(obj))
			resetChooseData()
		else:
			if obj != None and (obj['type'] == "node" or obj['type'] == "connection"):
				if obj['status'] == 'closed':
					obj['status'] = "open"
				elif obj['status'] == 'open':
					obj['status'] = "closed"
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
	d = event.__dict__
	if draggedObject != None:
		move(draggedObject, (d['x_root'] - mouseXLeft, d['y_root'] - mouseYLeft))
		setSaved(False)
	mouseXLeft = d['x_root']
	mouseYLeft = d['y_root']
	dragging = True
	updateMouse(event)

def onRightClick(event):
	global mouseXRight, mouseYRight
	d = event.__dict__
	mouseXRight = d['x_root']
	mouseYRight = d['y_root']

def onRightRelease(event):
	global dragging, window, cursorX, cursorY, popupmenu
	destroyPopup()
	if dragging == False:
		obj = getObjectAtMouse()
		popupmenu = tkinter.Menu(window, tearoff=0)
		if obj == None:
			popupmenu.add_command(label="Create Node", command=lambda: createNode(cursorX, cursorY))
		elif obj["type"] == "node":
			popupmenu.add_command(label="Delete Node", command=lambda: deleteNode(obj))
			popupmenu.add_command(label="Edit", command=lambda: editNode(obj))
			popupmenu.add_command(label="Add Connection", command=lambda: createConnection(obj))
		elif obj["type"] == "connection":
			popupmenu.add_command(label="Delete Connection", command=lambda: deleteConnection(obj))
			popupmenu.add_command(label="Add Source", command=lambda: chooseAddSource(obj))
			popupmenu.add_command(label="Remove Source", command=lambda: chooseRemoveSource(obj))
			popupmenu.add_command(label="Edit", command=lambda: editConnection(obj))
		elif obj['type'] == 'nodebody':
			popupmenu.add_command(label="Edit", command=lambda: editNodeBody(obj['node']))
		else:
			die("wot?")
		popupmenu.post(event.x_root, event.y_root)
	dragging = False

def onRightDrag(event):
	global focus, mouseXRight, mouseYRight, dragging
	d = event.__dict__
	focus = (focus[0] + mouseXRight - d['x_root'], focus[1] + mouseYRight - d['y_root'])
	mouseXRight = d['x_root']
	mouseYRight = d['y_root']
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
		if editdata['type'] == 'node':
			obj['head'] = editdata['text']
			resetEditdata()
			repositionConnections(obj)
		elif editdata['type'] == 'nodebody':
			obj['body'] = editdata['text']
			resetEditdata()
		elif editdata['type'] == 'connection':
			obj['body'] = editdata['text']
			resetEditdata()
		else:
			die("onKeyPress(): Ctrl+Return: editdata['type'] is unknown")
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
