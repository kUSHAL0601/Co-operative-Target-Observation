import math

def arc_tan(y,x):
	if(y>0 and x>=0):
		return math.atan(y/x)
	elif(y<0 and x<=0):
		return math.atan(y/x)+math.pi
	elif(y<0 and x>=0):
		return math.atan(y/x)-math.pi
	else:
		return math.atan(y/x)