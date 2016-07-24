#!/usr/bin/python3

def resetStatus():
	global status
	status = {'type': 'none'}

def nodeBodyVisible():
	global status
	return (status['type'] == 'edit' or status['type'] == 'open') and status['object'].getType() == 'nodebody'

def getVisibleNodeBody():
	if nodeBodyVisible():
		return status['object']
	die("getVisibleNodeBody(): no nodebody visible")
