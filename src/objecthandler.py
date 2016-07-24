#!/usr/bin/python3

def getObjectAtMouse():
	global canvas, focus, cursorX, cursorY, nodes, connections
	l = nodes + connections
	if nodeBodyVisible():
		l.append(getVisibleNodeBody())

	for thingy in l:
		sizeX, sizeY = thingy.getSize()
		if thingy.getX() - sizeX/2 < cursorX and thingy.getX() + sizeX/2 > cursorX and thingy.getY() - sizeY/2 < cursorY and thingy.getY() + sizeY/2 > cursorY:
			return thingy
	return None

def createNode(x, y):
	global nodes
	nodes.append(Node(text='', x=x, y=y, bodytext=''))
	setSaved(False)

def deleteNode(node):
	global nodes, connections
	for connection in connections:
		i = 0
		srcs = connection.getSrcIds()
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
	connection = Connection(dstid=nodes.index(obj), x=obj.getX(), y=obj.getY())
	connection.update()
	connections.append(connection)
	setSaved(False)

def deleteConnection(connection):
	global connections
	connections.remove(connection)
	setSaved(False)
