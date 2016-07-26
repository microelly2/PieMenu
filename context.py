
import FreeCADGui as Gui

class context():

	def count(self):
		print "count"



context().count()



def XXsig():
	ss=Gui.Selection.getSelection()
	for s in ss:
		# 'Feature'
		print s.__class__.__name__


def sig():
	''' compute a signature of a selection'''

	debug=False
	subs=[]

	for s in Gui.Selection.getSelectionEx():
		if debug:
			print s
			print s.ObjectName
			print s.Object.__class__.__name__
			print "Type Id",s.Object.TypeId
			print s.SubElementNames
			print s.SubObjects

		sub= s.Object.__class__.__name__
		if sub == 'FeaturePython' :
			try: 
				tid = s.Object.Proxy.TypeId
				if tid <>'': sub=tid
			except: pass

		k=[so.__class__.__name__ for so in s.SubObjects]
		sub += ":"+ ','.join(k)
		subs.append(sub)

	return '#'.join(subs)
