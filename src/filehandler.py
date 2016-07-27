#!/usr/bin/python3

import os

def loadFile(filename):
	global nodes, connections
	nodes = list()
	connections = list()

	if not os.path.isfile(filename):
		return

	f = open(filename)
	lines = f.readlines()
	f.close()

	for line in lines:
		tokens = list()
		line = line.strip()

		if line.startswith("node "):
			tokens.append("node")
			i = 5
		elif line.startswith("connection "):
			tokens.append("connection")
			i = 11
		else:
			die("Can not tokenize: " + line)
		while i < len(line):
			if line[i] == "'":
				tmp = ""
				i += 1
				while i < len(line):
					if line[i:i+2] == "\\'": # \'
						tmp += "'"
						i += 2
					elif line[i:i+2] == "\\\\": # \\
						tmp += "\\"
						i += 2
					elif line[i:i+2] == "\\`": # \`
						tmp += "\\`"
						i += 2
					elif line[i:i+2] == "\\n": # \n
						tmp += "\n"
						i += 2
					elif line[i:i+2] == "\\t": # \t
						tmp += "\t"
						i += 2
					elif line[i] == "'":
						break
					else:
						tmp += line[i]
						i += 1
				tokens.append(tmp)
				i += 1
			elif line[i] == " ":
				i += 1

		if tokens[0] == "node":
			nodes.append(Node(text=tokens[1], x=float(tokens[2]), y=float(tokens[3]), bodytext=tokens[4]))
		elif line.startswith("connection"):
			if tokens[1] == '':
				srcids = list()
			else:
				srcids = [int(x) for x in tokens[1].split(",")]
			connections.append(Connection(srcids=srcids, dstid=int(tokens[2]), x=float(tokens[3]), y=float(tokens[4]), text=tokens[5]))
		else:
			die("Could not parse line: " + line)

def saveFile(filename, nodes, connections):
	f = open(filename, "w")
	for node in nodes:
		f.write("node '" + node.getText().replace("\n", "\\n").replace("\t", "\\t") + "' '" + str(node.getX()) + "' '" + str(node.getY()) + "' '" + node.getNodeBody().getText().replace("\n", "\\n").replace("\t", "\\t") + "'\n")
	for connection in connections:
		f.write("connection '" + ",".join([str(x) for x in connection.getSrcIds()]) + "' '" + str(connection.getDstId()) + "' '" + str(connection.getX()) + "' '" + str(connection.getY()) + "' '" + connection.getContent() + "'\n")
	f.close()
