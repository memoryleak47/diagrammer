#!/usr/bin/python3

def loadFile(filename):
	global nodes, connections
	nodes = list()
	connections = list()

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
			nodes.append({'status': 'closed', 'type': 'node', "head": tokens[1], "x": int(tokens[2]), "y": int(tokens[3]), "body": tokens[4]})
		elif line.startswith("connection"):
			connections.append({'status': 'closed', 'type': 'connection', "from": int(tokens[1]), "to": int(tokens[2]), "body": tokens[3]})
		else:
			die("Could not parse line: " + line)

def saveFile(filename, nodes, connections):
	f = open(filename, "w")
	for node in nodes:
		f.write("node '" + node["head"].replace("\n", "\\n").replace("\t", "\\t") + "' '" + str(node['x']) + "' '" + str(node['y']) + "' '" + node['body'].replace("\n", "\\n").replace("\t", "\\t") + "'\n")
	for connection in connections:
		f.writeline("connection '" + connection["from"] + "' '" + node['to'] + "' '" + node['body'] + "'")
	f.close()
