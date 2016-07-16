#!/usr/bin/python3

def editNode(node):
	global nodes, editdata
	editdata['object'] = node
	editdata['type'] = 'node'
	editdata['text'] = node['head']
	render()

def editNodeBody(node):
	global nodes, editdata
	editdata['object'] = node
	editdata['type'] = 'nodebody'
	editdata['text'] = node['body']
	render()

def resetEditdata():
	global editdata
	editdata = dict()
	editdata['text'] = None
	editdata['object'] = None
	editdata['type'] = None
	editdata['cursor'] = 0

def incCursor():
	global editdata
	editdata['cursor'] = min(editdata['cursor']+1, len(editdata['text']))

def decCursor():
	global editdata
	editdata['cursor'] = max(0, editdata['cursor']-1)
