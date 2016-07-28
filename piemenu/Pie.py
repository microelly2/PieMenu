# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- piemenu helper functions -
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import FreeCAD
import FreeCADGui

App=FreeCAD
Gui=FreeCADGui

import PySide
from PySide import QtCore, QtGui


import piemenu.context
reload(piemenu.context)




class PieAction(QtGui.QAction):


	def __init__(self,icon,piecename,toolbar):

		super(self.__class__, self).__init__(icon,piecename,toolbar)
		self.setObjectName(piecename)
		self.Task=None
		self.task=None
		self.activated.connect(self.run)


	def run(self):

		if self.task.norun(): return

		if self.task.init():
			ef=EventFilter(self.task)
			FreeCAD.eventfilter=ef
			QtGui.qApp.installEventFilter(ef)
			Gui.ActiveDocument.activeView().stopAnimating()


	def onEnter(self):

#		print "this is onEnter"
		if self.Task <> None:
			try:
				print self.Task
				self.task=self.Task(self)
				self.task.init()
			except:
				sayexc()


	def onLeave(self):

#		print "this is onleave"
		if self.task<>None:
			self.task.kill()




class PieTask(object):

	def __init__(self,action=None):
		self.action=action

	def norun(self):
		return False

	def init(self):
		print "init task ..."
		return True

	def kill(self):
		print "cleanup and kill task finished."

	def start(self):
		print "start"

	def mouseAt(self,x,y):
		print ("process mouse position at ",x,y)

	def stop(self,state):
		print "stop state:" ,state




class PieSingleTask(PieTask):


	def norun(self):
		return True

	def init(self):
		self.runpre()
		return False

	def run(self):
		print "Pie single task - run's one time"

	def onLeave(self):
		print "this is onleave"


class dummyTask(PieSingleTask):

	def runpre(self):
		s=' '.join([str(self.action),'\n', str(self.action.text()),':\n',str(self.action.toolTip())])
		FreeCAD.Console.PrintWarning("\n" +s +"\n\n"+ "NOT yet implemented!\n")
		print s


class Pie(object):


	def __init__(self,pieName,pieces=[]):


		if pieName=='': pieName='No Selection'
		number=piemenu.context.getSigIndex(pieName)
		self.pieName=pieName
#		mw = Gui.getMainWindow()
#		self.tb=QtGui.QToolBar(mw)


		mw=FreeCAD.Gui.getMainWindow()
		mw.toolbar = mw.addToolBar(pieName)
		mw.toolbar.setWindowTitle(pieName)

		# mw.toolbar.show()
		self.tb=mw.toolbar


		paramGet = App.ParamGet("User parameter:BaseApp/PieMenu")
		paramIndexGet = App.ParamGet("User parameter:BaseApp/PieMenu/Index")
		indexList = paramIndexGet.GetString("IndexList")

		paramIndexGet.SetString(str(number), self.pieName)

		index=indexList.split('.,.')

		if str(number) not in index:
			paramIndexGet.SetString("IndexList", indexList + ".,."+str(number))
		paramGet.SetString("CurrentPie",self.pieName)

		group = paramIndexGet.GetGroup(str(number))
		t2=""

		if len(pieces)>0:
			for p in pieces:
				if len(p) == 4:
					[pieceName,iconpath,tooltip,taskClass]=p
					shortcut=''
				elif len(p) == 5:
					[pieceName,iconpath,tooltip,taskClass,shortcut]=p
				else:
					pieceName=p[0]

				for i in mw.findChildren(QtGui.QAction):
					found = False
					if i.objectName()==pieceName:
						found = True
						action = i
						break
				if not found:
					action =  PieAction(QtGui.QIcon( iconpath), pieceName, self.tb)
					if shortcut <>'':
						action.setShortcut(shortcut)
						sk=action.shortcut().toString()
						action.setToolTip(tooltip + "("+sk+")")
					else:
						action.setToolTip(tooltip)
					action.Task=taskClass

				self.tb.addAction(action)

				if t2=='': t2 = pieceName
				else: t2 += ".,." + pieceName

		else: # the dummy case
			pieceName="MyPiece2"

			for i in mw.findChildren(QtGui.QAction):
				found = False
				if i.objectName()==pieceName:
					found = True
					action = i
					break
			if not found:
				action =  PieAction(QtGui.QIcon("icons:freecad.svg"), pieceName, self.tb)

			action.setToolTip("I'm the My Piece Action XXX")
			action.Task=PieTask

			action.setObjectName(pieceName)
			self.tb.addAction(action)

			t2 +=".,." + pieceName

		group.SetString("ToolList", t2)


class  PieToggleTask(PieSingleTask):

	def run(self):
		pass

	def kill(self):
		self.runpre()



#-----------------------------------------------------------------------------------------


class EventFilter(QtCore.QObject):

	def __init__(self,task):
		QtCore.QObject.__init__(self)
		self.enterleave=False
		self.enterleave=True
		self.x=0
		self.y=0
		self.task=task
		self.task.start()

	def eventFilter(self, o, e):

		if e.type() == PySide.QtCore.QEvent.Type.KeyPress:
			if e.key()== QtCore.Qt.Key_F3  or e.key()== QtCore.Qt.Key_Escape or e.key()== QtCore.Qt.Key_Plus or e.key()== QtCore.Qt.Key_Minus :
				say("----Commit:F3 or Plus, Cancel:  ESC or Minus---")
				state = e.key()<> QtCore.Qt.Key_Escape and e.key() <> QtCore.Qt.Key_Minus
				QtGui.qApp.removeEventFilter(FreeCAD.eventfilter)
				say("Eventfilter stopped.")
				self.task.stop(state)
				self.task.kill()

		if e.type() == QtCore.QEvent.MouseMove:
			pos = e.pos()
			x=pos.x()
			y=pos.y()
			if self.x<>x or self.y<>y:
				self.task.mouseAt(x,y)
				self.x=x
				self.y=y

		return QtGui.QWidget.eventFilter(self, o, e)


#---------------------------------------------------------


