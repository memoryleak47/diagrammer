#!/usr/bin/python3

def getHeadSize(node):
	if editdata['object'] == node and editdata['type'] == 'node':
		return EditTextBox(editdata['text']).getSize()
	else:
		return TextBox(node['head']).getSize()

def getBodySize(node):
	if editdata['object'] == node and editdata['type'] == 'nodebody':
		return EditTextBox(node['body']).getSize()
	else:
		return TextBox(node['body']).getSize()

def getBodyPosition(node):
	global editdata

	if node['status'] != 'open':
		die('getBodyPosition(): node is not open')

	headheight = getHeadSize(node)[1]
	bodyheight = getBodySize(node)[1]

	return node['x'], node['y'] + headheight/2 + bodyheight/2 + 2 * PADDING
