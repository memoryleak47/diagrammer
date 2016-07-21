#!/usr/bin/python3

def renderConnectionPaths(connection):
	global canvas, focus, nodes
	toX, toY = gameToScreenPos((nodes[connection['to']]['x'], nodes[connection['to']]['y']))
	for src in connection['from']:
		x, y = gameToScreenPos((nodes[src]['x'], nodes[src]['y']))
		canvas.create_line(x, y, toX, toY)

def renderConnection(connection):
	global nodes, canvas, focus, editdata

	if connection['status'] == 'open':
		renderPosX, renderPosY = gameToScreenPos(getPosition(connection))
		sizeX, sizeY = getSize(connection)


		if editdata != None and editdata['object'] == connection:
			box = EditTextBox(editdata['text'])
			sizeX, sizeY = box.getSize()

			# box
			canvas.create_rectangle(renderPosX - sizeX/2 - PADDING, renderPosY - sizeY/2 - PADDING, renderPosX + sizeX/2 + PADDING, renderPosY + sizeY/2 + PADDING, fill=CONNECTIONCOLOR)

			# edit box
			canvas.create_rectangle(renderPosX - sizeX/2 - PADDING/2, renderPosY - sizeY/2 - PADDING/2, renderPosX + sizeX/2 + PADDING/2, renderPosY + sizeY/2 + PADDING/2, fill=EDITCOLOR)

			# text
			box.render(renderPosX, renderPosY)
		else:
			# box
			canvas.create_rectangle(renderPosX - sizeX/2, renderPosY - sizeY/2, renderPosX + sizeX/2, renderPosY + sizeY/2, fill=CONNECTIONCOLOR)

			box = TextBox(connection['body'])
			sizeX, sizeY = box.getSize()

			# text
			box.render(renderPosX, renderPosY)
	else:
		renderPosX, renderPosY = gameToScreenPos(getPosition(connection))
		sizeX, sizeY = getSize(connection)

		# box
		canvas.create_rectangle(renderPosX - sizeX/2, renderPosY - sizeY/2, renderPosX + sizeX/2, renderPosY + sizeY/2, fill=CONNECTIONCOLOR)


def renderNodeHead(node, editing=False):
	global focus, canvas, editdata

	renderPosX, renderPosY = gameToScreenPos((node["x"], node['y']))

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

	pos = getPosition(getNodeBody(node))
	renderPosX, renderPosY = gameToScreenPos(pos)

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
