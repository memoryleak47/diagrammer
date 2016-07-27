#!/usr/bin/python3

class Box:
	def __init__(self):
		self.__x = 0
		self.__y = 0
		self.__text = ""
		self.__sizeX = 0
		self.__sizeY = 0

	def getPadding(self):
		return PADDING, PADDING

	def __tokenize(self):
		global status
		if self.isEdited():
			text = status['text']
			tokens = list()

			# tokenize
			i = 0
			tmp = ""
			while i < len(text):
				if text[i] == "\n":
					if tmp != "":
						tokens.append({'type': 'normal', 'str': tmp})
						tmp = ""
					tokens.append({'type': 'newline', 'str': "\n"})
					i += 1
				else:
					tmp += text[i]
					i += 1
			if tmp != "":
				tokens.append({'type': 'normal', 'str': tmp})
			return tokens
		else:
			text = self.getText()
			tokens = list()

			# tokenize
			i = 0
			tmp = ""
			while i < len(text):
				if text[i] == "\n":
					if tmp != "":
						tokens.append({'type': 'normal', 'str': tmp})
						tmp = ""
					tokens.append({'type': 'newline', 'str': "\n"})
					i += 1
				elif text[i:i+2] == "\\\\":
					tmp += "\\"
					i += 2
				elif text[i:i+2] == "\\`":
					tmp += "`"
					i += 2
				elif text[i] == "`":
					tokens.append({'type': 'normal', 'str': tmp})
					tokens.append({'type': 'code', 'str': "`"})
					tmp = ""
					i += 1
				else:
					tmp += text[i]
					i += 1
			if tmp != "":
				tokens.append({'type': 'normal', 'str': tmp})
			return tokens

	def updateSize(self):
		global status
		tokens = self.__tokenize()

		if self.isEdited():
			x, y = 0, 0

			for token in tokens:
				if token['type'] == "newline":
					y += editfont.metrics()['linespace']
				elif token['type'] == "normal":
					x = max(x, editfont.measure(token['str']))
			y += editfont.metrics()['linespace']
		else:
			x, y = 0, 0

			tmpX = 0
			linespace = 0

			code = False
			for token in tokens:
				if token['type'] == "code":
					code = not code
				elif token['type'] == "newline":
					x = max(x, tmpX)
					tmpX = 0
					y += linespace
					linespace = 0
				elif token['type'] == "normal":
					if code:
						font = codefont
					else:
						font = stdfont
					tmpX += font.measure(token['str'])
					linespace = max(linespace, font.metrics()['linespace'])
			y += linespace
			x = max(x, tmpX)
		self.setSizeX(x + self.getPadding()[0]*2)
		self.setSizeY(y + self.getPadding()[1]*2)

	def setSizeX(self, sx):
		self.__sizeX = sx

	def setSizeY(self, sy):
		self.__sizeY = sy

	def getSizeX(self):
		return self.__sizeX

	def getSizeY(self):
		return self.__sizeY

	def render(self):
		global canvas
		tokens = self.__tokenize()
		padding = self.getPadding()
		size = self.getSizeX() - padding[0]*2, self.getSizeY() - padding[1]*2

		xArg, yArg = gameToScreenPos(self.getX() - size[0]/2, self.getY() - size[1]/2)

		canvas.create_rectangle(xArg - padding[0], yArg - padding[1], xArg + size[0] + padding[0], yArg + size[1] + padding[1], fill=self.getColor())

		x = xArg
		y = yArg

		if self.isEdited():
			canvas.create_rectangle(xArg - padding[0]/2, yArg - padding[1]/2, xArg + size[0] + padding[0]/2, yArg + size[1] + padding[1]/2, fill="white")
			cursor = status['cursor']

			for token in tokens:
				if token['type'] == 'newline':
					x = xArg
					y += editfont.metrics()['linespace']
					if cursor != -1:
						cursor -= 1
				else:
					canvas.create_text((x, y), text=token['str'], font=editfont, anchor="nw")
					x += editfont.measure(token['str'])
					if cursor != -1:
						if cursor <= len(token['str']):
							cx = x - editfont.measure(token['str'][cursor:])
							cy = y
							canvas.create_rectangle((cx, cy), cx+2, cy + editfont.metrics()['linespace'], fill="black")
							cursor = -1
						else:
							cursor -= len(token['str'])
			if cursor != -1:
				canvas.create_rectangle((x, y), x+2, y + editfont.metrics()['linespace'], fill="black")
		else:
			code = False
			linespace = 0

			for token in tokens:
				if token['type'] == 'code':
					code = not code
				elif token['type'] == 'newline':
					x = xArg
					y += linespace
				else:
					if code:
						font = codefont
					else:
						font = stdfont
					canvas.create_text((x, y), text=token['str'], font=font, anchor="nw")
					x += font.measure(token['str'])
					linespace = max(linespace, font.metrics()['linespace'])

	def isEdited(self):
		global status
		return (status['type'] == 'edit') and (status['object'] == self)

	def getX(self):
		return self.__x

	def getY(self):
		return self.__y

	def getText(self): # what is rendered (nothing if closed)
		return self.__text

	def getContent(self): # whats really in there
		return self.__text

	def setX(self, x):
		self.__x = x

	def setY(self, y):
		self.__y = y

	def setText(self, text):
		self.__text = text
		self.updateSize()

	# sub:
	#  getColor()
	#  click()
	#  rightClick()
	#  drag(to)
	#  drop()
	#  getType()
