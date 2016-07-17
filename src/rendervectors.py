#!/usr/bin/python3

def getHeadSize(node):
	if editdata['object'] == node and editdata['type'] == 'node':
		return EditTextBox(editdata['text']).getObjectSize()
	else:
		return TextBox(node['head']).getObjectSize()

def getBodySize(node):
	if editdata['object'] == node and editdata['type'] == 'nodebody':
		return EditTextBox(editdata['text']).getObjectSize()
	else:
		return TextBox(node['body']).getObjectSize()

def getBodyPosition(node):
	global editdata

	if node['status'] != 'open':
		die('getBodyPosition(): node is not open')

	headheight = getHeadSize(node)[1]
	bodyheight = getBodySize(node)[1]

	return node['x'], node['y'] + headheight/2 + bodyheight/2
