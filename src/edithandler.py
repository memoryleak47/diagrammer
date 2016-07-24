#!/usr/bin/python3

def setEditText(text):
	global status
	status['text'] = text

	if status['object'].getType() == 'node':
		status['object'].updateConnections()

def editNode(node):
	global nodes, status
	status = {'type': 'edit', 'object': node, 'text': node.getText(), 'cursor': 0}
	node.updateConnections()

def editNodeBody(body):
	global nodes, status
	status = {'type': 'edit', 'object': body, 'text': body.getText(), 'cursor': 0}

def editConnection(connection):
	global nodes, status
	status = {'type': 'edit', 'object': connection, 'text': connection.getText(), 'cursor': 0}
	connection.update()

def incCursor():
	global status
	status['cursor'] = min(status['cursor']+1, len(status['text']))

def decCursor():
	global status
	status['cursor'] = max(0, status['cursor']-1)
