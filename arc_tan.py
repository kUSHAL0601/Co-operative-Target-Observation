import math

def arc_tan(y,x):
	if(y>0 and x>=0):
		if(x==0):
			return math.pi/2
		return math.atan(y/x)
	elif(y<0 and x<=0):
		if(x==0):
			return -math.pi/2
		return math.atan(y/x)+math.pi
	elif(y<0 and x>=0):
		if(x==0):
			return -math.pi/2
		return math.atan(y/x)-math.pi
	else:
		if(x==0):
			return math.pi/2
		return math.atan(y/x)