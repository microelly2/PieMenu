
from say import *


import FreeCAD
import FreeCADGui

App=FreeCAD
Gui=FreeCADGui

import PySide
from PySide import QtCore, QtGui


class Pie(object):

	def __init__(self,pieName,number,pieces=[]):

		self.pieName=pieName
		mw = Gui.getMainWindow()
		self.tb=QtGui.QToolBar(mw)

		paramGet = App.ParamGet("User parameter:BaseApp/PieMenu")
		paramIndexGet = App.ParamGet("User parameter:BaseApp/PieMenu/Index")
		indexList = paramIndexGet.GetString("IndexList")

		paramIndexGet.SetString(str(number), self.pieName)
		paramIndexGet.SetString("IndexList", "0.,."+str(number))
		paramGet.SetString("CurrentPie",self.pieName)

		group = paramIndexGet.GetGroup(str(number))
		t2=""

		if len(pieces)>0:
			for p in pieces:
				[pieceName,iconpath,tooltip,hovermethod,clickmethod]=p

				for i in mw.findChildren(QtGui.QAction):
					found = False
					if i.objectName()==pieceName:
						found = True
						action = i
						break
				if not found:
					action =  QtGui.QAction(QtGui.QIcon( iconpath), pieceName, self.tb)

				action.setToolTip(tooltip)
				action.activated.connect(clickmethod)
				action.hovered.connect(hovermethod)
				action.setObjectName(pieceName)

				self.tb.addAction(action)
				t2 +=".,." + pieceName
				if pieceName=='test5':
					FreeCAD.a=action

		else: # the dummy case
			pieceName="MyPiece2"

			for i in mw.findChildren(QtGui.QAction):
				found = False
				if i.objectName()==pieceName:
					found = True
					action = i
					break
			if not found:
				action =  QtGui.QAction(QtGui.QIcon("icons:freecad.svg"), pieceName, self.tb)

			myActionh = lambda: FreeCAD.Console.PrintWarning("This is my Hover Method\n")
			myActiona =lambda:FreeCAD.Console.PrintError("This is my Click  Method\n")

			action.setToolTip("I'm the My Piece Action")
			action.activated.connect(myActiona)
			action.hovered.connect(myActionh)
			action.setObjectName(pieceName)

			self.tb.addAction(action)

			t2 +=".,." + pieceName

		group.SetString("ToolList", t2)


# some dummy functions 
myActionh = lambda: FreeCAD.Console.PrintMessage("This is my Hover Method\n")
myActiona =lambda:FreeCAD.Console.PrintMessage("This is my Click  Method\n")

myActionh2 = lambda: FreeCAD.Console.PrintWarning("This is my Hover Method\n")
myActiona2 =lambda:FreeCAD.Console.PrintError("This is my Click  Method\n")


idir=FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"

# dummy case
# pie2=Pie("meineTorteABC5",15,[])


# functions for  the nurbs scene


def mess(m):
	nomess()
	FreeCAD.m=QtGui.QLabel("----------------------\n" + m +"\n----------------------")
	FreeCAD.m.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	FreeCAD.m.show()

def nomess():
	try: FreeCAD.m.hide()
	except: pass

def preNurbsGrid():
	mess("hide/unhide \n\nnurbs grid")

def preNurbs():
	mess("hide/unhide \n\nnurbs")

def prePoleGrid():
	mess("hide/unhide \n\npole grid")




def toggleNurbsGrid():
	nomess()
	obj=App.ActiveDocument.getObjectsByLabel("Nurbs Grid")[0]
	obj.ViewObject.Visibility = not obj.ViewObject.Visibility
	mw = Gui.getMainWindow()
	a=mw.findChildren(QtGui.QAction,"test6")
	if not obj.ViewObject.Visibility:
		a[0].setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eye.svg"))
	else:
		a[0].setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eye_closed.svg"))

def togglePoleGrid():
	nomess()
	obj=App.ActiveDocument.getObjectsByLabel("Pole Grid")[0]
	obj.ViewObject.Visibility = not obj.ViewObject.Visibility
	mw = Gui.getMainWindow()
	a=mw.findChildren(QtGui.QAction,"test8")
	if not obj.ViewObject.Visibility:
		a[0].setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyepoles.svg"))
	else:
		a[0].setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyepoles_closed.svg"))


