#!/usr/bin/python3

def renderConnection(connection):
	die("TODO: renderConnection")

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
		renderConnection(connection)
	for node in reversed(nodes):
		renderNode(node)
