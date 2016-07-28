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


#----------
# some test data ...
try: App.closeDocument("Unnamed")
except: pass

App.newDocument("Unnamed")
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")
App.ActiveDocument.addObject("Part::Box","Box")
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")

try:
	import Animation
	Animation.createRotator()
	Animation.createMover()
	Animation.createManager()
	Gui.activateWorkbench("AnimationWorkbench")
	Gui.activateWorkbench("PartWorkbench")
except:
	pass

App.activeDocument().recompute()
Gui.SendMsgToActiveView("ViewFit")

#------------

idir=FreeCAD.ConfigGet('UserAppData')+"/Mod/PieMenu/icons/"


'''
Pie('PartWorkbench#PartDesign.Pad:Edge',[
		['_My_add_Edge', idir+"add_edge.svg",'add edge',dummyTask],
		['_My_delete_Edge', idir+"delete_edge.svg",'delete selected edge',dummyTask],
		['_My_move_Edge', idir+"move_edge.svg",'move the edge',dummyTask],
		['_My_elevate_Edge', idir+"elevate_edge.svg",'elevate the edge',dummyTask],

		['_My_show_curvature', idir+"curvature.svg",'show curvature and torsion',dummyTask],
		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
		['Std_ViewTop'],
	])

pie=Pie('*#PartDesign.Pad:Edge,Edge',[
		['_My_move_Edges', idir+"move_edge.svg",'move both edges',dummyTask],
		['_My_elevate_Edges', idir+"elevate_edges.svg",'change height of both edges',dummyTask],
		['_My_press_Edges', idir+"press_edges.svg",'reduce distance between both edges',dummyTask],
		['_My_wide_Edges', idir+"wide_edges.svg",'increase distance between both edges',dummyTask],

		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],
		['Std_ViewTop'],
	])


Pie('*#*:Edge,Edge,Edge',[
		['_My_move_inner_Edge', idir+"move_inner_edge.svg",'move the inner segement',dummyTask],
		['_My_elevate_inner_Edge', idir+"elevate_inner_edge.svg",'elevate the inner segment',dummyTask],
		['_My_nurbs_grid', idir+"eye.svg",'toggle Nurbs grid',toggleNurbsGrid],
		['_My_nurbs_view', idir+"eyenurbs.svg",'toggle Nurbs Visibility',toggleNurbs],

		['Std_ViewTop'],
		['Std_ViewFront'],
	])


Pie('*#*:Edge,Edge,Edge,Edge',[
		['_My_move_Rectangle', idir+"move_rectangle.svg",'move the complete rectangle',dummyTask],
		['_My_elevate_Rectangle', idir+"elevate_rectangle.svg",'elevate the complete rectangle',dummyTask],
		['_My_smooth_Rectangle', idir+"smooth_rectangle.svg",'smooth or sharp the edges of the  rectangle',dummyTask],
		['_My_circle_Rectangle', idir+"circle_rectangle.svg",'rectangle to square',dummyTask],

		['Std_ViewTop'],
		['Std_ViewFront'],
	])


Pie('PartWorkbench#*:Face',[
		['_My_add_Edge', idir+"add_edge.svg",'add edge',dummyTask],
		['Std_ViewTop'],
		['Std_ViewFront'],
	])


# Vertex in the Part WB
Pie('PartWorkbench#*:Vertex',[
		['Std_ViewTop'],
		['Std_ViewTop'],
		['_My_add_Edgey', idir+"add_edge.svg",'add edge',toggleNurbsGrid],
	])


# nothing selected in the Animation WB
Pie('AnimationWorkbench#:',[
		['Std_ViewFront'],
	])

# a Mover or a Rotator is selected
Pie('AnimationWorkbench#Animation._Rotator|Animation._Mover:',[
		['Std_ViewFront'],
	])


# only a Manager is selected
Pie('AnimationWorkbench#Animation._Manager:',[
		['Std_ViewTop'],
	])

# edge of a box and edge of a cylinder
Pie('PartWorkbench#Part.Box:Edge#Part.Cylinder:Edge',[
		['Std_ViewTop'],
	])

'''


Pie('PartWorkbench#*:Face#*:Edge',[
		['Std_ViewTop'],
		['Anim_Plugger'],
		['Anim_Photographer'],
		['Anim_Toucher']
	])


Pie('PartWorkbench#Animation._Rotator|Part.Box:',[
		['Std_ViewTop'],
		['Std_ViewZoomIn'],
		['Std_ViewZoomOut'],
		['Std_Undo']

	])



# more selection examples
'''

Sketcher.SketchObject
PartDesign.Pad

'''

