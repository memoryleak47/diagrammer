#!/usr/bin/python3

indent = 0

def funcOn(msg):
	global indent
	print("\t"*indent + msg + " {")
	indent += 1

def func(msg):
	global indent
	print("\t"*indent + msg)

def funcOff(msg):
	global indent
	indent -= 1
	print("\t"*indent + "}")
