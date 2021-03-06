#!/usr/bin/python3

class Node(Box):
	def __init__(self, text, x, y, bodytext=""):
		super().__init__()
		self.__body = NodeBody(node=self, x=0, y=0, text=bodytext)
		self.setText(text)
		self.setX(x)
		self.setY(y)
		self.updateSize()

	def getColor(self):
		global status, nodes
		if status['type'].startswith('choose') and nodes.index(self) in status['nodeids']:
			return CHOOSEHEADCOLOR
		else:
			return HEADCOLOR

	def click(self, x, y):
		global status
		if nodeBodyVisible() and status['object'] == self.getNodeBody():
			resetStatus()
		else:
			statusOpen(self.getNodeBody())

	def rightClick(self, x, y):
		global window, rightclickmenu
		obj = getObjectAtMouse()
		rightclickmenu = tkinter.Menu(window, tearoff=0)
		rightclickmenu.add_command(label="Delete Node", command=lambda: deleteNode(obj))
		rightclickmenu.add_command(label="Edit", command=lambda: editNode(obj))
		rightclickmenu.add_command(label="Add Connection", command=lambda: createConnection(obj))
		rightclickmenu.post(x, y)

	def __updateConnections(self):
		global connections, nodes
		if self not in nodes:
			return

		for connection in connections:
			if connection.getDstId() == nodes.index(self):
				connection.update()

	def setSizeX(self, sx):
		super().setSizeX(sx)
		self.__updateConnections()

	def setSizeY(self, sy):
		super().setSizeY(sy)
		self.__updateConnections()

	def getNodeBody(self):
		return self.__body

	def getType(self):
		return 'node'

	def drag(self, x, y):
		self.setX(self.getX() + x)
		self.setY(self.getY() + y)

	def drop(self): pass
