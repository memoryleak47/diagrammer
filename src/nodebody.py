#!/usr/bin/python3

class NodeBody(Box):
	def __init__(self, node, x, y, text=""):
		super().__init__()
		self.__node = node
		self.setText(text)
		self.setX(x)
		self.setY(y)

	def getType(self):
		return 'nodebody'

	def getColor(self):
		return BODYCOLOR

	def getX(self):
		return self.__node.getX()

	def getY(self):
		return self.__node.getY() + self.__node.getSize()[1]/2 + self.getSize()[1]/2

	def click(self, x, y): pass

	def rightClick(self, x, y):
		global window, rightclickmenu
		rightclickmenu = tkinter.Menu(window, tearoff=0)
		rightclickmenu.add_command(label="Edit", command=lambda: editNodeBody(self))
		rightclickmenu.post(x, y)

	def drag(self, x, y): pass
	def drop(self): pass