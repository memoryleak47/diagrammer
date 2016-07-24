#!/usr/bin/python3

def chooseAddSource(connection):
	global nodes, status
	nodeids = list()
	for i in range(len(nodes)):
		if i not in connection.getSrcIds() and i != connection.getDstId():
			nodeids.append(i)
	status = {'type': 'choose_add', 'connection': connection, 'nodeids': nodeids, 'connection': connection}
	
def chooseRemoveSource(connection):
	global status
	nodeids = list()
	for i in range(len(nodes)):
		if i in connection.getSrcIds() and i != connection.getDstId():
			nodeids.append(i)
	status = {'type': 'choose_remove', 'connection': connection, 'nodeids': nodeids, 'connection': connection}
