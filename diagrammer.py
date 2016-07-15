#!/usr/bin/python3

usage="Usage:\tdiagrammer <file>"
import sys
import tkinter

def die(msg):
	print(msg)
	sys.exit()

def loadFile(filename):
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
					if line[i] == "\\":
						tmp += line[i+1]
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
			nodes.append({"name": tokens[1], "desc": tokens[2]})
		elif line.startswith("connection"):
			connections.append({"name": tokens[1], "desc": tokens[2]})
		else:
			die("Could not parse line: " + line)
	return nodes, connections

def saveFile(filename, nodes, connections):
	print("TODO")

def onClick(event):
	print(event)

def onKeyPress(event):
	print(event)

def main(filename):
	nodes, connections = loadFile(filename)

	window = tkinter.Tk()
	window.minsize(800, 600)
	window.maxsize(800, 600)
	window.bind("<Button-1>", onClick)
	window.bind("<Key>", onKeyPress)
	canvas = tkinter.Canvas(window, width=800, height=600)
	canvas.pack()
	window.mainloop()

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		die(usage)
