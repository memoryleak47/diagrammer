#!/usr/bin/python3

def editNode(node):
	global nodes, editdata
	editdata['object'] = node
	editdata['type'] = 'node'
	editdata['text'] = node['head']
	repositionConnections(node)

def editNodeBody(node):
	global nodes, editdata
	editdata['object'] = node
	editdata['type'] = 'nodebody'
	editdata['text'] = node['body']

def editConnection(connection):
	global nodes, editdata
	editdata['object'] = connection
	editdata['type'] = 'connection'
	editdata['text'] = connection['body']
	connection['status'] = 'open'
	repositionConnection(connection)

def resetEditdata():
	global editdata

	t, o = None, None
	if editdata != None:
		t = editdata['type']
		o = editdata['object']

	editdata = {'text': None, 'object': None, 'type': None, 'cursor': 0}

	if t == 'node':
		repositionConnections(o)
	elif t == 'connection':
		repositionConnection(o)

def setEditText(text):
	global editdata

	editdata['text'] = text
	if editdata['type'] == 'node':
		repositionConnections(editdata['object'])
	elif editdata['type'] == 'connection':
		repositionConnection(editdata['object'])

def incCursor():
	global editdata
	editdata['cursor'] = min(editdata['cursor']+1, len(editdata['text']))

def decCursor():
	global editdata
	editdata['cursor'] = max(0, editdata['cursor']-1)
