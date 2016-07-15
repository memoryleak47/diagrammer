#!/usr/bin/python3

usage="Usage:\tdiagrammer <file>"
import sys
import tkinter

def die(msg):
	print(msg)
	sys.exit()

def tokenize(line):
	line = line.strip()

	tokens = list()
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
	return tokens

def dia_open(filename):
	# if file exists
	f = open(filename)
	lines = f.readlines()
	f.close()

	nodes = list()
	connections = list()
	
	for line in lines:
		tokens = tokenize(line)
		if tokens[0] == "node":
			nodes.append({"name": tokens[1], "desc": tokens[2]})
		elif line.startswith("connection"):
			connections.append({"name": tokens[1], "desc": tokens[2]})
		else:
			die("Could not parse line: " + line)
	print(nodes)
	window = tkinter.Tk()

if len(sys.argv) == 2:
	dia_open(sys.argv[1])
else:
	die(usage)
