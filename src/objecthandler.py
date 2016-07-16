#!/usr/bin/python3

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

def deleteConnection(connection):
	global connections
	connections.remove(connection)
	setSaved(False)
	render()