def toggleNurbs():
	nomess()
	print "Nurbs visibility"
	obj=App.ActiveDocument.getObjectsByLabel("Nurbs")[0]
	obj.ViewObject.Visibility = not obj.ViewObject.Visibility
	mw = Gui.getMainWindow()
	a=mw.findChildren(QtGui.QAction,"test7")
	if not obj.ViewObject.Visibility:
		a[0].setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyenurbs.svg"))
	else:
		a[0].setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyenurbs_closed.svg"))

#---------------------------

def showmouse(x,y):
	say(["Mouse is at",x,y])

class EventFilter(QtCore.QObject):

	def __init__(self):
		QtCore.QObject.__init__(self)
		self.mouseWheel=0
		self.enterleave=False
		self.enterleave=True
		self.x=0
		self.y=0

	def eventFilter(self, o, e):
		global lastEvent

		global keyPressed2
		global editmode

		global lasttime
		global lastkey

		# http://doc.qt.io/qt-5/qevent.html
		z=str(e.type())

		event=e


		try:

			if z == 'PySide.QtCore.QEvent.Type.KeyPress':
				if e.key()== QtCore.Qt.Key_F3  or e.key()== QtCore.Qt.Key_Escape or e.key()== QtCore.Qt.Key_Plus or e.key()== QtCore.Qt.Key_Minus :
					say("----Commit:---F3 or Plus, Cancel:  ESC or Minus---")
					state = e.key()<> QtCore.Qt.Key_Escape and e.key() <> QtCore.Qt.Key_Minus
					self.task.stop(state)
					stopEf()
					say("Eventfilter stopped ------------")


			if event.type() == QtCore.QEvent.MouseMove:
				if event.buttons() == QtCore.Qt.NoButton:
					pos = event.pos()
					x=pos.x()
					y=pos.y()
					if self.x<>x or self.y<>y:
						# showmouse(x,y)
						self.task.mouseAt(x,y)
						self.x=x
						self.y=y

				# wheel rotation

			if event.type()== QtCore.QEvent.Type.Wheel:
				# http://doc.qt.io/qt-4.8/qwheelevent.html
				#FreeCAD.Console.PrintMessage(str(event.type())+ " " + str(o) +'!!\n')
				FreeCAD.Console.PrintMessage("delta wheel: " + str(e.delta()) + " pos: " +str(e.pos()) + "\n")
				
				self.mouseWheel += e.delta()/120
				FreeCAD.Console.PrintMessage("wheel: " + str(self.mouseWheel) +"\n")
				self.modedat[self.mode]=self.mouseWheel
				
				# self.update()
				


				
				if noDefaultWheel:
					return True 
				else:
					return False

			# mouse clicks
			if event.type() == QtCore.QEvent.MouseButtonPress or \
					event.type() == QtCore.QEvent.MouseButtonRelease or\
					event.type() == QtCore.QEvent.MouseButtonDblClick:

	#				FreeCAD.Console.PrintMessage(str(event.type())+ " " + str(o) +'!!\n')
				pos=e.pos()
				x=pos.x()
				y=pos.y()
				
				
				pw=o.parentWidget()
				try:name=pw.objectName()
				except: name=''
				if name=='': 
					try: name=o.objectName()
					except: pass
				if 0:
					FreeCAD.Console.PrintMessage( " mouse position: xy"  +str(x) +"\n")
					FreeCAD.Console.PrintMessage( " mouse position: " +str(e.pos()) + "\n")
					FreeCAD.Console.PrintMessage( " widget height: " +str(o.height()) + "\n")
					FreeCAD.Console.PrintMessage( " widget width: " +str(o.width()) + "\n")
					FreeCAD.Console.PrintMessage( " widget position: " +str(o.pos()) + "\n")
					#FreeCAD.Console.PrintMessage( " parent widget: " +str(o.parentWidget()) + "\n")
				
				if name<>'':
					FreeCAD.Console.PrintMessage( " parent widget: " +name + "\n")
				widget = QtGui.qApp.widgetAt(e.pos())
	#				if widget:
	#					FreeCAD.Console.PrintMessage("widget under mouse: " + str(widget) +" !--"+widget.objectName() +"--!\n")
				
				# double clicked
				if event.type() == QtCore.QEvent.MouseButtonDblClick and event.button() == QtCore.Qt.MidButton :
					FreeCAD.Console.PrintMessage('two\n')

				# middle
				if event.button() == QtCore.Qt.MidButton or  event.button() == QtCore.Qt.MiddleButton:
					FreeCAD.Console.PrintMessage('!-------------------------------------!!  X middle \n')
					
					# wenn nicht navigation aktiv sein soll, sonst return False
					return True
					
					# return QtGui.QWidget.eventFilter(self, o, e)

				if event.button() == QtCore.Qt.LeftButton:
	#					FreeCAD.Console.PrintMessage('!! X one left\n')
					pass

				# right mouse button when context menue deactivated
				elif event.button() == QtCore.Qt.RightButton:
					FreeCAD.Console.PrintMessage('!! X one right\n')

		except:
			sayexc()

		return QtGui.QWidget.eventFilter(self, o, e)

