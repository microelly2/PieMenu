
from say import *

import FreeCAD
import FreeCADGui

App=FreeCAD
Gui=FreeCADGui

import PySide
from PySide import QtCore, QtGui


import context
reload(context)

def getPieSignatures():
	paramIndexGet = App.ParamGet("User parameter:BaseApp/PieMenu/Index")
	indexList = paramIndexGet.GetString("IndexList")
#	print indexList
	index=indexList.split('.,.')
	sigs=[paramIndexGet.GetString(ix) for ix in index]
	return sigs

def getSigIndex(sig):
	paramIndexGet = App.ParamGet("User parameter:BaseApp/PieMenu/Index")
	indexList = paramIndexGet.GetString("IndexList")
	print indexList
	index=indexList.split('.,.')
	
	for ix in index:
		if sig == paramIndexGet.GetString(ix) : return ix
	ixint=[int(ix) for ix in index]
	newix=str(max(ixint)+1)
	print "new idex created", newix
	return newix 


def activatePieMenu(sig):

		paramGet = App.ParamGet("User parameter:BaseApp/PieMenu")
		if sig in getPieSignatures():
			paramGet.SetString("CurrentPie",sig)
		else:
			print "signature >" + sig + "< not found --> Default Pie Menu"
			paramGet.SetString("CurrentPie",'Default')



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

		print "this is onEnter"
		if self.Task <> None:
			try:
				print self.Task
				self.task=self.Task(self)
				self.task.init()
			except:
				sayexc()


	def onLeave(self):

		print "this is onleave"
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
		print "... cleanup and kill task finished."

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
		s=' '.join([str(self.action),'\n', str(self.action.text()),':',str(self.action.toolTip())])
		FreeCAD.Console.PrintWarning("\n" +s +"\n\n"+ "NOT yet implemented!\n")
		print s


class Pie(object):


	def __init__(self,pieName,pieces=[]):


		if pieName=='': pieName='No Selection'
		number=getSigIndex(pieName)
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

		print indexList
		index=indexList.split('.,.')
		print index

		if str(number) not in index:
			paramIndexGet.SetString("IndexList", indexList + ".,."+str(number))
		paramGet.SetString("CurrentPie",self.pieName)

		group = paramIndexGet.GetGroup(str(number))
		t2=""

		if len(pieces)>0:
			for p in pieces:
				if len(p) == 4:
					[pieceName,iconpath,tooltip,taskClass]=p
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



#
# user defs
#

idir=FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"
idir=FreeCAD.ConfigGet('UserAppData')+"/Mod/PieMenu/icons/"

class mySingleTask(PieSingleTask):

	def run(self):
		print "My single task runs"


class myTorusTask(PieTask):
	''' task to create a torus and move it around, can be killed ''' 

	def __init__(self,action,name='My Task'):
		super(self.__class__, self).__init__(action)
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




def mess(m):
	FreeCAD.m=QtGui.QLabel("----------------------\n" + m +"\n----------------------")
	FreeCAD.m.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	FreeCAD.m.show()


class  PieToggleTask(PieSingleTask):

	def run(self):
		pass

	def kill(self):
		self.runpre()


class toggleNurbsGrid(PieToggleTask):

	def runpre(self):
		obj=App.ActiveDocument.getObjectsByLabel("Nurbs Grid")[0]
		obj.ViewObject.Visibility = not obj.ViewObject.Visibility
		if obj.ViewObject.Visibility:
			self.action.setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eye.svg"))
		else:
			self.action.setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eye_closed.svg"))



class togglePoleGrid(PieToggleTask):

	def runpre(self):
		obj=App.ActiveDocument.getObjectsByLabel("Pole Grid")[0]
		obj.ViewObject.Visibility = not obj.ViewObject.Visibility
		if obj.ViewObject.Visibility:
			self.action.setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyepoles.svg"))
		else:
			self.action.setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyepoles_closed.svg"))



class toggleNurbs(PieToggleTask):

	def runpre(self):
		obj=App.ActiveDocument.getObjectsByLabel("Nurbs")[0]
		obj.ViewObject.Visibility = not obj.ViewObject.Visibility
		if obj.ViewObject.Visibility:
			self.action.setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyenurbs.svg"))
		else:
			self.action.setIcon(QtGui.QIcon(FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"+"eyenurbs_closed.svg"))


#---------------------------

if 0:
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")


	try: App.ActiveDocument.Sphere
	except: App.ActiveDocument.addObject("Part::Sphere","Sphere")

	App.ActiveDocument.recompute()



# icons http://www.freecadweb.org/wiki/index.php?title=Artwork
#-----------------------------------------------------------	

#
# test pie menu
#

Pie('',[
		# a action to create and move a part
		['_My_torus',"icons:freecad.svg",'demo add and move torus',myTorusTask],
		# syntax of :
		# [ 'action name', 'icon', 'tooltipp', classForBehaviour]

		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
		['_My_nurbs_poles', idir+"eyepoles.svg",'toggle Pole Grid Vsisibility ',togglePoleGrid],

		# some predefined actions
		['Std_ViewFront'],
		['Std_ViewTop'],
		['Std_ViewFitSelection'],

		['Part_Torus']
	])


Pie('Feature:Edge',[
		['_My_add_Edge', idir+"add_edge.svg",'add edge',dummyTask],
		['_My_delete_Edge', idir+"delete_edge.svg",'delete selected edge',dummyTask],
		['_My_move_Edge', idir+"move_edge.svg",'move the edge',dummyTask],
		['_My_elevate_Edge', idir+"elevate_edge.svg",'elevate the edge',dummyTask],

		['_My_show_curvature', idir+"curvature.svg",'show curvature and torsion',dummyTask],
		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
		['Std_ViewTop'],
	])

pie=Pie('Feature:Edge,Edge',[
		['_My_move_Edges', idir+"move_edge.svg",'move both edges',dummyTask],
		['_My_elevate_Edges', idir+"elevate_edges.svg",'change height of both edges',dummyTask],
		['_My_press_Edges', idir+"press_edges.svg",'reduce distance between both edges',dummyTask],
		['_My_wide_Edges', idir+"wide_edges.svg",'increase distance between both edges',dummyTask],

		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
		['Std_ViewTop'],
	])


Pie('Feature:Edge,Edge,Edge',[
		['_My_move_inner_Edge', idir+"move_inner_edge.svg",'move the inner segement',dummyTask],
		['_My_elevate_inner_Edge', idir+"elevate_inner_edge.svg",'elevate the inner segment',dummyTask],
		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],

		['Std_ViewTop'],
		['Std_ViewFront'],
	])


Pie('Feature:Edge,Edge,Edge,Edge',[
		['_My_move_Rectangle', idir+"move_rectangle.svg",'move the complete rectangle',dummyTask],
		['_My_elevate_Rectangle', idir+"elevate_rectangle.svg",'elevate the complete rectangle',dummyTask],
		['_My_smooth_Rectangle', idir+"smooth_rectangle.svg",'smooth or sharp the edges of the  rectangle',dummyTask],
		['_My_circle_Rectangle', idir+"circle_rectangle.svg",'rectangle to square',dummyTask],

		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
		['Std_ViewTop'],
		['Std_ViewFront'],
	])


