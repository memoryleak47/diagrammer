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
	render()

def onRelease(event):
	global dragging, draggedObject, choosedata, nodes
	if dragging == False:
		obj = getObjectAtMouse()
		if choosedata['type'] != 'none':
			if obj['type'] == 'node':
				if choosedata['type'] == 'remove':
					if nodes.index(obj) in choosedata['connection']['from']:
						choosedata['connection']['from'].remove(nodes.index(obj))
				elif choosedata['type'] == 'add':
					if nodes.index(obj) not in choosedata['connection']['from']:
						choosedata['connection']['from'].append(nodes.index(obj))
			resetChooseData()
			render()
		else:
			if obj != None and (obj['type'] == "node" or obj['type'] == "connection"):
				if obj['status'] == 'closed':
					obj['status'] = "open"
				elif obj['status'] == 'open':
					obj['status'] = "closed"
				render()
		draggedObject = None
	dragging = False

def onDrag(event):
	global dragging, mouseXLeft, mouseYLeft, draggedObject, saved
	d = event.__dict__
	if draggedObject != None:
		draggedObject['x'] -= mouseXLeft - d['x_root']
		draggedObject['y'] -= mouseYLeft - d['y_root']
		render()
		setSaved(False)
	mouseXLeft = d['x_root']
	mouseYLeft = d['y_root']
	dragging = True


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
	render()
	mouseXRight = d['x_root']
	mouseYRight = d['y_root']
	dragging = True

def handleKeyPress(arg):
	global editdata, cursor

	if editdata['text'] == None:
		return

	if arg == "Tab":
		cursor = editdata['cursor']
		editdata['text'] = editdata['text'][:cursor] + "    " + editdata['text'][cursor:]
		editdata['cursor'] += 4
		render()
	elif arg == "Right":
		incCursor()
		render()
	elif arg == "Left":
		decCursor()
		render()
	elif arg == "Ctrl+Return":
		obj = editdata['object']
		if editdata['type'] == 'node':
			obj['head'] = editdata['text']
		elif editdata['type'] == 'nodebody':
			obj['body'] = editdata['text']
		elif editdata['type'] == 'connection':
			obj['body'] = editdata['text']
		else:
			die("onKeyPress(): Ctrl+Return: editdata['type'] is unknown")
		resetEditdata()
		setSaved(False)
		render()
	elif arg == "Escape":
		resetEditdata()
		render()
	elif arg == "RemoveLeft":
		cursor = editdata['cursor']
		if cursor != 0:
			editdata['text'] = editdata['text'][:cursor-1] + editdata['text'][cursor:]
			decCursor()
			render()
	elif arg == "RemoveRight":
		cursor = editdata['cursor']
		if cursor < len(editdata['text']):
			editdata['text'] = editdata['text'][:cursor] + editdata['text'][cursor+1:]
			render()
	elif arg == "Return":
		cursor = editdata['cursor']
		editdata['text'] = editdata['text'][:cursor] + '\n' + editdata['text'][cursor:]
		incCursor()
		render()
	elif arg != '' and arg in (string.printable + "ßöäüÄÖÜ\\"):
		cursor = editdata['cursor']
		editdata['text'] = editdata['text'][:cursor] + arg + editdata['text'][cursor:]
		incCursor()
		render()

def onKeyPress(event):
	if event.keysym == 'backslash':
		handleKeyPress("\\")
	else:
		handleKeyPress(repr(event.char)[1:-1])

def updateMouse(event):
	global cursorX, cursorY
	cursorX, cursorY = screenToGamePos((event.x, event.y))