#--------------------------

class myTask():

	def __init__(self,name='My Task'):
		self.name=name
		self.sx=None
		self.sy=None
		self.x=None
		self.y=None
		self.obj=None

	def start(self):
		print ("start Task" + self.name)
		if self.obj<>None:
			self.obj.ViewObject.show()
		else:
			self.obj=App.ActiveDocument.addObject("Part::Box",self.name)

	def mouseAt(self,x,y):
		if self.sx==None: self.sx=x
		if self.sy==None: self.sy=y
		self.x=x
		self.y=y
		print (self.obj.Label," started at:",self.sx,self.sy," is now here ",self.x,self.y)
		self.obj.Placement.Base.x=x-self.sx
		self.obj.Placement.Base.y=self.sy-y
		App.ActiveDocument.recompute()


	def stop(self,state):
		try:
			print ("stop Task" + self.name)
			print ("my way was from ",self.sx,self.sy," to ",self.x,self.y)
			if state:
				print "commit action"
				obj=App.ActiveDocument.addObject("Part::Torus","Result "+ self.name)
				obj.Placement=FreeCAD.Placement(self.obj.Placement)
				#App.ActiveDocument.removeObject(self.obj.Name)
				self.obj.ViewObject.hide()
				import random
				obj.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
			else:
				print "********* cancel action   ****"
			App.ActiveDocument.recompute()
			App.ActiveDocument.removeObject(self.obj.Name)
		except: sayexc()

def run():
	task=myTask("Otto")
	FreeCAD.task=task
	mw=QtGui.qApp
	ef=EventFilter()
	ef.task=task
	task.start()
	ef.mouseWheel=0
	ef.modedat={}
	FreeCAD.eventfilter=ef
	mw.installEventFilter(ef)
	Gui.ActiveDocument.activeView().stopAnimating()
	print "started "


#---------------------------



'''
def startEf():
	mw=QtGui.qApp
	ef=EventFilter()
	ef.mouseWheel=0
	ef.modedat={}
	FreeCAD.eventfilter=ef
	mw.installEventFilter(ef)
	Gui.ActiveDocument.activeView().stopAnimating()
	print "started "
'''

def stopEf():
	ef=FreeCAD.eventfilter
	mw=QtGui.qApp
	mw.removeEventFilter(ef)
	print "call stopEf"

App.newDocument("Unnamed")
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")

try: App.ActiveDocument.Sphere
except: App.ActiveDocument.addObject("Part::Sphere","Sphere")
App.ActiveDocument.recompute()


pie=Pie("meineTorteABC5",15,[
		['test0', idir+"addvline.svg",'Add V-Line to Polegrid',myActiona,myActionh],
		['test1', idir+"adduline.svg",'add U-Line to the Polegrid',myActiona,myActionh],
#		['test2', idir+"height.svg",'change Height of the selected pole',nomess,run],
		['test3', idir+"addout.svg",'increase distance of pole lines',nomess,myActionh],
#		['test4', idir+"addin.svg",'increase distance of pole lines',myActiona,myActionh],

		['test5', "icons:freecad.svg",'demo add and move torus',nomess,run],
#		['test5', "icons:freecad.svg",'increase distance of pole lines',startEf,stopEf],

		['test6', idir+"eye_closed.svg",'toggle Nurbs grid',preNurbsGrid,toggleNurbsGrid],
		['test7', idir+"eyenurbs_closed.svg",'toggle Nurbs Visibility',preNurbs,toggleNurbs],
		['test8', idir+"eyepoles_closed.svg",'toggle Pole Grid Vsisibility ',prePoleGrid,togglePoleGrid],
		
	])






