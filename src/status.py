#!/usr/bin/python3

def nodeBodyVisible():
	global status
	return (status['type'] == 'edit' or status['type'] == 'open') and status['object'].getType() == 'nodebody'

def getVisibleNodeBody():
	if nodeBodyVisible():
		return status['object']
	die("getVisibleNodeBody(): no nodebody visible")

def setStatus(new):
	global status
	if 'object' in status:
		obj = status['object']
		status = new
		obj.updateSize()
	else:
		status = new
	if 'object' in status:
		status['object'].updateSize()

def resetStatus():
	setStatus({'type': 'none'})

def statusOpen(obj):
	setStatus({'type': 'open', 'object': obj})

def statusEdit(obj):
	setStatus({'type': 'edit', 'object': obj, 'text': obj.getText(), 'cursor': 0})

def setEditText(txt):
	global status
	status['text'] = txt
	setStatus(status)

def statusChooseAdd(connection, nodeids):
	setStatus({'type': 'choose_add', 'connection': connection, 'nodeids': nodeids})

def statusChooseRemove(connection, nodeids):
	setStatus({'type': 'choose_remove', 'connection': connection, 'nodeids': nodeids})
