# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- piemenu helper functions -
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import FreeCAD as App
import FreeCADGui as Gui

#  FreeCADGui.listWorkbenches()


def sig():
	''' compute a signature of a selection'''

	debug=False
	subs=[]
	wbn=Gui.activeWorkbench().name()

	for s in Gui.Selection.getSelectionEx():
		if debug:
			print s
			print s.ObjectName
			print s.Object.__class__.__name__
			print "Type Id",s.Object.TypeId
			print s.SubElementNames
			print s.SubObjects

#		sub= s.Object.__class__.__name__
		sub= s.Object.TypeId.replace('::','.')

		if sub == 'Part.FeaturePython' or  sub== 'App.DocumentObjectGroupPython' :
			try: 
				tid = s.Object.Proxy.__module__ + '.' + s.Object.Proxy.__class__.__name__
				if tid <>'': sub=tid
			except: pass

		k=[so.__class__.__name__ for so in s.SubObjects]

		sub += ":"+ ','.join(k)
		subs.append(sub)

	if subs==[]: subs=[":"]

	sss=wbn +'#' + '#'.join(subs)
	print "Look for SIGNATURE:\n"+sss+'--'
	return sss
	



def getPieSignatures():
	''' creates a list of all signatures '''

	paramIndexGet = App.ParamGet("User parameter:BaseApp/PieMenu/Index")
	indexList = paramIndexGet.GetString("IndexList")
	if indexList=="": return []
	index=indexList.split('.,.')
	return [paramIndexGet.GetString(ix) for ix in index]

def getSigIndex(sig):
	''' get the index of a signature '''

	paramIndexGet = App.ParamGet("User parameter:BaseApp/PieMenu/Index")
	indexList = paramIndexGet.GetString("IndexList")

	# default
	if indexList=='': return '0'
	index=indexList.split('.,.')

	# find the index
	for ix in index:
		if sig == paramIndexGet.GetString(ix) : return ix

	# create a new if not found 
	newix=str(max([int(ix) for ix in index])+1)
	print "new index for " + sig +" created: " + newix
	return newix 


def activatePieMenu(sig):
	''' set the signature as active pie menue '''

	debug=0
	if sig=='': raise Exception("unexpected signature") 

	paramGet = App.ParamGet("User parameter:BaseApp/PieMenu")
	if debug:
		print "sig=",sig
		print "-------------------"
	sigs=sig.split("#")
	sigapp=sigs[0]
	sigs=sigs[1:]
	
	
	for s in getPieSignatures():
		sl=s.split("#")
		# only complete
		if len(sl)<2: continue
		yapp=sl[0]
		if yapp <> sigapp and yapp<>'*':
#			print "apps fehler " + yapp +"<>" + sigapp
			continue
		sl=sl[1:]

		if debug:
			print "vergleiche"
			print sl
			print sigs

		if len(sl)<>len(sigs):
#			print "unterschiedl lang"
			continue
		anz=len(sl)
		match=True
		for i in range(anz):
			if debug:
				print "runde ",i
				print sl[i]
				print sigs[i]

			if not match: break
			lsos,lsu=sl[i].split(':')
			sigso,sigsu=sigs[i].split(':')
			found=False 
			for lso in lsos.split('|'):
				if found: break
				if lso==sigso or lso=='*':
					found=True
			if not found:
				match=False
				print "Fehler1:" +lsos + "<>" + sigso
				continue
			if lsu<>sigsu and lsu<>'*':
				match=False
				print "Fehler2:" +lsu + "<>" + sigsu
				continue
		
		if match:
			'''

			continue


			[yapp,ysel,ysub]=sl

			#check the workbench
			if sigapp <>yapp and yapp<>'*': continue

			#check the object type list
			ysels=ysel.split('|')
			found=False
			for ysel in ysels:
				if ysel == '*' : found=True
				if sigsel == ysel : found=True
			if not found: continue

			#check the componentes
			if sigsub <>ysub and ysub<>'*': continue
			else:
			'''
			print "found:\n" + s +'--'
			paramGet.SetString("CurrentPie",s)
			return

	# otherhwise
	print "signature [" + sig + "] not found,\nuse Default Pie Menu!"
	paramGet.SetString("CurrentPie",'Default')



