#!/usr/bin/python3

usage="Usage:\tdiagrammer <file>"
import sys
import tkinter

def die(msg):
	print(msg)
	sys.exit()

def loadFile(filename):
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
			nodes.append({"name": tokens[1], "x": int(tokens[2]), "y": int(tokens[3]), "desc": tokens[4]})
		elif line.startswith("connection"):
			connections.append({"name": tokens[1], "desc": tokens[2]})
		else:
			die("Could not parse line: " + line)
	return nodes, connections

def saveFile(filename, nodes, connections):
	print("TODO")

def getTextWidth(text):
	m = 0
	for line in text.split("\\n"):
		m = max(m, len(line))
	return 7 * m

def getTextHeight(text):
	return 14 * (1+text.count("\\n"))

def render():
	global canvas, focus, nodes, connections, chosenObject
	canvas.delete("all")
	canvas.create_rectangle(0, 0, 800, 600, fill="white")
	for connection in connections:
		if connection == chosenObject:
			die("chosen? D:")
		else:
			canvas.create_line()
	for node in nodes:
		renderPosX = 400 + node["x"] - focus[0]
		renderPosY = 300 + node["y"] - focus[1]
		sizeX = getTextWidth(node["name"])
		sizeY = getTextHeight(node["name"])
		canvas.create_rectangle(renderPosX - sizeX/2, renderPosY - sizeY/2, renderPosX + sizeX/2, renderPosY + sizeY/2, fill="grey")
		canvas.create_text((renderPosX - sizeX/2, renderPosY - sizeY/2), anchor="nw", text=node["name"])
		if node == chosenObject:
			die("chosen?")
			# TODO render description

def onClick(event): pass

def onRelease(event):
	global dragging
	if dragging == False:
		print("select node/connection")
	dragging = False

def onRightClick(event):
	global mouseXRight, mouseYRight
	d = event.__dict__
	mouseXRight = d['x_root']
	mouseYRight = d['y_root']

def onRightRelease(event):
	global dragging
	if dragging == False:
		print("create node/connection? ")
	dragging = False

def onDrag(event):
	global dragging
	dragging = True
	print("move chosen node/connection")

def onRightDrag(event):
	global focus, mouseXRight, mouseYRight, dragging
	d = event.__dict__
	focus = (focus[0] + mouseXRight - d['x_root'], focus[1] + mouseYRight - d['y_root'])
	render()
	mouseXRight = d['x_root']
	mouseYRight = d['y_root']
	dragging = True

def onKeyPress(event):
	print("key event")

def main(filename):
	global nodes, connections, canvas, chosenObject, focus, dragging
	dragging = False
	chosenObject = None
	nodes, connections = loadFile(filename)

	focus = (0, 0)

	window = tkinter.Tk()
	window.minsize(800, 600)
	window.maxsize(800, 600)
	window.bind("<Button-1>", onClick) # fully show node / edit mode
	window.bind("<Button-3>", onRightClick) # create node / connection
	window.bind("<ButtonRelease-1>", onRelease)
	window.bind("<ButtonRelease-3>", onRightRelease)
	window.bind("<B1-Motion>", onDrag) # move node
	window.bind("<B3-Motion>", onRightDrag) # move screen
	window.bind("<Key>", onKeyPress) # enter text
	canvas = tkinter.Canvas(window, width=800, height=600)
	canvas.pack()
	render()
	window.mainloop()

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		die(usage)
