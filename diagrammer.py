#!/usr/bin/python3

usage="Usage:\tdiagrammer <file>"

import sys
import tkinter
import string
from tkinter.filedialog import *

PADDING = 6
HEADCOLOR = "red"
BODYCOLOR = "grey"
EDITCOLOR = "blue"

def die(msg):
	print(msg)
	sys.exit()

def loadFile(filename):
	global nodes, connections
	nodes = list()
	connections = list()

	f = open(filename)
	lines = f.readlines()
	f.close()

	for line in lines:
		tokens = list()
		line = line.strip()

		if line.startswith("node "):
			tokens.append("node")
			i = 5
		elif line.startswith("connection "):
			tokens.append("connection")
			i = 11
		else:
			die("Can not tokenize: " + line)
		while i < len(line):
			if line[i] == "'":
				tmp = ""
				i += 1
				while i < len(line):
					if line[i] == "\\":
						tmp += line[i+1]
						i += 2
					elif line[i] == "'":
						break
					else:
						tmp += line[i]
						i += 1
				tokens.append(tmp)
				i += 1
			elif line[i] == " ":
				i += 1

		if tokens[0] == "node":
			nodes.append({'status': 'closed', 'type': 'node', "head": tokens[1], "x": int(tokens[2]), "y": int(tokens[3]), "body": tokens[4]})
		elif line.startswith("connection"):
			connections.append({'status': 'closed', 'type': 'connection', "from": tokens[1], "to": tokens[2], "body": tokens[3]})
		else:
			die("Could not parse line: " + line)

def saveFile(filename, nodes, connections):
	f = open(filename, "w")
	for node in nodes:
		f.write("node '" + node["head"] + "' '" + str(node['x']) + "' '" + str(node['y']) + "' '" + node['body'] + "'\n")
	for connection in connections:
		f.writeline("connection '" + connection["from"] + "' '" + node['to'] + "' '" + node['body'] + "'")
	f.close()

def getBodyPosition(node):
	if node['status'] != 'open':
		die('getBodyPosition(): node is not open')
	return node['x'], node['y'] + getHeadSize(node)[1] + 2 * PADDING

def getObjectAtMouse():
	global canvas, focus, cursorX, cursorY
	for node in nodes:
		sizeX, sizeY = getHeadSize(node)
		if node["x"] - sizeX/2 - PADDING < cursorX and node["x"] + sizeX/2 + PADDING > cursorX and node["y"] - sizeY/2 - PADDING < cursorY and node["y"] + sizeY/2 + PADDING > cursorY:
			return node
		elif node['status'] == 'open':
			bodyPosX, bodyPosY = getBodyPosition(node)
			bodySizeX, bodySizeY = getBodySize(node)
			if bodyPosX - bodySizeX/2 - PADDING < cursorX and bodyPosX + bodySizeX/2 + PADDING > cursorX and bodyPosY - bodySizeY/2 - PADDING < cursorY and bodyPosY + bodySizeY/2 + PADDING > cursorY:
				return {'type': 'nodebody', 'node': node}
	# for connection in connections:
	return None

def getHeadSize(node):
	global editdata
	if editdata['object'] == node and editdata['type'] == 'node':
		text = editdata['text']
	else:
		text = node['head']
	m = 0
	for line in text.split("\\n"):
		m = max(m, len(line))
	x = 7 * m
	if text == "":
		y = 0
	else:
		y = 14 * (1+text.count("\\n"))
	return x, y

def getBodySize(node):
	global editdata
	if editdata['object'] == node and editdata['type'] == 'nodebody':
		text = editdata['text']
	else:
		text = node['body']
	m = 0
	for line in text.split("\\n"):
		m = max(m, len(line))
	x = 7 * m
	if text == "":
		y = 0
	else:
		y = 14 * (1+text.count("\\n"))
	return x, y

def render():
	global canvas, focus, nodes, connections, editdata
	canvas.delete("all")
	canvas.create_rectangle(0, 0, 800, 600, fill="white")
	for connection in connections:
		canvas.create_line()
	for node in nodes:
		renderPosX = 400 + node["x"] - focus[0]
		renderPosY = 300 + node["y"] - focus[1]
		sizeX, sizeY = getHeadSize(node)
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING, renderPosY - sizeY/2 - PADDING, renderPosX + sizeX/2 + PADDING, renderPosY + sizeY/2 + PADDING, fill=HEADCOLOR)

		# if node is edited
		if editdata['object'] == node and editdata['type'] == 'node':
			# render edit environment
			canvas.create_rectangle(renderPosX - sizeX/2 - PADDING/2, renderPosY - sizeY/2 - PADDING/2, renderPosX + sizeX/2 + PADDING/2, renderPosY + sizeY/2 + PADDING/2, fill=EDITCOLOR)
			canvas.create_text((renderPosX - sizeX/2, renderPosY - sizeY/2), anchor="nw", text=editdata['text'])
		else:
			canvas.create_text((renderPosX - sizeX/2, renderPosY - sizeY/2), anchor="nw", text=node["head"])
		if node['status'] == 'open':
			bodyRenderPosX = 400 + getBodyPosition(node)[0] - focus[0]
			bodyRenderPosY = 300 + getBodyPosition(node)[1] - focus[1]
			bodySizeX, bodySizeY = getBodySize(node)
			canvas.create_rectangle(bodyRenderPosX - bodySizeX/2 - PADDING, bodyRenderPosY - bodySizeY/2 - PADDING, bodyRenderPosX + bodySizeX/2 + PADDING, bodyRenderPosY + bodySizeY/2 + PADDING, fill=BODYCOLOR)
			# if body is edited
			if editdata['object'] == node and editdata['type'] == 'nodebody':
				canvas.create_rectangle(bodyRenderPosX - bodySizeX/2 - PADDING/2, bodyRenderPosY - bodySizeY/2 - PADDING/2, bodyRenderPosX + bodySizeX/2 + PADDING/2, bodyRenderPosY + bodySizeY/2 + PADDING/2, fill=EDITCOLOR)
				canvas.create_text((bodyRenderPosX - bodySizeX/2, bodyRenderPosY - bodySizeY/2), anchor="nw", text=editdata["text"])
			else:
				canvas.create_text((bodyRenderPosX - bodySizeX/2, bodyRenderPosY - bodySizeY/2), anchor="nw", text=node["body"])

