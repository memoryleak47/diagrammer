#!/usr/bin/python3

def getTextSize(text):
	global codefont, stdfont

	x = 0
	for line in text.split("\n"):
		line.find("`")
		x = max(x, stdfont.measure(line))
	if text == "":
		y = 0
	else:
		y = stdfont.metrics()['linespace'] * (1+text.count("\n"))
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
	global editdata, codefont, stdfont
	if editdata['object'] == node and editdata['type'] == 'nodebody':
		text = editdata['text']
	else:
		text = node['body']
	return getTextSize(text)
