#!/usr/bin/python3

def restart(filename=None):
	global openfilename, dragging, nodes, connections, focus, saved, redrawNeeded, redrawing
	status = {'type': 'none'}
	openfilename = filename
	dragging = False
	focus = (0, 0) # what coordinates are centered
	if openfilename != None:
		loadFile(openfilename)
	else:
		nodes = list()
		connections = list()
	setSaved(True)
	redrawNeeded = True
	redrawing = False

def main():
	global canvas, cursorX, cursorY, window, rightclickmenu, stdfont, codefont, editfont, status

	rightclickmenu = None
	status = {'type': 'none'}
	cursorX = 0
	cursorY = 0

	window = tkinter.Tk()
	stdfont = tkfont.Font(family=STDFONT[0], size=STDFONT[1])
	codefont = tkfont.Font(family=CODEFONT[0], size=CODEFONT[1])
	editfont = tkfont.Font(family=EDITFONT[0], size=EDITFONT[1])

	# menu
	menu = tkinter.Menu(window)
	window.config(menu=menu)
	filemenu = tkinter.Menu(menu)
	menu.add_cascade(label="File", menu=filemenu)
	filemenu.add_command(label="New", command=menu_new)
	filemenu.add_command(label="Open File", command=menu_openFile)
	filemenu.add_command(label="Save File", command=menu_saveFile)
	filemenu.add_command(label="Save File As", command=menu_saveFileAs)
	filemenu.add_command(label="Close", command=menu_close)

	window.bind("<Button-1>", onClick) # fully show node / edit mode
	window.bind("<Button-3>", onRightClick) # create node / connection
	window.bind("<ButtonRelease-1>", onRelease)
	window.bind("<ButtonRelease-3>", onRightRelease)
	window.bind("<B1-Motion>", onDrag) # move node
	window.bind("<B3-Motion>", onRightDrag) # move screen
	window.bind("<Motion>", updateMouse)

	window.bind("<Control-Return>", lambda e: handleKeyPress("Ctrl+Return"))
	window.bind("<Tab>", lambda e: handleKeyPress("Tab"))
	window.bind("<Left>", lambda e: handleKeyPress("Left"))
	window.bind("<Right>", lambda e: handleKeyPress("Right"))
	window.bind("<Escape>", lambda e: handleKeyPress("Escape"))
	window.bind("<BackSpace>", lambda e: handleKeyPress("RemoveLeft"))
	window.bind("<Delete>", lambda e: handleKeyPress("RemoveRight"))
	window.bind("<Return>", lambda e: handleKeyPress("Return"))
	window.bind("<Control-v>", lambda e: handleKeyPress("Paste"))
	window.bind("<Control-S>", lambda e: menu_saveFileAs())
	window.bind("<Control-s>", lambda e: menu_saveFile())
	window.bind("<Control-w>", lambda e: menu_close())
	window.bind("<Control-o>", lambda e: menu_openFile())
	window.bind("<Control-n>", lambda e: menu_new())
	window.bind("<Key>", onKeyPress)
	window.bind("<Configure>", lambda e: requestRender())

	canvas = tkinter.Canvas(window)
	canvas.pack(fill=BOTH, expand=YES)

	if len(sys.argv) == 1:
		restart()
	elif len(sys.argv) == 2:
		restart(sys.argv[1])
	else:
		die(usage)

	window.after(0, loop)
	window.mainloop()

def loop():
	global window, redrawNeeded, redrawing
	optRender()
	window.after(1, loop)