def destroyPopup():
	global popupmenu
	if popupmenu != None:
		popupmenu.destroy()
		popupmenu = None

# events

def onClick(event):
	global mouseXLeft, mouseYLeft, draggedObject
	destroyPopup()
	d = event.__dict__
	mouseXLeft = d['x_root']
	mouseYLeft = d['y_root']
	draggedObject = getObjectAtMouse()

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

def createNode(x, y):
	global nodes
	nodes.append({'status': 'closed', 'type': 'node', 'head': '', 'x': x, 'y': y, 'body': ''})
	setSaved(False)
	render()

def deleteNode(node):
	global nodes
	nodes.remove(node)
	setSaved(False)
	render()

def editNode(node):
	global nodes, editdata
	editdata['object'] = node
	editdata['type'] = 'node'
	editdata['text'] = node['head']
	render()

def editNodeBody(node):
	global nodes, editdata
	editdata['object'] = node
	editdata['type'] = 'nodebody'
	editdata['text'] = node['body']
	render()

# def createConnection(): TODO

def deleteConnection(connection):
	global connections
	connections.remove(connection)
	setSaved(False)
	render()

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

def resetEditdata():
	global editdata
	editdata = dict()
	editdata['text'] = None
	editdata['object'] = None
	editdata['type'] = None

def onKeyPress(event):
	global editdata
	char = repr(event.char)[1:-1] # 'wow' -> wow

	if char in string.printable:
		editdata['text'] += char
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
	elif char == "\\x08":
		editdata['text'] = editdata['text'][:-1]
		render()
	elif char == "\\r":
		editdata['text'] += "\n"
		render()
	else:
		print(char, event.state)

def updateMouse(event):
	global cursorX, cursorY, focus
	cursorX = event.x - 400 + focus[0]
	cursorY = event.y - 300 + focus[1]

# decision

def checkDecision():
	global decision, decisionwindow
	if decision != None:
		decisionwindow.quit()
		decisionwindow.destroy()
		decisionwindow = None
	else:
		decisionwindow.after(20, checkDecision)

def decideNo():
	global decision
	decision = False

def decideYes():
	global decision
	decision = True

def reallyDiscardContent():
	global saved, decisionwindow, decision
	decision = None
	if not saved:
		decisionwindow = tkinter.Tk()
		decisionwindow.wm_title("Do you really want to discard your current changes?")
		label = tkinter.Label(decisionwindow, text="Pressing 'Yes' will discard your current changes")
		buttonYes = tkinter.Button(decisionwindow, text="Yes", command=decideYes)
		buttonNo = tkinter.Button(decisionwindow, text="Cancel", command=decideNo)
		label.pack()
		buttonYes.pack()
		buttonNo.pack()
		checkDecision()
		decisionwindow.mainloop()
		tmp = decision
		decision = None
		return tmp
	return True

def restart(filename=None):
	global openfilename, dragging, nodes, connections, focus, saved, editdata
	resetEditdata()
	openfilename = filename
	dragging = False
	focus = (0, 0) # what coordinates are centered
	if openfilename != None:
		loadFile(openfilename)
	else:
		nodes = list()
		connections = list()
	setSaved(True)
	render()

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

def setSaved(b):
	global saved, window, openfilename
	saved = b
	title = "diagrammer - "
	if openfilename == None:
		title += "<Unsaved Document>"
	else:
		title += openfilename

	if not saved:
		title += " *"
	window.wm_title(title)

def main():
	global canvas, cursorX, cursorY, window, popupmenu

	popupmenu = None
	cursorX = 0
	cursorY = 0

	window = tkinter.Tk()

	# menu
	menu = tkinter.Menu(window)
	window.config(menu=menu)
	filemenu = tkinter.Menu(menu)
	menu.add_cascade(label="File", menu=filemenu)
	filemenu.add_command(label="New", command=menu_new)
	filemenu.add_command(label="Open File", command=menu_openFile)
	filemenu.add_command(label="Save File", command=menu_saveFile)
	filemenu.add_command(label="Save File As", command=menu_saveFileAs)
	filemenu.add_command(label="Close", command=menu_close)

	window.minsize(800, 600)
	window.maxsize(800, 600)
	window.bind("<Button-1>", onClick) # fully show node / edit mode
	window.bind("<Button-3>", onRightClick) # create node / connection
	window.bind("<ButtonRelease-1>", onRelease)
	window.bind("<ButtonRelease-3>", onRightRelease)
	window.bind("<B1-Motion>", onDrag) # move node
	window.bind("<B3-Motion>", onRightDrag) # move screen
	window.bind("<Key>", onKeyPress) # enter text
	window.bind("<Motion>", updateMouse)
	canvas = tkinter.Canvas(window, width=800, height=600)
	canvas.pack()

	if len(sys.argv) == 1:
		restart()
	elif len(sys.argv) == 2:
		restart(sys.argv[1])
	else:
		die(usage)

	window.mainloop()

if __name__ == "__main__":
	main()
