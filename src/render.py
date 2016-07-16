#!/usr/bin/python3

def renderConnection(connection):
	die("TODO: renderConnection")

def renderEditText(x, y, text, cursor):
	global focus, stdfont

	lines = [line for line in text.split("\n")]
	renderLines(x, y, lines)

	y = 0
	for i in range(len(lines)):
		if cursor <= len(lines[i]):
			x = 400 - focus[0] + stdfont.measure(lines[i][:cursor]) - getTextSize(text)[0]/2
			y = 300 - focus[1] + stdfont.metrics()['linespace'] * y - getTextSize(text)[1]/2
			canvas.create_rectangle((x, y), x+2, y + stdfont.metrics()['linespace'], fill="black")
			return
		else:
			cursor -= len(lines[i])
			y += 1

def renderText(x, y, text):
	# TODO source-`code`
	renderLines(x, y, [line for line in text.split("\n")])

def renderLines(x, y, lines):
	global canvas, codefont, stdfont

	for line in lines:
		canvas.create_text((x, y), anchor="nw", text=line, font=stdfont)
		y += stdfont.metrics()['linespace']

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
	canvas.create_rectangle(0, 0, 800, 600, fill=BACKGROUNDCOLOR)
	for connection in connections:
		renderConnection(connection)
	for node in nodes:
		renderNode(node)
