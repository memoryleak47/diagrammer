#!/usr/bin/python3

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
