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
		x, y = getPosition(connection)
		sizeX, sizeY = getSize(connection)
		if x - sizeX/2 < cursorX and x + sizeX/2 > cursorX and y - sizeY/2 < cursorY and y + sizeY/2 > cursorY:
			return connection
	return None

def createNode(x, y):
	global nodes
	nodes.append({'status': 'closed', 'type': 'node', 'head': '', 'x': x, 'y': y, 'body': ''})
	setSaved(False)

def deleteNode(node):
	global nodes, connections
	for connection in connections:
		i = 0
		srcs = connection['from']
		while i < len(srcs):
			# node-ids get lower -> connections should get lower
			if srcs[i] > nodes.index(node):
				srcs[i] -= 1
				i += 1
			# remove removed connection-sources
			elif srcs[i] == nodes.index(node):
				srcs.remove(srcs[i])
			else:
				i += 1
	nodes.remove(node)
	setSaved(False)

def createConnection(obj):
	global connections, nodes
	# obj == dst-node
	connection = {'status': 'closed', 'type': 'connection', 'from': list(), 'to': nodes.index(obj), 'x': obj['x'], 'y': obj['y'], 'body': ''}
	repositionConnection(connection)
	connections.append(connection)
	setSaved(False)

def deleteConnection(connection):
	global connections
	connections.remove(connection)
	setSaved(False)
