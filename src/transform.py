#!/usr/bin/python3

def getPosition(thingy):
	global editdata
	if thingy['type'] == 'node':
		return thingy['x'], thingy['y']	
	elif thingy['type'] == 'nodebody':

		node = thingy['node']
		if node['status'] != 'open':
			die('getPosition(): node is not open')

		headheight = getSize(node)[1]
		bodyheight = getSize(getNodeBody(node))[1]

		return node['x'], node['y'] + headheight/2 + bodyheight/2
	elif thingy['type'] == 'connection':
		if thingy['status'] == 'closed':
			dst = nodes[thingy['to']]
			if thingy['anchor'] == 'left':
				x = dst['x'] - getSize(dst)[0]/2 - CONNECTIONSIZE/2
				y = dst['y'] - getSize(dst)[1]/2 + thingy['anchoroffset'] + CONNECTIONSIZE/2
			elif thingy['anchor'] == 'right':
				x = dst['x'] + getSize(dst)[0]/2 + CONNECTIONSIZE/2
				y = dst['y'] - getSize(dst)[1]/2 + thingy['anchoroffset'] + CONNECTIONSIZE/2
			elif thingy['anchor'] == 'top':
				x = dst['x'] - getSize(dst)[0]/2 + thingy['anchoroffset'] + CONNECTIONSIZE/2
				y = dst['y'] - getSize(dst)[1]/2 - CONNECTIONSIZE/2
			elif thingy['anchor'] == 'bot':
				x = dst['x'] - getSize(dst)[0]/2 + thingy['anchoroffset'] + CONNECTIONSIZE/2
				y = dst['y'] + getSize(dst)[1]/2 + CONNECTIONSIZE/2
			else:
				die("unknown connection anchor=" + str(thingy['anchor']))
			return x, y
		else:
			die("shbuu")

def getSize(thingy):
	global editdata
	if thingy['type'] == 'node':
		if editdata['object'] == thingy and editdata['type'] == 'node':
			return EditTextBox(editdata['text']).getObjectSize()
		else:
			return TextBox(thingy['head']).getObjectSize()
	elif thingy['type'] == 'nodebody':
		if editdata['object'] == thingy and editdata['type'] == 'nodebody':
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

def getNodeBody(node):
	return {'node': node, 'type': 'nodebody'}
