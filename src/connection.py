#!/usr/bin/python3

class Connection(Box):
	def __init__(self, dstid, x, y, text=""):
		super().__init__()
		self.__srcids = list()
		self.__dstid = dstid
		self.setX(x)
		self.setY(y)
		self.setText(text)

	def drop(self):
		self.update()

	def update(self):
		global nodes
		node = nodes[self.__dstid]

		nodeSize = node.getSize()
		connectionSize = self.getSize()
		xDiff = (self.getX() - node.getX())/nodeSize[0]
		yDiff = (self.getY() - node.getY())/nodeSize[1]

		if abs(xDiff) > abs(yDiff):
			if xDiff < 0:
				self.setX(node.getX() - nodeSize[0]/2 - connectionSize[0]/2)
				self.setY(min(node.getY() + nodeSize[1]/2 + connectionSize[1]/2, max(node.getY() - nodeSize[1]/2 - connectionSize[1]/2, self.getY())))
			else:
				self.setX(node.getX() + nodeSize[0]/2 + connectionSize[0]/2)
				self.setY(min(node.getY() + nodeSize[1]/2 + connectionSize[1]/2, max(node.getY() - nodeSize[1]/2 - connectionSize[1]/2, self.getY())))
		else:
			if yDiff < 0:
				self.setY(node.getY() - nodeSize[1]/2 - connectionSize[1]/2)
				self.setX(min(node.getX() + nodeSize[0]/2 + connectionSize[0]/2, max(node.getX() - nodeSize[0]/2 - connectionSize[0]/2, self.getX())))
			else:
				self.setY(node.getY() + nodeSize[1]/2 + connectionSize[1]/2)
				self.setX(min(node.getX() + nodeSize[0]/2 + connectionSize[0]/2, max(node.getX() - nodeSize[0]/2 - connectionSize[0]/2, self.getX())))

	def getDstId(self):
		return self.__dstid

	def getSrcIds(self):
		return self.__srcids.copy()

	def renderPaths(self):
		global canvas, nodes
		dstX, dstY = gameToScreenPos(self.getX(), self.getY())
		for srcId in self.getSrcIds():
			srcX, srcY = gameToScreenPos(nodes[srcId].getX(), nodes[srcId].getY())
			canvas.create_line(srcX, srcY, dstX, dstY)

	def getColor(self):
		return CONNECTIONCOLOR

	def click(self, x, y): pass

	def rightClick(self, x, y):
		global window, rightclickmenu
		rightclickmenu = tkinter.Menu(window, tearoff=0)
		rightclickmenu.add_command(label="Delete Connection", command=lambda: deleteConnection(self))
		rightclickmenu.add_command(label="Add Source", command=lambda: chooseAddSource(self))
		rightclickmenu.add_command(label="Remove Source", command=lambda: chooseRemoveSource(self))
		rightclickmenu.add_command(label="Edit", command=lambda: editConnection(self))
		rightclickmenu.post(x, y)

	def drag(self, x, y):
		self.setX(self.getX() + x)
		self.setY(self.getY() + y)

	def drop(self):
		self.update()

	def getType(self):
		return 'connection'

	def addSrc(self, src):
		global nodes
		self.__srcids.append(nodes.index(src))

	def removeSrc(self, src):
		global nodes
		self.__srcids.remove(nodes.index(src))
