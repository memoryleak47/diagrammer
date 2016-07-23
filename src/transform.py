#!/usr/bin/python3

def getPosition(thingy):
	global editdata
	if thingy['type'] == 'node' or thingy['type'] == 'connection':
		return thingy['x'], thingy['y']	
	elif thingy['type'] == 'nodebody':

		node = thingy['node']
		if node['status'] != 'open':
			die('getPosition(): node is not open')

		headheight = getSize(node)[1]
		bodyheight = getSize(getNodeBody(node))[1]

		return node['x'], node['y'] + headheight/2 + bodyheight/2
	else:
		die("getPosition(): awkward type=" + thingy['type'])

def getSize(thingy):
	global editdata
	if thingy['type'] == 'node':
		if editdata['object'] == thingy and editdata['type'] == 'node':
			return EditTextBox(editdata['text']).getObjectSize()
		else:
			return TextBox(thingy['head']).getObjectSize()
	elif thingy['type'] == 'nodebody':
		if editdata['object'] == thingy['node'] and editdata['type'] == 'nodebody':
			return EditTextBox(editdata['text']).getObjectSize()
		else:
			return TextBox(thingy['node']['body']).getObjectSize()
	elif thingy['type'] == 'connection':
		if thingy['status'] == 'closed':
			return CONNECTIONSIZE, CONNECTIONSIZE
		else:
			if editdata['object'] == thingy:
				return EditTextBox(editdata['text']).getObjectSize()
			else:
				return TextBox(thingy['body']).getObjectSize()
	else:
		die("getSize(): awkward type=" + thingy['type'])

def getNodeBody(node):
	return {'node': node, 'type': 'nodebody'}

def move(obj, amount):
	global connections, nodes

	obj['x'] += amount[0]
	obj['y'] += amount[1]

	if obj['type'] == 'node':
		for connection in connections:
			if connection['to'] == nodes.index(obj):
				connection['x'] += amount[0]
				connection['y'] += amount[1]
