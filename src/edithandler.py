#!/usr/bin/python3

def setEditText(text):
	global status
	status['text'] = text

def editNode(node):
	global nodes, status
	statusEdit(node)

def editNodeBody(body):
	global nodes, status
	statusEdit(body)

def editConnection(connection):
	global nodes, status
	statusOpen(connection) # needed
	statusEdit(connection)

def incCursor():
	global status
	status['cursor'] = min(status['cursor']+1, len(status['text']))

def decCursor():
	global status
	status['cursor'] = max(0, status['cursor']-1)
