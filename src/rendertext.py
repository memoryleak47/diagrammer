#!/usr/bin/python3

class TextBox:
	def __init__(self, text):
		global editfont

		self.tokens = list()

		# tokenize
		i = 0
		tmp = ""
		while i < len(text):
			if text[i] == "\n":
				self.tokens.append({'type': 'normal', 'str': tmp})
				tmp = ""
				self.tokens.append({'type': 'newline', 'str': "\n"})
				i += 1
			elif text[i:i+2] == "\\\\":
				tmp += "\\"
				i += 2
			elif text[i:i+2] == "\\`":
				tmp += "`"
				i += 2
			elif text[i] == "`":
				self.tokens.append({'type': 'normal', 'str': tmp})
				self.tokens.append({'type': 'code', 'str': "`"})
				tmp = ""
				i += 1
			else:
				tmp += text[i]
				i += 1
		if tmp != "":
			self.tokens.append({'type': 'normal', 'str': tmp})

		# size calculation
		x, y = 0, 0

		tmpX = 0
		linespace = 0

		code = False
		for token in self.tokens:
			if token['type'] == "code":
				code = not code
			elif token['type'] == "newline":
				x = max(x, tmpX)
				tmpX = 0
				y += linespace
				linespace = 0
			elif token['type'] == "normal":
				font = self.__getFont(code)
				tmpX += font.measure(token['str'])
				linespace = max(linespace, font.metrics()['linespace'])
		y += linespace
		x = max(x, tmpX)
		self.size = (x, y)

	def __getFont(self, code):
		global stdfont, codefont
		if code:
			return codefont
		else:
			return stdfont

	def getSize(self): # textsize
		return self.size

	def getObjectSize(self): # textsize + padding
		return (self.size[0] + 2*PADDING, self.size[1] + 2*PADDING)

	def render(self, xArg, yArg):
		global canvas
		
		xArg -= self.size[0]/2
		yArg -= self.size[1]/2

		x = xArg
		y = yArg
		code = False
		linespace = 0

		for token in self.tokens:
			if token['type'] == 'code':
				code = not code
			elif token['type'] == 'newline':
				x = xArg
				y += linespace
			else:
				font = self.__getFont(code)
				canvas.create_text((x, y), text=token['str'], font=font, anchor="nw")
				x += font.measure(token['str'])
				linespace = max(linespace, font.metrics()['linespace'])

class EditTextBox:
	def __init__(self, text):
		global editfont

		self.tokens = list()

		# tokenize
		i = 0
		tmp = ""
		while i < len(text):
			if text[i] == "\n":
				self.tokens.append({'type': 'normal', 'str': tmp})
				tmp = ""
				self.tokens.append({'type': 'newline', 'str': "\n"})
				i += 1
			else:
				tmp += text[i]
				i += 1
		if tmp != "":
			self.tokens.append({'type': 'normal', 'str': tmp})

		# size calculation
		x, y = 0, 0

		tmpX = 0

		for token in self.tokens:
			if token['type'] == "newline":
				x = max(x, tmpX)
				tmpX = 0
				y += editfont.metrics()['linespace']
				linespace = 0
			elif token['type'] == "normal":
				tmpX += editfont.measure(token['str'])
		y += editfont.metrics()['linespace']
		x = max(x, tmpX)
		self.size = (x, y)

	def getSize(self): # textsize
		return self.size

	def getObjectSize(self): # textsize + padding
		return (self.size[0] + 2*PADDING, self.size[1] + 2*PADDING)

	def render(self, xArg, yArg):
		global canvas, editfont, editdata
		
		xArg -= self.size[0]/2
		yArg -= self.size[1]/2

		x = xArg
		y = yArg
		cursor = editdata['cursor']

		for token in self.tokens:
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
