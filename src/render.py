#!/usr/bin/python3

def render():
	global canvas, nodes, connections, status

	canvas.delete("all")
	canvas.create_rectangle(0, 0, 800, 600, fill=BACKGROUNDCOLOR)
	for connection in reversed(connections):
		connection.renderPaths()

	for connection in reversed(connections):
		connection.render()

	for node in reversed(nodes):
		node.render()

	if nodeBodyVisible():
		status['object'].render()
