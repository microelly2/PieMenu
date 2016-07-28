

def sayErr():
	print("--------------ERROR loading piemenu addons ---------------------")

try: raise Exception("test exception from piemenu")
except: sayErr()

#try: import reconstruction.makePlane
#except: sayErr()

