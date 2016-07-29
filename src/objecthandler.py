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
	requestRender()

def deleteNode(node):
	global nodes, connections, status
	index = nodes.index(node)

	for connection in connections:
		# update dst
		if connection.getDstId() == index:
			connections.remove(connection)
			continue
		if connection.getDstId() > index:
			connection.setDstId(connection.getDstId()-1)
		# update srcs
		srcs = connection.getSrcIds()
		i = 0
		while i < len(srcs):
			# node-ids get lower -> connections should get lower
			if srcs[i] > index:
				srcs[i] -= 1
				i += 1
			# remove removed connection-sources
			elif srcs[i] == index:
				srcs.remove(srcs[i])
			else:
				i += 1
		connection.setSrcIds(srcs)
	if 'object' in status and status['object'] == node.getNodeBody():
		resetStatus()
	nodes.remove(node)
	setSaved(False)
	requestRender()

def createConnection(obj):
	global connections, nodes
	# obj == dst-node
	connection = Connection(dstid=nodes.index(obj), x=obj.getX(), y=obj.getY(), srcids=list())
	connections.append(connection)
	setSaved(False)
	requestRender()

def deleteConnection(connection):
	global connections
	connections.remove(connection)
	setSaved(False)
	requestRender()
