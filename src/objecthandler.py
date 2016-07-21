#!/usr/bin/python3

def getObjectAtMouse():
	global canvas, focus, cursorX, cursorY, nodes, connections
	for node in nodes:
		sizeX, sizeY = getSize(node)
		if node["x"] - sizeX/2 < cursorX and node["x"] + sizeX/2 > cursorX and node["y"] - sizeY/2 < cursorY and node["y"] + sizeY/2 > cursorY:
			return node
		elif node['status'] == 'open':
			bodyPosX, bodyPosY = getPosition(getNodeBody(node))
			bodySizeX, bodySizeY = getSize(getNodeBody(node))
			if bodyPosX - bodySizeX/2 < cursorX and bodyPosX + bodySizeX/2 > cursorX and bodyPosY - bodySizeY/2 < cursorY and bodyPosY + bodySizeY/2 > cursorY:
				return getNodeBody(node)
	for connection in connections:
		if connection['status'] == 'closed':
			die("getObjectAtMouse() cant do closed connection")
		else:
			die("getObjectAtMouse() cant do open connection")
	return None

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

def createConnection(obj):
	global connections, nodes
	# obj == dst-node
	connections.append({'status': 'closed', 'type': 'connection', 'from': list(), 'to': nodes.index(obj), 'anchor': 'left', 'anchoroffset': 0, 'body': ''})
	setSaved(False)
	render()

def deleteConnection(connection):
	global connections
	connections.remove(connection)
	setSaved(False)
	render()
