#!/usr/bin/python3

def setEditText(text):
	global status
	status['text'] = text
	setStatus(status)

def editNode(node):
	global nodes, status
	statusEdit(node)

def editNodeBody(body):
	global nodes, status
	statusEdit(body)

def editConnection(connection):
	global nodes, status
	statusEdit(connection)

def incCursor():
	global status
	status['cursor'] = min(status['cursor']+1, len(status['text']))
	setStatus(status)

def decCursor():
	global status
	status['cursor'] = max(0, status['cursor']-1)
	setStatus(status)
