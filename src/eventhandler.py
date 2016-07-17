#!/usr/bin/python3

def onClick(event):
	global mouseXLeft, mouseYLeft, draggedObject
	destroyPopup()
	d = event.__dict__
	mouseXLeft = d['x_root']
	mouseYLeft = d['y_root']
	draggedObject = getObjectAtMouse()
	if draggedObject != None and draggedObject['type'] == 'nodebody':
		draggedObject = None

def onRelease(event):
	global dragging, draggedObject
	if dragging == False:
		obj = getObjectAtMouse()
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
			#popupmenu.add_command(label="Connect To", command=lambda: createConnection(obj))
		elif obj["type"] == "connection":
			popupmenu.add_command(label="Delete Connection", command=lambda: deleteConnection(obj))
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

def onKeyPress(event):
	global editdata
	char = repr(event.char)[1:-1] # 'wow' -> wow

	if editdata['text'] != None:
		if event.keysym == "Tab":
			editdata['text'] += "\t"
			render()
		elif event.keysym == "Right":
			incCursor()
			render()
		elif event.keysym == "Left":
			editdata['cursor'] = max(0, editdata['cursor']-1)
			render()
		elif char == "\\r" and event.state == 20: # Ctrl + Enter
			obj = editdata['object']
			if editdata['type'] == 'node':
				obj['head'] = editdata['text']
			elif editdata['type'] == 'nodebody':
				obj['body'] = editdata['text']
			elif editdata['type'] == 'connection':
				die("TODO $12")
			else:
				die("onKeyPress(): Ctrl+Enter: editdata['type'] is unknown")
			resetEditdata()
			setSaved(False)
			render()
		elif char == "\\x1b":
			resetEditdata()
			render()
		elif char == "\\x08": # backspace
			cursor = editdata['cursor']
			if cursor != 0:
				editdata['text'] = editdata['text'][:cursor-1] + editdata['text'][cursor:]
				decCursor()
				render()
		elif char == "\\x7f": # remove right
			cursor = editdata['cursor']
			if cursor < len(editdata['text']):
				editdata['text'] = editdata['text'][:cursor] + editdata['text'][cursor+1:]
				render()
		elif char != '' and char in (string.printable + "ßöäüÄÖÜ"):
			cursor = editdata['cursor']
			editdata['text'] = editdata['text'][:cursor] + char + editdata['text'][cursor:]
			incCursor()
			render()
		elif char == "\\r":
			cursor = editdata['cursor']
			editdata['text'] = editdata['text'][:cursor] + '\n' + editdata['text'][cursor:]
			incCursor()
			render()
		elif event.keysym == "backslash":
			cursor = editdata['cursor']
			editdata['text'] = editdata['text'][:cursor] + "\\" + editdata['text'][cursor:]
			incCursor()
			render()

def updateMouse(event):
	global cursorX, cursorY, focus
	cursorX = event.x - 400 + focus[0]
	cursorY = event.y - 300 + focus[1]
