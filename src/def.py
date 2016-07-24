#!/usr/bin/python3

#dicts

# node = {
#	'type': 'node',
#	'status': 'closed'/'open',
#	'x': 12,
#	'y': 12,
#	'head': 'str',
#	'body': 'str'
# }

# connection = {
# 	'type': 'connection',
#	'status': 'closed'/'open',
#	'x': 'int'
#	'y': 'int'
#	'body': 'str'
# }

# editdata = {
#	'text': 'str',
#	'object': node/nodebody/connection,
#	'type': 'node'/'nodebody'/'connection'
# }

# nodebody = {
#	'node': node
#	'type': 'nodebody'
# }

# choosedata = {
#	'type': 'none'/'remove'/'add'
#	'connection': None/connection
# }

#render

# The node(body)/connection-box has the size of textbox.getObjectSize() -> textsize + PADDINGstuff
# If edited: a white box is added with the size textsize + PADDINGstuff/2
