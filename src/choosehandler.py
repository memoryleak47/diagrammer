#!/usr/bin/python3

def resetChooseData():
	global choosedata
	choosedata = {'type': 'none', 'connection': None, 'nodeids': list()}

def chooseAddSource(connection):
	global choosedata, nodes
	nodeids = list()
	for i in range(len(nodes)):
		if i not in connection['from'] and i != connection['to']:
			nodeids.append(i)
	choosedata = {'type': 'add', 'connection': connection, 'nodeids': nodeids}
	
def chooseRemoveSource(connection):
	global choosedata
	nodeids = list()
	for i in range(len(nodes)):
		if i in connection['from'] and i != connection['to']:
			nodeids.append(i)
	choosedata = {'type': 'remove', 'connection': connection, 'nodeids': nodeids}
