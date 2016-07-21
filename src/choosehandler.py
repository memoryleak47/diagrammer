#!/usr/bin/python3

def resetChooseData():
	global choosedata
	choosedata = {'type': 'none', 'connection': None}

def chooseAddSource(connection):
	global choosedata
	choosedata = {'type': 'add', 'connection': connection}
	
def chooseRemoveSource(connection):
	global choosedata
	choosedata = {'type': 'remove', 'connection': connection}
