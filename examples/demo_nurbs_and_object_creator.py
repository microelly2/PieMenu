# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- create personal piemenu collection -
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

from piemenu.Pie import Pie, PieTask, PieSingleTask, PieToggleTask, dummyTask

#
# user defs
#

#idir=FreeCAD.ConfigGet('UserAppData')+"/Mod/reconstruction/icons/"
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


class toggleNurbsGrid(PieToggleTask):

	def runpre(self):
		obj=App.ActiveDocument.getObjectsByLabel("Nurbs Grid")[0]
		obj.ViewObject.Visibility = not obj.ViewObject.Visibility
		if obj.ViewObject.Visibility:
			self.action.setIcon(QtGui.QIcon(idir+"eye.svg"))
		else:
			self.action.setIcon(QtGui.QIcon(idir+"eye_closed.svg"))



class togglePoleGrid(PieToggleTask):

	def runpre(self):
		obj=App.ActiveDocument.getObjectsByLabel("Pole Grid")[0]
		obj.ViewObject.Visibility = not obj.ViewObject.Visibility
		if obj.ViewObject.Visibility:
			self.action.setIcon(QtGui.QIcon(idir+"eyepoles.svg"))
		else:
			self.action.setIcon(QtGui.QIcon(idir+"eyepoles_closed.svg"))



class toggleNurbs(PieToggleTask):

	def runpre(self):
		obj=App.ActiveDocument.getObjectsByLabel("Nurbs")[0]
		obj.ViewObject.Visibility = not obj.ViewObject.Visibility
		if obj.ViewObject.Visibility:
			self.action.setIcon(QtGui.QIcon(idir+"eyenurbs.svg"))
		else:
			self.action.setIcon(QtGui.QIcon(idir+"eyenurbs_closed.svg"))



# icons http://www.freecadweb.org/wiki/index.php?title=Artwork
#-----------------------------------------------------------	

#
# test pie menu
#

Pie('XYZ#:',[
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


Pie('PartWorkbench#*:Edge',[
		['_My_add_Edge', idir+"add_edge.svg",'add edge',dummyTask],
		['_My_delete_Edge', idir+"delete_edge.svg",'delete selected edge',dummyTask],
		['_My_move_Edge', idir+"move_edge.svg",'move the edge',dummyTask],
		['_My_elevate_Edge', idir+"elevate_edge.svg",'elevate the edge',dummyTask],

		['_My_show_curvature', idir+"curvature.svg",'show curvature and torsion',dummyTask],
		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
	])

pie=Pie('*#*:Edge,Edge',[
		['_My_move_Edges', idir+"move_edge.svg",'move both edges',dummyTask],
		['_My_elevate_Edges', idir+"elevate_edges.svg",'change height of both edges',dummyTask],
		['_My_press_Edges', idir+"press_edges.svg",'reduce distance between both edges',dummyTask],
		['_My_wide_Edges', idir+"wide_edges.svg",'increase distance between both edges',dummyTask],

		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
	])


Pie('*#*:Edge,Edge,Edge',[
		['_My_move_inner_Edge', idir+"move_inner_edge.svg",'move the inner segement',dummyTask],
		['_My_elevate_inner_Edge', idir+"elevate_inner_edge.svg",'elevate the inner segment',dummyTask],
		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
	])


Pie('*#*:Edge,Edge,Edge,Edge',[
		['_My_move_Rectangle', idir+"move_rectangle.svg",'move the complete rectangle',dummyTask],
		['_My_elevate_Rectangle', idir+"elevate_rectangle.svg",'elevate the complete rectangle',dummyTask],
		['_My_smooth_Rectangle', idir+"smooth_rectangle.svg",'smooth or sharp the edges of the  rectangle',dummyTask],
		['_My_circle_Rectangle', idir+"circle_rectangle.svg",'rectangle to square',dummyTask],

		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
	])

