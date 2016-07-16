#!/usr/bin/python3

def checkDecision():
	global decision, decisionwindow
	if decision != None:
		decisionwindow.quit()
		decisionwindow.destroy()
		decisionwindow = None
	else:
		decisionwindow.after(20, checkDecision)

def decideNo():
	global decision
	decision = False

def decideYes():
	global decision
	decision = True

def reallyDiscardContent():
	global saved, decisionwindow, decision
	decision = None
	if not saved:
		decisionwindow = tkinter.Tk()
		decisionwindow.wm_title("Do you really want to discard your current changes?")
		label = tkinter.Label(decisionwindow, text="Pressing 'Yes' will discard your current changes")
		buttonYes = tkinter.Button(decisionwindow, text="Yes", command=decideYes)
		buttonNo = tkinter.Button(decisionwindow, text="Cancel", command=decideNo)
		label.pack()
		buttonYes.pack()
		buttonNo.pack()
		checkDecision()
		decisionwindow.mainloop()
		tmp = decision
		decision = None
		return tmp
	return True

def setSaved(b):
	global saved, window, openfilename
	saved = b
	title = "diagrammer - "
	if openfilename == None:
		title += "<Unsaved Document>"
	else:
		title += openfilename

	if not saved:
		title += " *"
	window.wm_title(title)
