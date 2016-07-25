#!/usr/bin/python3


def nodeBodyVisible():
	global status
	return (status['type'] == 'edit' or status['type'] == 'open') and status['object'].getType() == 'nodebody'

def getVisibleNodeBody():
	if nodeBodyVisible():
		return status['object']
	die("getVisibleNodeBody(): no nodebody visible")

def resetStatus():
	global status
	status = {'type': 'none'}

def statusOpen(obj):
	global status
	status = {'type': 'open', 'object': obj}

def statusEdit(obj):
	global status
	status = {'type': 'edit', 'object': obj, 'text': obj.getText(), 'cursor': 0}

def statusChooseAdd(connection, nodeids):
	global status
	status = {'type': 'choose_add', 'connection': connection, 'nodeids': nodeids}

def statusChooseRemove(connection, nodeids):
	global status
	status = {'type': 'choose_remove', 'connection': connection, 'nodeids': nodeids}
