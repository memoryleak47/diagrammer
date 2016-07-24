#!/usr/bin/python3

def editNode(node):
	global nodes, editdata
	editdata['object'] = node
	editdata['text'] = node['head']
	repositionConnections(node)

def editNodeBody(node):
	global nodes, editdata
	editdata['object'] = getNodeBody(node)
	editdata['text'] = node['body']

def editConnection(connection):
	global nodes, editdata
	editdata['object'] = connection
	editdata['text'] = connection['body']
	connection['status'] = 'open'
	repositionConnection(connection)

def resetEditdata():
	global editdata

	obj = None
	if editdata != None:
		obj = editdata['object']

	editdata = {'text': None, 'object': None, 'cursor': 0}

	if obj != None:
		if obj['type'] == 'node':
			repositionConnections(obj)
		elif obj['type'] == 'connection':
			repositionConnection(obj)

def setEditText(text):
	global editdata

	editdata['text'] = text
	if editdata['object']['type'] == 'node':
		repositionConnections(editdata['object'])
	elif editdata['object']['type'] == 'connection':
		repositionConnection(editdata['object'])

def incCursor():
	global editdata
	editdata['cursor'] = min(editdata['cursor']+1, len(editdata['text']))

def decCursor():
	global editdata
	editdata['cursor'] = max(0, editdata['cursor']-1)
