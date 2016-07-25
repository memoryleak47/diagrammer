#!/usr/bin/python3

def chooseAddSource(connection):
	global nodes, status
	nodeids = list()
	for i in range(len(nodes)):
		if i not in connection.getSrcIds() and i != connection.getDstId():
			nodeids.append(i)
	statusChooseAdd(connection, nodeids)
	
def chooseRemoveSource(connection):
	global status
	nodeids = list()
	for i in range(len(nodes)):
		if i in connection.getSrcIds() and i != connection.getDstId():
			nodeids.append(i)
	statusChooseRemove(connection, nodeids)
