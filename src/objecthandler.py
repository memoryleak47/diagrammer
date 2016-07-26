#!/usr/bin/python3

def getObjectAtMouse():
	global canvas, focus, cursorX, cursorY, nodes, connections
	l = nodes + connections
	if nodeBodyVisible():
		l.insert(0, getVisibleNodeBody())

	for thingy in l:
		sizeX, sizeY = thingy.getSizeX(), thingy.getSizeY()
		if thingy.getX() - sizeX/2 < cursorX and thingy.getX() + sizeX/2 > cursorX and thingy.getY() - sizeY/2 < cursorY and thingy.getY() + sizeY/2 > cursorY:
			return thingy
	return None

def createNode(x, y):
	global nodes
	nodes.append(Node(text='', x=x, y=y, bodytext=''))
	setSaved(False)
	render()

def deleteNode(node):
	global nodes, connections, status
	index = nodes.index(node)

	for connection in connections:
		i = 0
		if connection.getDstId() == index:
			connections.remove(connection)
		else:
			srcs = connection.getSrcIds()
			while i < len(srcs):
				# node-ids get lower -> connections should get lower
				if srcs[i] > index:
					srcs[i] -= 1
					i += 1
				# remove removed connection-sources
				elif srcs[i] == index:
					connection.removeSrc(nodes[srcs[i]])
				else:
					i += 1
	if 'object' in status and status['object'] == node.getNodeBody():
		resetStatus()
	nodes.remove(node)
	setSaved(False)
	render()

def createConnection(obj):
	global connections, nodes
	# obj == dst-node
	connection = Connection(dstid=nodes.index(obj), x=obj.getX(), y=obj.getY())
	connections.append(connection)
	setSaved(False)
	render()

def deleteConnection(connection):
	global connections
	connections.remove(connection)
	setSaved(False)
	render()
