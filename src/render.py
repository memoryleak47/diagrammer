#!/usr/bin/python3

def render():
	global canvas, nodes, connections, status, redrawNeeded, redrawing

	redrawNeeded = False
	redrawing = True

	canvas.delete("all")
	ssize = getScreenSize()
	canvas.create_rectangle(0, 0, ssize[0], ssize[1], fill=BACKGROUNDCOLOR)
	for connection in reversed(connections):
		connection.renderPaths()

	for connection in reversed(connections):
		connection.render()

	for node in reversed(nodes):
		node.render()

	if 'object' in status:
		status['object'].render()

	redrawing = False

def requestRender():
	global redrawNeeded
	redrawNeeded = True

def optRender():
	global redrawNeeded, redrawing

	if redrawNeeded and not redrawing:
		render()
