#!/usr/bin/python3

def getObjectAtMouse():
	global canvas, focus, cursorX, cursorY
	for node in nodes:
		sizeX, sizeY = getHeadSize(node)
		if node["x"] - sizeX/2 - PADDING < cursorX and node["x"] + sizeX/2 + PADDING > cursorX and node["y"] - sizeY/2 - PADDING < cursorY and node["y"] + sizeY/2 + PADDING > cursorY:
			return node
		elif node['status'] == 'open':
			bodyPosX, bodyPosY = getBodyPosition(node)
			bodySizeX, bodySizeY = getBodySize(node)
			if bodyPosX - bodySizeX/2 - PADDING < cursorX and bodyPosX + bodySizeX/2 + PADDING > cursorX and bodyPosY - bodySizeY/2 - PADDING < cursorY and bodyPosY + bodySizeY/2 + PADDING > cursorY:
				return {'type': 'nodebody', 'node': node}
	# for connection in connections:
	return None

def getTextSize(text):
	global codefont, stdfont

	x = 0
	code = False
	for line in text.split("\n"):
		line.find("`")
		x = max(x, font.measure(line))
	if text == "":
		y = 0
	else:
		y = font.metrics()['linespace'] * (1+text.count("\n"))
	return x, y

def getHeadSize(node):
	global editdata
	if editdata['object'] == node and editdata['type'] == 'node':
		text = editdata['text']
	else:
		text = node['head']
	return getTextSize(text)

def getBodyPosition(node):
	if node['status'] != 'open':
		die('getBodyPosition(): node is not open')
	return node['x'], node['y'] + getHeadSize(node)[1]/2 + getBodySize(node)[1]/2 + 2 * PADDING

def getBodySize(node):
	global editdata, font
	if editdata['object'] == node and editdata['type'] == 'nodebody':
		text = editdata['text']
	else:
		text = node['body']
	return getTextSize(text)

def renderConnection(connection):
	die("TODO: renderConnection")

def renderEditText(x, y, text, cursor):
	renderLines(x, y, [line for line in text.split("\n")])
	# TODO render cursor

def renderText(x, y, text):
	# TODO source-`code`
	renderLines(x, y, [line for line in text.split("\n")])

def renderLines(x, y, lines):
	global canvas, font

	for line in lines:
		canvas.create_text((x, y), anchor="nw", text=line, font=font)
		y += font.metrics()['linespace']

def renderNodeHead(node, editing=False):
	global focus, canvas, editdata

	renderPosX = 400 + node["x"] - focus[0]
	renderPosY = 300 + node["y"] - focus[1]
	sizeX, sizeY = getHeadSize(node)
	canvas.create_rectangle(renderPosX - sizeX/2 - PADDING, renderPosY - sizeY/2 - PADDING, renderPosX + sizeX/2 + PADDING, renderPosY + sizeY/2 + PADDING, fill=HEADCOLOR)

	if editing:
		# render edit environment
		canvas.create_rectangle(renderPosX - sizeX/2 - PADDING/2, renderPosY - sizeY/2 - PADDING/2, renderPosX + sizeX/2 + PADDING/2, renderPosY + sizeY/2 + PADDING/2, fill=EDITCOLOR)
		renderEditText(renderPosX - sizeX/2, renderPosY - sizeY/2, editdata['text'], editdata['cursor'])
	else:
		renderText(renderPosX - sizeX/2, renderPosY - sizeY/2, node['head'])

def renderNodeBody(node, editing=False):
	global focus, canvas, editdata

	bodyRenderPosX = 400 + getBodyPosition(node)[0] - focus[0]
	bodyRenderPosY = 300 + getBodyPosition(node)[1] - focus[1]
	bodySizeX, bodySizeY = getBodySize(node)
	canvas.create_rectangle(bodyRenderPosX - bodySizeX/2 - PADDING, bodyRenderPosY - bodySizeY/2 - PADDING, bodyRenderPosX + bodySizeX/2 + PADDING, bodyRenderPosY + bodySizeY/2 + PADDING, fill=BODYCOLOR)

	if editing:
		canvas.create_rectangle(bodyRenderPosX - bodySizeX/2 - PADDING/2, bodyRenderPosY - bodySizeY/2 - PADDING/2, bodyRenderPosX + bodySizeX/2 + PADDING/2, bodyRenderPosY + bodySizeY/2 + PADDING/2, fill=EDITCOLOR)
		renderEditText(bodyRenderPosX - bodySizeX/2, bodyRenderPosY - bodySizeY/2, editdata["text"], editdata['cursor'])
	else:
		renderText(bodyRenderPosX - bodySizeX/2, bodyRenderPosY - bodySizeY/2, node["body"])

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
	canvas.create_rectangle(0, 0, 800, 600, fill="white")
	for connection in connections:
		renderConnection(connection)
	for node in nodes:
		renderNode(node)
