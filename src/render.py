#!/usr/bin/python3

def renderConnectionPaths(connection):
	global canvas, focus, nodes
	toX = 400 + nodes[connection['to']]['x'] - focus[0]
	toY = 300 + nodes[connection['to']]['y'] - focus[1]
	for src in connection['from']:
		x = 400 + nodes[src]['x'] - focus[0]
		y = 300 + nodes[src]['y'] - focus[1]
		canvas.create_line(x, y, toX, toY)

def renderConnection(connection):
	global nodes, canvas, focus
	if connection['status'] == 'closed':
		dst = nodes[connection['to']]
		if connection['anchor'] == 'left':
			x = dst['x'] - getHeadSize(dst)[0]/2 - 6
			y = dst['y'] - getHeadSize(dst)[1]/2 + connection['anchoroffset'] + 6
		elif connection['anchor'] == 'right':
			x = dst['x'] + getHeadSize(dst)[0]/2 + 6
			y = dst['y'] - getHeadSize(dst)[1]/2 + connection['anchoroffset'] + 6
		elif connection['anchor'] == 'top':
			x = dst['x'] - getHeadSize(dst)[0]/2 + connection['anchoroffset'] + 6
			y = dst['y'] - getHeadSize(dst)[1]/2 - 6
		elif connection['anchor'] == 'bot':
			x = dst['x'] - getHeadSize(dst)[0]/2 + connection['anchoroffset'] + 6
			y = dst['y'] + getHeadSize(dst)[1]/2 + 6
		else:
			die("unknown connection anchor=" + str(connection['anchor']))

		x = 400 + x - focus[0]
		y = 300 + y - focus[1]

		canvas.create_rectangle(x-6, y-6, x+6, y+6, fill=CONNECTIONCOLOR)
	else:
		print("open connection yet?")

def renderNodeHead(node, editing=False):
	global focus, canvas, editdata

	renderPosX = 400 + node["x"] - focus[0]
	renderPosY = 300 + node["y"] - focus[1]

	if editing:
		box = EditTextBox(editdata['text'])
		sizeX, sizeY = box.getSize()

		# head box
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING, renderPosY - sizeY/2 - PADDING, renderPosX + sizeX/2 + PADDING, renderPosY + sizeY/2 + PADDING, fill=HEADCOLOR)

		# edit box
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING/2, renderPosY - sizeY/2 - PADDING/2, renderPosX + sizeX/2 + PADDING/2, renderPosY + sizeY/2 + PADDING/2, fill=EDITCOLOR)

		# text
		box.render(renderPosX, renderPosY)
	else:
		box = TextBox(node['head'])
		sizeX, sizeY = box.getSize()

		# head box
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING, renderPosY - sizeY/2 - PADDING, renderPosX + sizeX/2 + PADDING, renderPosY + sizeY/2 + PADDING, fill=HEADCOLOR)

		# text
		box.render(renderPosX, renderPosY)

def renderNodeBody(node, editing=False):
	global focus, canvas, editdata

	renderPosX = 400 + getBodyPosition(node)[0] - focus[0]
	renderPosY = 300 + getBodyPosition(node)[1] - focus[1]

	if editing:
		box = EditTextBox(editdata['text'])
		sizeX, sizeY = box.getSize()

		# body box
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING, renderPosY - sizeY/2 - PADDING, renderPosX + sizeX/2 + PADDING, renderPosY + sizeY/2 + PADDING, fill=BODYCOLOR)

		# edit box
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING/2, renderPosY - sizeY/2 - PADDING/2, renderPosX + sizeX/2 + PADDING/2, renderPosY + sizeY/2 + PADDING/2, fill=EDITCOLOR)

		# text
		box.render(renderPosX, renderPosY)
	else:
		box = TextBox(node['body'])
		sizeX, sizeY = box.getSize()

		# body box
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING, renderPosY - sizeY/2 - PADDING, renderPosX + sizeX/2 + PADDING, renderPosY + sizeY/2 + PADDING, fill=BODYCOLOR)

		# text
		box.render(renderPosX, renderPosY)

def renderNode(node):
	global editdata
	# if node is edited
	if editdata['object'] == node:
		renderNodeHead(node, editing=(editdata['type'] == 'node'))
		if node['status'] == 'open':
			renderNodeBody(node, editing=(editdata['type'] == 'nodebody'))
	else:
		renderNodeHead(node)
		if node['status'] == 'open':
			renderNodeBody(node)

def render():
	global canvas, nodes, connections
	canvas.delete("all")
	canvas.create_rectangle(0, 0, 800, 600, fill=BACKGROUNDCOLOR)
	for connection in reversed(connections):
		renderConnectionPaths(connection)

	for connection in reversed(connections):
		renderConnection(connection)

	for node in reversed(nodes):
		renderNode(node)
