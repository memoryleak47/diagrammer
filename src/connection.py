#!/usr/bin/python3

def repositionConnection(connection):
	global nodes
	node = nodes[connection['to']]

	nodeSize = getSize(node)
	connectionSize = getSize(connection)
	xDiff = (connection['x'] - node['x'])/nodeSize[0]
	yDiff = (connection['y'] - node['y'])/nodeSize[1]

	if abs(xDiff) > abs(yDiff):
		if xDiff < 0:
			connection['x'] = node['x'] - nodeSize[0]/2 - connectionSize[0]/2
			connection['y'] = min(node['y'] + nodeSize[1]/2 + connectionSize[1]/2, max(node['y'] - nodeSize[1]/2 - connectionSize[1]/2, connection['y']))
		else:
			connection['x'] = node['x'] + nodeSize[0]/2 + connectionSize[0]/2
			connection['y'] = min(node['y'] + nodeSize[1]/2 + connectionSize[1]/2, max(node['y'] - nodeSize[1]/2 - connectionSize[1]/2, connection['y']))
	else:
		if yDiff < 0:
			connection['y'] = node['y'] - nodeSize[1]/2 - connectionSize[1]/2
			connection['x'] = min(node['x'] + nodeSize[0]/2 + connectionSize[0]/2, max(node['x'] - nodeSize[0]/2 - connectionSize[0]/2, connection['x']))
		else:
			connection['y'] = node['y'] + nodeSize[1]/2 + connectionSize[1]/2
			connection['x'] = min(node['x'] + nodeSize[0]/2 + connectionSize[0]/2, max(node['x'] - nodeSize[0]/2 - connectionSize[0]/2, connection['x']))
