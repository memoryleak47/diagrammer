#!/usr/bin/python3

def repositionConnections(node):
	global connections, nodes

	for connection in connections:
		if connection['to'] == nodes.index(node):
			repositionConnection(connection)
